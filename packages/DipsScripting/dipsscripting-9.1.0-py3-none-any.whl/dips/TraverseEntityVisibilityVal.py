"""Generated wrapper for TraverseEntityVisibility protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .TraverseEntityOptionsVal import TraverseEntityOptionsVal
from .OrientationDataSetRef import OrientationDataSetRef

class TraverseEntityVisibilityVal:
    """Simple wrapper for TraverseEntityVisibility with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.TraverseEntityVisibility


    def __init__(self, options: Optional[TraverseEntityOptionsVal] = None, traverse_entity_reference: Optional[OrientationDataSetRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the TraverseEntityVisibility wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if options is not None:
            self._proto_message.Options.CopyFrom(options.to_proto())
            self._options_wrapper = options
        if traverse_entity_reference is not None:
            self.traverse_entity_reference = traverse_entity_reference


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
    def options(self) -> TraverseEntityOptionsVal:
        """Get the Options field as a wrapper."""
        if not hasattr(self, '_options_wrapper'):
            self._options_wrapper = TraverseEntityOptionsVal(proto_message=self._proto_message.Options)
        return self._options_wrapper
    
    @options.setter
    def options(self, value: TraverseEntityOptionsVal) -> None:
        """Set the Options field to a wrapper."""
        self._proto_message.Options.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_options_wrapper'):
            self._options_wrapper._proto_message.CopyFrom(self._proto_message.Options)


    @property
    def traverse_entity_reference(self) -> OrientationDataSetRef:
        """Get the TraverseEntityReference field as a reference."""
        return OrientationDataSetRef(self.__channelToConnectOn, self._proto_message.TraverseEntityReference)
    
    @traverse_entity_reference.setter
    def traverse_entity_reference(self, value: OrientationDataSetRef) -> None:
        """Set the TraverseEntityReference field to a reference."""
        self._proto_message.TraverseEntityReference.CopyFrom(value.get_model_ref())


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
