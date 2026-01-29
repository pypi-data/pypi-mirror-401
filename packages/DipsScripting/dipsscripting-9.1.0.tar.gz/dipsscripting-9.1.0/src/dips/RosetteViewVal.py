"""Generated wrapper for RosetteView protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AnnotativeTools2DVal import AnnotativeTools2DVal
from .PlaneEntityVisibilityVal import PlaneEntityVisibilityVal
from .RosettePresetOptionsVal import RosettePresetOptionsVal
from .RosetteSettingsVal import RosetteSettingsVal
from .StereonetProjectionModeVal import StereonetProjectionModeVal
from .DataFilterRef import DataFilterRef

class RosetteViewVal:
    """Simple wrapper for RosetteView with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.RosetteView


    def __init__(self, rosette_settings: Optional[RosetteSettingsVal] = None, projection_mode: Optional[StereonetProjectionModeVal] = None, preset_options: Optional[RosettePresetOptionsVal] = None, annotative_tools: Optional[AnnotativeTools2DVal] = None, active_filter: Optional[DataFilterRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the RosetteView wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if rosette_settings is not None:
            self._proto_message.RosetteSettings.CopyFrom(rosette_settings.to_proto())
            self._rosette_settings_wrapper = rosette_settings
        if projection_mode is not None:
            self._proto_message.ProjectionMode.CopyFrom(projection_mode.to_proto())
            self._projection_mode_wrapper = projection_mode
        if preset_options is not None:
            self._proto_message.PresetOptions.CopyFrom(preset_options.to_proto())
            self._preset_options_wrapper = preset_options
        if annotative_tools is not None:
            self._proto_message.AnnotativeTools.CopyFrom(annotative_tools.to_proto())
            self._annotative_tools_wrapper = annotative_tools
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
    def rosette_settings(self) -> RosetteSettingsVal:
        """Get the RosetteSettings field as a wrapper."""
        if not hasattr(self, '_rosette_settings_wrapper'):
            self._rosette_settings_wrapper = RosetteSettingsVal(proto_message=self._proto_message.RosetteSettings)
        return self._rosette_settings_wrapper
    
    @rosette_settings.setter
    def rosette_settings(self, value: RosetteSettingsVal) -> None:
        """Set the RosetteSettings field to a wrapper."""
        self._proto_message.RosetteSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_rosette_settings_wrapper'):
            self._rosette_settings_wrapper._proto_message.CopyFrom(self._proto_message.RosetteSettings)


    @property
    def projection_mode(self) -> StereonetProjectionModeVal:
        """Get the ProjectionMode field as a wrapper."""
        if not hasattr(self, '_projection_mode_wrapper'):
            self._projection_mode_wrapper = StereonetProjectionModeVal(proto_message=self._proto_message.ProjectionMode)
        return self._projection_mode_wrapper
    
    @projection_mode.setter
    def projection_mode(self, value: StereonetProjectionModeVal) -> None:
        """Set the ProjectionMode field to a wrapper."""
        self._proto_message.ProjectionMode.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_projection_mode_wrapper'):
            self._projection_mode_wrapper._proto_message.CopyFrom(self._proto_message.ProjectionMode)


    @property
    def preset_options(self) -> RosettePresetOptionsVal:
        """Get the PresetOptions field as a wrapper."""
        if not hasattr(self, '_preset_options_wrapper'):
            self._preset_options_wrapper = RosettePresetOptionsVal(proto_message=self._proto_message.PresetOptions)
        return self._preset_options_wrapper
    
    @preset_options.setter
    def preset_options(self, value: RosettePresetOptionsVal) -> None:
        """Set the PresetOptions field to a wrapper."""
        self._proto_message.PresetOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_preset_options_wrapper'):
            self._preset_options_wrapper._proto_message.CopyFrom(self._proto_message.PresetOptions)


    @property
    def user_plane_entity_visibilities(self) -> List[PlaneEntityVisibilityVal]:
        """Get the UserPlaneEntityVisibilities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.UserPlaneEntityVisibilities, PlaneEntityVisibilityVal)
    
    @user_plane_entity_visibilities.setter
    def user_plane_entity_visibilities(self, value: List[PlaneEntityVisibilityVal]) -> None:
        """Set the UserPlaneEntityVisibilities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.UserPlaneEntityVisibilities[:] = []
        for item in value:
            self._proto_message.UserPlaneEntityVisibilities.append(item.to_proto())


    @property
    def annotative_tools(self) -> AnnotativeTools2DVal:
        """Get the AnnotativeTools field as a wrapper."""
        if not hasattr(self, '_annotative_tools_wrapper'):
            self._annotative_tools_wrapper = AnnotativeTools2DVal(proto_message=self._proto_message.AnnotativeTools)
        return self._annotative_tools_wrapper
    
    @annotative_tools.setter
    def annotative_tools(self, value: AnnotativeTools2DVal) -> None:
        """Set the AnnotativeTools field to a wrapper."""
        self._proto_message.AnnotativeTools.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_annotative_tools_wrapper'):
            self._annotative_tools_wrapper._proto_message.CopyFrom(self._proto_message.AnnotativeTools)


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
