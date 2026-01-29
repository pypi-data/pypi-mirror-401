"""Generated wrapper for StereonetOverlayEntityVisibility protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .StereonetOverlaySettingsVal import StereonetOverlaySettingsVal

class StereonetOverlayEntityVisibilityVal:
    """Simple wrapper for StereonetOverlayEntityVisibility with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.StereonetOverlayEntityVisibility


    def __init__(self, stereonet_overlay_settings: Optional[StereonetOverlaySettingsVal] = None, proto_message: Optional[Any] = None):
        """Initialize the StereonetOverlayEntityVisibility wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if stereonet_overlay_settings is not None:
            self._proto_message.StereonetOverlaySettings.CopyFrom(stereonet_overlay_settings.to_proto())
            self._stereonet_overlay_settings_wrapper = stereonet_overlay_settings


    # Properties

    @property
    def is_visible(self) -> bool:
        """Get the IsVisible field value."""
        return self._proto_message.IsVisible
    
    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        """Set the IsVisible field value."""
        self._proto_message.IsVisible = value


    @property
    def stereonet_overlay_settings(self) -> StereonetOverlaySettingsVal:
        """Get the StereonetOverlaySettings field as a wrapper."""
        if not hasattr(self, '_stereonet_overlay_settings_wrapper'):
            self._stereonet_overlay_settings_wrapper = StereonetOverlaySettingsVal(proto_message=self._proto_message.StereonetOverlaySettings)
        return self._stereonet_overlay_settings_wrapper
    
    @stereonet_overlay_settings.setter
    def stereonet_overlay_settings(self, value: StereonetOverlaySettingsVal) -> None:
        """Set the StereonetOverlaySettings field to a wrapper."""
        self._proto_message.StereonetOverlaySettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_stereonet_overlay_settings_wrapper'):
            self._stereonet_overlay_settings_wrapper._proto_message.CopyFrom(self._proto_message.StereonetOverlaySettings)


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
