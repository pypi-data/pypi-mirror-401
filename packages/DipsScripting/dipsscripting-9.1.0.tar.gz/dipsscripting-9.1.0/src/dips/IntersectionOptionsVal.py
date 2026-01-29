"""Generated wrapper for IntersectionOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .SetVersusSetVal import SetVersusSetVal

class IntersectionOptionsVal:
    """Simple wrapper for IntersectionOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.IntersectionOptions


    def __init__(self, set_versus_set: Optional[SetVersusSetVal] = None, proto_message: Optional[Any] = None):
        """Initialize the IntersectionOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if set_versus_set is not None:
            self._proto_message.SetVersusSet.CopyFrom(set_versus_set.to_proto())
            self._set_versus_set_wrapper = set_versus_set


    # Properties

    @property
    def intersection_type(self) -> Any:
        """Get the IntersectionType field value."""
        return self._proto_message.IntersectionType
    
    @intersection_type.setter
    def intersection_type(self, value: Any) -> None:
        """Set the IntersectionType field value."""
        self._proto_message.IntersectionType = value


    @property
    def set_versus_set(self) -> SetVersusSetVal:
        """Get the SetVersusSet field as a wrapper."""
        if not hasattr(self, '_set_versus_set_wrapper'):
            self._set_versus_set_wrapper = SetVersusSetVal(proto_message=self._proto_message.SetVersusSet)
        return self._set_versus_set_wrapper
    
    @set_versus_set.setter
    def set_versus_set(self, value: SetVersusSetVal) -> None:
        """Set the SetVersusSet field to a wrapper."""
        self._proto_message.SetVersusSet.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_set_versus_set_wrapper'):
            self._set_versus_set_wrapper._proto_message.CopyFrom(self._proto_message.SetVersusSet)


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
