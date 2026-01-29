"""Generated wrapper for CumulativePlotSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .DataDescriptorVal import DataDescriptorVal

class CumulativePlotSettingsVal:
    """Simple wrapper for CumulativePlotSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CumulativePlotSettings


    def __init__(self, selected_column: Optional[DataDescriptorVal] = None, proto_message: Optional[Any] = None):
        """Initialize the CumulativePlotSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if selected_column is not None:
            self._proto_message.SelectedColumn.CopyFrom(selected_column.to_proto())
            self._selected_column_wrapper = selected_column


    # Properties

    @property
    def selected_column(self) -> DataDescriptorVal:
        """Get the SelectedColumn field as a wrapper."""
        if not hasattr(self, '_selected_column_wrapper'):
            self._selected_column_wrapper = DataDescriptorVal(proto_message=self._proto_message.SelectedColumn)
        return self._selected_column_wrapper
    
    @selected_column.setter
    def selected_column(self, value: DataDescriptorVal) -> None:
        """Set the SelectedColumn field to a wrapper."""
        self._proto_message.SelectedColumn.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_selected_column_wrapper'):
            self._selected_column_wrapper._proto_message.CopyFrom(self._proto_message.SelectedColumn)


    @property
    def num_bins(self) -> int:
        """Get the NumBins field value."""
        return self._proto_message.NumBins
    
    @num_bins.setter
    def num_bins(self, value: int) -> None:
        """Set the NumBins field value."""
        self._proto_message.NumBins = value


    @property
    def is_weighted(self) -> bool:
        """Get the IsWeighted field value."""
        return self._proto_message.IsWeighted
    
    @is_weighted.setter
    def is_weighted(self, value: bool) -> None:
        """Set the IsWeighted field value."""
        self._proto_message.IsWeighted = value


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
