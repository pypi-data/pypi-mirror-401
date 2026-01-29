"""Generated wrapper for DataDescriptor protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .DataIdentifierVal import DataIdentifierVal

class DataDescriptorVal:
    """Simple wrapper for DataDescriptor with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.DataDescriptor


    def __init__(self, data_name: Optional[DataIdentifierVal] = None, proto_message: Optional[Any] = None):
        """Initialize the DataDescriptor wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if data_name is not None:
            self._proto_message.DataName.CopyFrom(data_name.to_proto())
            self._data_name_wrapper = data_name


    # Properties

    @property
    def data_name(self) -> DataIdentifierVal:
        """Get the DataName field as a wrapper."""
        if not hasattr(self, '_data_name_wrapper'):
            self._data_name_wrapper = DataIdentifierVal(proto_message=self._proto_message.DataName)
        return self._data_name_wrapper
    
    @data_name.setter
    def data_name(self, value: DataIdentifierVal) -> None:
        """Set the DataName field to a wrapper."""
        self._proto_message.DataName.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_data_name_wrapper'):
            self._data_name_wrapper._proto_message.CopyFrom(self._proto_message.DataName)


    @property
    def data_type(self) -> Any:
        """Get the DataType field value."""
        return self._proto_message.DataType
    
    @data_type.setter
    def data_type(self, value: Any) -> None:
        """Set the DataType field value."""
        self._proto_message.DataType = value


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
