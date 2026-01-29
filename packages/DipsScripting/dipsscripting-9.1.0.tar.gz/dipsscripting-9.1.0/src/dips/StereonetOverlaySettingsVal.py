"""Generated wrapper for StereonetOverlaySettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .TrendPlungeVal import TrendPlungeVal

class StereonetOverlaySettingsVal:
    """Simple wrapper for StereonetOverlaySettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.StereonetOverlaySettings


    def __init__(self, color: Optional[ColorSurrogateVal] = None, custom_orientation: Optional[TrendPlungeVal] = None, proto_message: Optional[Any] = None):
        """Initialize the StereonetOverlaySettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if custom_orientation is not None:
            self._proto_message.CustomOrientation.CopyFrom(custom_orientation.to_proto())
            self._custom_orientation_wrapper = custom_orientation


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
    def option(self) -> Any:
        """Get the Option field value."""
        return self._proto_message.Option
    
    @option.setter
    def option(self, value: Any) -> None:
        """Set the Option field value."""
        self._proto_message.Option = value


    @property
    def custom_orientation(self) -> TrendPlungeVal:
        """Get the CustomOrientation field as a wrapper."""
        if not hasattr(self, '_custom_orientation_wrapper'):
            self._custom_orientation_wrapper = TrendPlungeVal(proto_message=self._proto_message.CustomOrientation)
        return self._custom_orientation_wrapper
    
    @custom_orientation.setter
    def custom_orientation(self, value: TrendPlungeVal) -> None:
        """Set the CustomOrientation field to a wrapper."""
        self._proto_message.CustomOrientation.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_custom_orientation_wrapper'):
            self._custom_orientation_wrapper._proto_message.CopyFrom(self._proto_message.CustomOrientation)


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
