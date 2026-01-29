"""Generated wrapper for SetWindowEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .CircularWindowVal import CircularWindowVal
from .ClusterWindowVal import ClusterWindowVal
from .ColorSurrogateVal import ColorSurrogateVal
from .CurvedWindowVal import CurvedWindowVal
from .SetStatisticsSettingsVal import SetStatisticsSettingsVal
from .WrappedFreehandWindowVal import WrappedFreehandWindowVal

class SetWindowEntityInfoVal:
    """Simple wrapper for SetWindowEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SetWindowEntityInfo


    def __init__(self, color: Optional[ColorSurrogateVal] = None, statistics_settings: Optional[SetStatisticsSettingsVal] = None, circular_set_window: Optional[CircularWindowVal] = None, curved_set_window: Optional[CurvedWindowVal] = None, wrapped_freehand_set_window: Optional[WrappedFreehandWindowVal] = None, cluster_set_window: Optional[ClusterWindowVal] = None, proto_message: Optional[Any] = None):
        """Initialize the SetWindowEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if statistics_settings is not None:
            self._proto_message.StatisticsSettings.CopyFrom(statistics_settings.to_proto())
            self._statistics_settings_wrapper = statistics_settings
        if circular_set_window is not None:
            self._proto_message.CircularSetWindow.CopyFrom(circular_set_window.to_proto())
            self._circular_set_window_wrapper = circular_set_window
        if curved_set_window is not None:
            self._proto_message.CurvedSetWindow.CopyFrom(curved_set_window.to_proto())
            self._curved_set_window_wrapper = curved_set_window
        if wrapped_freehand_set_window is not None:
            self._proto_message.WrappedFreehandSetWindow.CopyFrom(wrapped_freehand_set_window.to_proto())
            self._wrapped_freehand_set_window_wrapper = wrapped_freehand_set_window
        if cluster_set_window is not None:
            self._proto_message.ClusterSetWindow.CopyFrom(cluster_set_window.to_proto())
            self._cluster_set_window_wrapper = cluster_set_window


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
    def set_window_type(self) -> Any:
        """Get the SetWindowType field value."""
        return self._proto_message.SetWindowType
    
    @set_window_type.setter
    def set_window_type(self, value: Any) -> None:
        """Set the SetWindowType field value."""
        self._proto_message.SetWindowType = value


    @property
    def statistics_settings(self) -> SetStatisticsSettingsVal:
        """Get the StatisticsSettings field as a wrapper."""
        if not hasattr(self, '_statistics_settings_wrapper'):
            self._statistics_settings_wrapper = SetStatisticsSettingsVal(proto_message=self._proto_message.StatisticsSettings)
        return self._statistics_settings_wrapper
    
    @statistics_settings.setter
    def statistics_settings(self, value: SetStatisticsSettingsVal) -> None:
        """Set the StatisticsSettings field to a wrapper."""
        self._proto_message.StatisticsSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_statistics_settings_wrapper'):
            self._statistics_settings_wrapper._proto_message.CopyFrom(self._proto_message.StatisticsSettings)


    @property
    def circular_set_window(self) -> CircularWindowVal:
        """Get the CircularSetWindow field as a wrapper."""
        if not hasattr(self, '_circular_set_window_wrapper'):
            self._circular_set_window_wrapper = CircularWindowVal(proto_message=self._proto_message.CircularSetWindow)
        return self._circular_set_window_wrapper
    
    @circular_set_window.setter
    def circular_set_window(self, value: CircularWindowVal) -> None:
        """Set the CircularSetWindow field to a wrapper."""
        self._proto_message.CircularSetWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_circular_set_window_wrapper'):
            self._circular_set_window_wrapper._proto_message.CopyFrom(self._proto_message.CircularSetWindow)


    @property
    def curved_set_window(self) -> CurvedWindowVal:
        """Get the CurvedSetWindow field as a wrapper."""
        if not hasattr(self, '_curved_set_window_wrapper'):
            self._curved_set_window_wrapper = CurvedWindowVal(proto_message=self._proto_message.CurvedSetWindow)
        return self._curved_set_window_wrapper
    
    @curved_set_window.setter
    def curved_set_window(self, value: CurvedWindowVal) -> None:
        """Set the CurvedSetWindow field to a wrapper."""
        self._proto_message.CurvedSetWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_curved_set_window_wrapper'):
            self._curved_set_window_wrapper._proto_message.CopyFrom(self._proto_message.CurvedSetWindow)


    @property
    def wrapped_freehand_set_window(self) -> WrappedFreehandWindowVal:
        """Get the WrappedFreehandSetWindow field as a wrapper."""
        if not hasattr(self, '_wrapped_freehand_set_window_wrapper'):
            self._wrapped_freehand_set_window_wrapper = WrappedFreehandWindowVal(proto_message=self._proto_message.WrappedFreehandSetWindow)
        return self._wrapped_freehand_set_window_wrapper
    
    @wrapped_freehand_set_window.setter
    def wrapped_freehand_set_window(self, value: WrappedFreehandWindowVal) -> None:
        """Set the WrappedFreehandSetWindow field to a wrapper."""
        self._proto_message.WrappedFreehandSetWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_wrapped_freehand_set_window_wrapper'):
            self._wrapped_freehand_set_window_wrapper._proto_message.CopyFrom(self._proto_message.WrappedFreehandSetWindow)


    @property
    def cluster_set_window(self) -> ClusterWindowVal:
        """Get the ClusterSetWindow field as a wrapper."""
        if not hasattr(self, '_cluster_set_window_wrapper'):
            self._cluster_set_window_wrapper = ClusterWindowVal(proto_message=self._proto_message.ClusterSetWindow)
        return self._cluster_set_window_wrapper
    
    @cluster_set_window.setter
    def cluster_set_window(self, value: ClusterWindowVal) -> None:
        """Set the ClusterSetWindow field to a wrapper."""
        self._proto_message.ClusterSetWindow.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_cluster_set_window_wrapper'):
            self._cluster_set_window_wrapper._proto_message.CopyFrom(self._proto_message.ClusterSetWindow)


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
