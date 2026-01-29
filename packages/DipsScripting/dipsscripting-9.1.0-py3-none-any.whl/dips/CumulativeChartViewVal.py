"""Generated wrapper for CumulativeChartView protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .CumulativePlotSettingsVal import CumulativePlotSettingsVal
from .DataFilterRef import DataFilterRef

class CumulativeChartViewVal:
    """Simple wrapper for CumulativeChartView with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CumulativeChartView


    def __init__(self, cumulative_plot_settings: Optional[CumulativePlotSettingsVal] = None, active_filter: Optional[DataFilterRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the CumulativeChartView wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if cumulative_plot_settings is not None:
            self._proto_message.CumulativePlotSettings.CopyFrom(cumulative_plot_settings.to_proto())
            self._cumulative_plot_settings_wrapper = cumulative_plot_settings
        if active_filter is not None:
            self.active_filter = active_filter


    # Properties

    @property
    def view_name(self) -> str:
        """Get the ViewName field value."""
        return self._proto_message.ViewName
    
    @view_name.setter
    def view_name(self, value: str) -> None:
        """Set the ViewName field value."""
        self._proto_message.ViewName = value


    @property
    def cumulative_plot_settings(self) -> CumulativePlotSettingsVal:
        """Get the CumulativePlotSettings field as a wrapper."""
        if not hasattr(self, '_cumulative_plot_settings_wrapper'):
            self._cumulative_plot_settings_wrapper = CumulativePlotSettingsVal(proto_message=self._proto_message.CumulativePlotSettings)
        return self._cumulative_plot_settings_wrapper
    
    @cumulative_plot_settings.setter
    def cumulative_plot_settings(self, value: CumulativePlotSettingsVal) -> None:
        """Set the CumulativePlotSettings field to a wrapper."""
        self._proto_message.CumulativePlotSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_cumulative_plot_settings_wrapper'):
            self._cumulative_plot_settings_wrapper._proto_message.CopyFrom(self._proto_message.CumulativePlotSettings)


    @property
    def active_filter(self) -> DataFilterRef:
        """Get the ActiveFilter field as a reference."""
        return DataFilterRef(self.__channelToConnectOn, self._proto_message.ActiveFilter)
    
    @active_filter.setter
    def active_filter(self, value: DataFilterRef) -> None:
        """Set the ActiveFilter field to a reference."""
        self._proto_message.ActiveFilter.CopyFrom(value.get_model_ref())


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
