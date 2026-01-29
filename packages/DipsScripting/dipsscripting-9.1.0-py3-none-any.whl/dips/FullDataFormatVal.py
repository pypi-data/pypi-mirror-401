"""Generated wrapper for FullDataFormat protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .DataDescriptorVal import DataDescriptorVal
from .DataFormatterVal import DataFormatterVal

class FullDataFormatVal:
    """Simple wrapper for FullDataFormat with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.FullDataFormat


    def __init__(self, descriptor: Optional[DataDescriptorVal] = None, format: Optional[DataFormatterVal] = None, proto_message: Optional[Any] = None):
        """Initialize the FullDataFormat wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if descriptor is not None:
            self._proto_message.Descriptor.CopyFrom(descriptor.to_proto())
            self._descriptor_wrapper = descriptor
        if format is not None:
            self._proto_message.Format.CopyFrom(format.to_proto())
            self._format_wrapper = format


    # Properties

    @property
    def descriptor(self) -> DataDescriptorVal:
        """Get the Descriptor field as a wrapper."""
        if not hasattr(self, '_descriptor_wrapper'):
            self._descriptor_wrapper = DataDescriptorVal(proto_message=self._proto_message.Descriptor)
        return self._descriptor_wrapper
    
    @descriptor.setter
    def descriptor(self, value: DataDescriptorVal) -> None:
        """Set the Descriptor field to a wrapper."""
        self._proto_message.Descriptor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_descriptor_wrapper'):
            self._descriptor_wrapper._proto_message.CopyFrom(self._proto_message.Descriptor)


    @property
    def format(self) -> DataFormatterVal:
        """Get the Format field as a wrapper."""
        if not hasattr(self, '_format_wrapper'):
            self._format_wrapper = DataFormatterVal(proto_message=self._proto_message.Format)
        return self._format_wrapper
    
    @format.setter
    def format(self, value: DataFormatterVal) -> None:
        """Set the Format field to a wrapper."""
        self._proto_message.Format.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_format_wrapper'):
            self._format_wrapper._proto_message.CopyFrom(self._proto_message.Format)


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
