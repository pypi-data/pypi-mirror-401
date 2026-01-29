"""Generated wrapper for ScatterPlotSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .DataDescriptorVal import DataDescriptorVal

class ScatterPlotSettingsVal:
    """Simple wrapper for ScatterPlotSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ScatterPlotSettings


    def __init__(self, selected_column_x: Optional[DataDescriptorVal] = None, selected_column_y: Optional[DataDescriptorVal] = None, proto_message: Optional[Any] = None):
        """Initialize the ScatterPlotSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if selected_column_x is not None:
            self._proto_message.SelectedColumnX.CopyFrom(selected_column_x.to_proto())
            self._selected_column_x_wrapper = selected_column_x
        if selected_column_y is not None:
            self._proto_message.SelectedColumnY.CopyFrom(selected_column_y.to_proto())
            self._selected_column_y_wrapper = selected_column_y


    # Properties

    @property
    def selected_column_x(self) -> DataDescriptorVal:
        """Get the SelectedColumnX field as a wrapper."""
        if not hasattr(self, '_selected_column_x_wrapper'):
            self._selected_column_x_wrapper = DataDescriptorVal(proto_message=self._proto_message.SelectedColumnX)
        return self._selected_column_x_wrapper
    
    @selected_column_x.setter
    def selected_column_x(self, value: DataDescriptorVal) -> None:
        """Set the SelectedColumnX field to a wrapper."""
        self._proto_message.SelectedColumnX.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_selected_column_x_wrapper'):
            self._selected_column_x_wrapper._proto_message.CopyFrom(self._proto_message.SelectedColumnX)


    @property
    def selected_column_y(self) -> DataDescriptorVal:
        """Get the SelectedColumnY field as a wrapper."""
        if not hasattr(self, '_selected_column_y_wrapper'):
            self._selected_column_y_wrapper = DataDescriptorVal(proto_message=self._proto_message.SelectedColumnY)
        return self._selected_column_y_wrapper
    
    @selected_column_y.setter
    def selected_column_y(self, value: DataDescriptorVal) -> None:
        """Set the SelectedColumnY field to a wrapper."""
        self._proto_message.SelectedColumnY.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_selected_column_y_wrapper'):
            self._selected_column_y_wrapper._proto_message.CopyFrom(self._proto_message.SelectedColumnY)


    @property
    def show_regression_line(self) -> bool:
        """Get the ShowRegressionLine field value."""
        return self._proto_message.ShowRegressionLine
    
    @show_regression_line.setter
    def show_regression_line(self, value: bool) -> None:
        """Set the ShowRegressionLine field value."""
        self._proto_message.ShowRegressionLine = value


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
