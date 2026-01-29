"""Generated wrapper for WrappedFreehandWindow protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .FreehandWindowVal import FreehandWindowVal

class WrappedFreehandWindowVal:
    """Simple wrapper for WrappedFreehandWindow with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.WrappedFreehandWindow


    def __init__(self, primary_window: Optional[FreehandWindowVal] = None, secondary_window: Optional[FreehandWindowVal] = None, proto_message: Optional[Any] = None):
        """Initialize the WrappedFreehandWindow wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if primary_window is not None:
            self._proto_message.PrimaryWindow.CopyFrom(primary_window.to_proto())
            self._primary_window_wrapper = primary_window
        if secondary_window is not None:
            self._proto_message.SecondaryWindow.CopyFrom(secondary_window.to_proto())
            self._secondary_window_wrapper = secondary_window


    # Properties

    @property
    def id(self) -> str:
        """Get the ID field value."""
        return self._proto_message.ID
    
    @id.setter
    def id(self, value: str) -> None:
        """Set the ID field value."""
        self._proto_message.ID = value


    @property
    def primary_window(self) -> FreehandWindowVal:
        """Get the PrimaryWindow field as a wrapper."""
        if not hasattr(self, '_primary_window_wrapper'):
            self._primary_window_wrapper = FreehandWindowVal(proto_message=self._proto_message.PrimaryWindow)
        return self._primary_window_wrapper
    
    @primary_window.setter
    def primary_window(self, value: FreehandWindowVal) -> None:
        """Set the PrimaryWindow field to a wrapper."""
        self._proto_message.PrimaryWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_primary_window_wrapper'):
            self._primary_window_wrapper._proto_message.CopyFrom(self._proto_message.PrimaryWindow)


    @property
    def secondary_window(self) -> FreehandWindowVal:
        """Get the SecondaryWindow field as a wrapper."""
        if not hasattr(self, '_secondary_window_wrapper'):
            self._secondary_window_wrapper = FreehandWindowVal(proto_message=self._proto_message.SecondaryWindow)
        return self._secondary_window_wrapper
    
    @secondary_window.setter
    def secondary_window(self, value: FreehandWindowVal) -> None:
        """Set the SecondaryWindow field to a wrapper."""
        self._proto_message.SecondaryWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_secondary_window_wrapper'):
            self._secondary_window_wrapper._proto_message.CopyFrom(self._proto_message.SecondaryWindow)


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
