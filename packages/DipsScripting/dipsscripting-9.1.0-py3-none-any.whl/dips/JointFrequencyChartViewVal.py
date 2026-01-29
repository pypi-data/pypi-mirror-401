"""Generated wrapper for JointFrequencyChartView protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .JointFrequencyAnalysisSettingsVal import JointFrequencyAnalysisSettingsVal
from .DataFilterRef import DataFilterRef

class JointFrequencyChartViewVal:
    """Simple wrapper for JointFrequencyChartView with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.JointFrequencyChartView


    def __init__(self, joint_frequency_analysis_settings: Optional[JointFrequencyAnalysisSettingsVal] = None, active_filter: Optional[DataFilterRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the JointFrequencyChartView wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if joint_frequency_analysis_settings is not None:
            self._proto_message.JointFrequencyAnalysisSettings.CopyFrom(joint_frequency_analysis_settings.to_proto())
            self._joint_frequency_analysis_settings_wrapper = joint_frequency_analysis_settings
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
    def joint_frequency_analysis_settings(self) -> JointFrequencyAnalysisSettingsVal:
        """Get the JointFrequencyAnalysisSettings field as a wrapper."""
        if not hasattr(self, '_joint_frequency_analysis_settings_wrapper'):
            self._joint_frequency_analysis_settings_wrapper = JointFrequencyAnalysisSettingsVal(proto_message=self._proto_message.JointFrequencyAnalysisSettings)
        return self._joint_frequency_analysis_settings_wrapper
    
    @joint_frequency_analysis_settings.setter
    def joint_frequency_analysis_settings(self, value: JointFrequencyAnalysisSettingsVal) -> None:
        """Set the JointFrequencyAnalysisSettings field to a wrapper."""
        self._proto_message.JointFrequencyAnalysisSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_joint_frequency_analysis_settings_wrapper'):
            self._joint_frequency_analysis_settings_wrapper._proto_message.CopyFrom(self._proto_message.JointFrequencyAnalysisSettings)


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
