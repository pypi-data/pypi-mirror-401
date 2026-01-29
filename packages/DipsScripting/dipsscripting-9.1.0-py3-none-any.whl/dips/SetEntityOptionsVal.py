"""Generated wrapper for SetEntityOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .PlaneOptionsVal import PlaneOptionsVal

class SetEntityOptionsVal:
    """Simple wrapper for SetEntityOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SetEntityOptions


    def __init__(self, plane_options: Optional[PlaneOptionsVal] = None, confidence_cone_color: Optional[ColorSurrogateVal] = None, variability_cone_color: Optional[ColorSurrogateVal] = None, proto_message: Optional[Any] = None):
        """Initialize the SetEntityOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if plane_options is not None:
            self._proto_message.PlaneOptions.CopyFrom(plane_options.to_proto())
            self._plane_options_wrapper = plane_options
        if confidence_cone_color is not None:
            self._proto_message.ConfidenceConeColor.CopyFrom(confidence_cone_color.to_proto())
            self._confidence_cone_color_wrapper = confidence_cone_color
        if variability_cone_color is not None:
            self._proto_message.VariabilityConeColor.CopyFrom(variability_cone_color.to_proto())
            self._variability_cone_color_wrapper = variability_cone_color


    # Properties

    @property
    def plane_options(self) -> PlaneOptionsVal:
        """Get the PlaneOptions field as a wrapper."""
        if not hasattr(self, '_plane_options_wrapper'):
            self._plane_options_wrapper = PlaneOptionsVal(proto_message=self._proto_message.PlaneOptions)
        return self._plane_options_wrapper
    
    @plane_options.setter
    def plane_options(self, value: PlaneOptionsVal) -> None:
        """Set the PlaneOptions field to a wrapper."""
        self._proto_message.PlaneOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_plane_options_wrapper'):
            self._plane_options_wrapper._proto_message.CopyFrom(self._proto_message.PlaneOptions)


    @property
    def show_confidence_cones(self) -> bool:
        """Get the ShowConfidenceCones field value."""
        return self._proto_message.ShowConfidenceCones
    
    @show_confidence_cones.setter
    def show_confidence_cones(self, value: bool) -> None:
        """Set the ShowConfidenceCones field value."""
        self._proto_message.ShowConfidenceCones = value


    @property
    def confidence_cone_color(self) -> ColorSurrogateVal:
        """Get the ConfidenceConeColor field as a wrapper."""
        if not hasattr(self, '_confidence_cone_color_wrapper'):
            self._confidence_cone_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.ConfidenceConeColor)
        return self._confidence_cone_color_wrapper
    
    @confidence_cone_color.setter
    def confidence_cone_color(self, value: ColorSurrogateVal) -> None:
        """Set the ConfidenceConeColor field to a wrapper."""
        self._proto_message.ConfidenceConeColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_confidence_cone_color_wrapper'):
            self._confidence_cone_color_wrapper._proto_message.CopyFrom(self._proto_message.ConfidenceConeColor)


    @property
    def show_variability_cones(self) -> bool:
        """Get the ShowVariabilityCones field value."""
        return self._proto_message.ShowVariabilityCones
    
    @show_variability_cones.setter
    def show_variability_cones(self, value: bool) -> None:
        """Set the ShowVariabilityCones field value."""
        self._proto_message.ShowVariabilityCones = value


    @property
    def variability_cone_color(self) -> ColorSurrogateVal:
        """Get the VariabilityConeColor field as a wrapper."""
        if not hasattr(self, '_variability_cone_color_wrapper'):
            self._variability_cone_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.VariabilityConeColor)
        return self._variability_cone_color_wrapper
    
    @variability_cone_color.setter
    def variability_cone_color(self, value: ColorSurrogateVal) -> None:
        """Set the VariabilityConeColor field to a wrapper."""
        self._proto_message.VariabilityConeColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_variability_cone_color_wrapper'):
            self._variability_cone_color_wrapper._proto_message.CopyFrom(self._proto_message.VariabilityConeColor)


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
