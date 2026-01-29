"""Generated wrapper for FoldEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .FoldWindowEntityInfoVal import FoldWindowEntityInfoVal

class FoldEntityInfoVal:
    """Simple wrapper for FoldEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.FoldEntityInfo


    def __init__(self, color: Optional[ColorSurrogateVal] = None, fold_window_entity_info: Optional[FoldWindowEntityInfoVal] = None, proto_message: Optional[Any] = None):
        """Initialize the FoldEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if fold_window_entity_info is not None:
            self._proto_message.FoldWindowEntityInfo.CopyFrom(fold_window_entity_info.to_proto())
            self._fold_window_entity_info_wrapper = fold_window_entity_info


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
    def fold_window_entity_info(self) -> FoldWindowEntityInfoVal:
        """Get the FoldWindowEntityInfo field as a wrapper."""
        if not hasattr(self, '_fold_window_entity_info_wrapper'):
            self._fold_window_entity_info_wrapper = FoldWindowEntityInfoVal(proto_message=self._proto_message.FoldWindowEntityInfo)
        return self._fold_window_entity_info_wrapper
    
    @fold_window_entity_info.setter
    def fold_window_entity_info(self, value: FoldWindowEntityInfoVal) -> None:
        """Set the FoldWindowEntityInfo field to a wrapper."""
        self._proto_message.FoldWindowEntityInfo.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_fold_window_entity_info_wrapper'):
            self._fold_window_entity_info_wrapper._proto_message.CopyFrom(self._proto_message.FoldWindowEntityInfo)


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
