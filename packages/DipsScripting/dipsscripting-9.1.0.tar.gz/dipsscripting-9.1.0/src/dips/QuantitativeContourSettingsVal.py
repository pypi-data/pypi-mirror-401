"""Generated wrapper for QuantitativeContourSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal
from .DataDescriptorVal import DataDescriptorVal

class QuantitativeContourSettingsVal:
    """Simple wrapper for QuantitativeContourSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.QuantitativeContourSettings


    def __init__(self, local_angle: Optional[AngleDataVal] = None, selected_column: Optional[DataDescriptorVal] = None, proto_message: Optional[Any] = None):
        """Initialize the QuantitativeContourSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if local_angle is not None:
            self._proto_message.LocalAngle.CopyFrom(local_angle.to_proto())
            self._local_angle_wrapper = local_angle
        if selected_column is not None:
            self._proto_message.SelectedColumn.CopyFrom(selected_column.to_proto())
            self._selected_column_wrapper = selected_column


    # Properties

    @property
    def interpolation(self) -> Any:
        """Get the Interpolation field value."""
        return self._proto_message.Interpolation
    
    @interpolation.setter
    def interpolation(self, value: Any) -> None:
        """Set the Interpolation field value."""
        self._proto_message.Interpolation = value


    @property
    def local_angle(self) -> AngleDataVal:
        """Get the LocalAngle field as a wrapper."""
        if not hasattr(self, '_local_angle_wrapper'):
            self._local_angle_wrapper = AngleDataVal(proto_message=self._proto_message.LocalAngle)
        return self._local_angle_wrapper
    
    @local_angle.setter
    def local_angle(self, value: AngleDataVal) -> None:
        """Set the LocalAngle field to a wrapper."""
        self._proto_message.LocalAngle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_local_angle_wrapper'):
            self._local_angle_wrapper._proto_message.CopyFrom(self._proto_message.LocalAngle)


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
