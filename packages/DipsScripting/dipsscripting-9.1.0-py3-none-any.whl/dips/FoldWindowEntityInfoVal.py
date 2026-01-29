"""Generated wrapper for FoldWindowEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .WrappedFreehandWindowVal import WrappedFreehandWindowVal

class FoldWindowEntityInfoVal:
    """Simple wrapper for FoldWindowEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.FoldWindowEntityInfo


    def __init__(self, color: Optional[ColorSurrogateVal] = None, wrapped_freehand_fold_window: Optional[WrappedFreehandWindowVal] = None, proto_message: Optional[Any] = None):
        """Initialize the FoldWindowEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if wrapped_freehand_fold_window is not None:
            self._proto_message.WrappedFreehandFoldWindow.CopyFrom(wrapped_freehand_fold_window.to_proto())
            self._wrapped_freehand_fold_window_wrapper = wrapped_freehand_fold_window


    # Properties

    @property
    def color(self) -> ColorSurrogateVal:
        """Get the Color field as a wrapper."""
        if not hasattr(self, '_color_wrapper'):
            self._color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.Color)
        return self._color_wrapper
    
    @color.setter
    def color(self, value: ColorSurrogateVal) -> None:
        """Set the Color field to a wrapper."""
        self._proto_message.Color.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_color_wrapper'):
            self._color_wrapper._proto_message.CopyFrom(self._proto_message.Color)


    @property
    def wrapped_freehand_fold_window(self) -> WrappedFreehandWindowVal:
        """Get the WrappedFreehandFoldWindow field as a wrapper."""
        if not hasattr(self, '_wrapped_freehand_fold_window_wrapper'):
            self._wrapped_freehand_fold_window_wrapper = WrappedFreehandWindowVal(proto_message=self._proto_message.WrappedFreehandFoldWindow)
        return self._wrapped_freehand_fold_window_wrapper
    
    @wrapped_freehand_fold_window.setter
    def wrapped_freehand_fold_window(self, value: WrappedFreehandWindowVal) -> None:
        """Set the WrappedFreehandFoldWindow field to a wrapper."""
        self._proto_message.WrappedFreehandFoldWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_wrapped_freehand_fold_window_wrapper'):
            self._wrapped_freehand_fold_window_wrapper._proto_message.CopyFrom(self._proto_message.WrappedFreehandFoldWindow)


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
