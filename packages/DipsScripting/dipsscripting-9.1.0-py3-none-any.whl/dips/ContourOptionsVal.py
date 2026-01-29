"""Generated wrapper for ContourOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .CustomRangeVal import CustomRangeVal

class ContourOptionsVal:
    """Simple wrapper for ContourOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ContourOptions


    def __init__(self, custom_range: Optional[CustomRangeVal] = None, min_color: Optional[ColorSurrogateVal] = None, max_color: Optional[ColorSurrogateVal] = None, proto_message: Optional[Any] = None):
        """Initialize the ContourOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if custom_range is not None:
            self._proto_message.CustomRange.CopyFrom(custom_range.to_proto())
            self._custom_range_wrapper = custom_range
        if min_color is not None:
            self._proto_message.MinColor.CopyFrom(min_color.to_proto())
            self._min_color_wrapper = min_color
        if max_color is not None:
            self._proto_message.MaxColor.CopyFrom(max_color.to_proto())
            self._max_color_wrapper = max_color


    # Properties

    @property
    def custom_range(self) -> CustomRangeVal:
        """Get the CustomRange field as a wrapper."""
        if not hasattr(self, '_custom_range_wrapper'):
            self._custom_range_wrapper = CustomRangeVal(proto_message=self._proto_message.CustomRange)
        return self._custom_range_wrapper
    
    @custom_range.setter
    def custom_range(self, value: CustomRangeVal) -> None:
        """Set the CustomRange field to a wrapper."""
        self._proto_message.CustomRange.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_custom_range_wrapper'):
            self._custom_range_wrapper._proto_message.CopyFrom(self._proto_message.CustomRange)


    @property
    def intervals(self) -> int:
        """Get the Intervals field value."""
        return self._proto_message.Intervals
    
    @intervals.setter
    def intervals(self, value: int) -> None:
        """Set the Intervals field value."""
        self._proto_message.Intervals = value


    @property
    def contour_mode(self) -> Any:
        """Get the ContourMode field value."""
        return self._proto_message.ContourMode
    
    @contour_mode.setter
    def contour_mode(self, value: Any) -> None:
        """Set the ContourMode field value."""
        self._proto_message.ContourMode = value


    @property
    def min_color(self) -> ColorSurrogateVal:
        """Get the MinColor field as a wrapper."""
        if not hasattr(self, '_min_color_wrapper'):
            self._min_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.MinColor)
        return self._min_color_wrapper
    
    @min_color.setter
    def min_color(self, value: ColorSurrogateVal) -> None:
        """Set the MinColor field to a wrapper."""
        self._proto_message.MinColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_min_color_wrapper'):
            self._min_color_wrapper._proto_message.CopyFrom(self._proto_message.MinColor)


    @property
    def max_color(self) -> ColorSurrogateVal:
        """Get the MaxColor field as a wrapper."""
        if not hasattr(self, '_max_color_wrapper'):
            self._max_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.MaxColor)
        return self._max_color_wrapper
    
    @max_color.setter
    def max_color(self, value: ColorSurrogateVal) -> None:
        """Set the MaxColor field to a wrapper."""
        self._proto_message.MaxColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_max_color_wrapper'):
            self._max_color_wrapper._proto_message.CopyFrom(self._proto_message.MaxColor)


    @property
    def color_interpolation_method(self) -> Any:
        """Get the ColorInterpolationMethod field value."""
        return self._proto_message.ColorInterpolationMethod
    
    @color_interpolation_method.setter
    def color_interpolation_method(self, value: Any) -> None:
        """Set the ColorInterpolationMethod field value."""
        self._proto_message.ColorInterpolationMethod = value


    @property
    def fill_below_minimum(self) -> bool:
        """Get the FillBelowMinimum field value."""
        return self._proto_message.FillBelowMinimum
    
    @fill_below_minimum.setter
    def fill_below_minimum(self, value: bool) -> None:
        """Set the FillBelowMinimum field value."""
        self._proto_message.FillBelowMinimum = value


    @property
    def fill_above_maximum(self) -> bool:
        """Get the FillAboveMaximum field value."""
        return self._proto_message.FillAboveMaximum
    
    @fill_above_maximum.setter
    def fill_above_maximum(self, value: bool) -> None:
        """Set the FillAboveMaximum field value."""
        self._proto_message.FillAboveMaximum = value


    @property
    def custom_colors(self) -> List[ColorSurrogateVal]:
        """Get the CustomColors field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.CustomColors, ColorSurrogateVal)
    
    @custom_colors.setter
    def custom_colors(self, value: List[ColorSurrogateVal]) -> None:
        """Set the CustomColors field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.CustomColors[:] = []
        for item in value:
            self._proto_message.CustomColors.append(item.to_proto())


    @property
    def contour_color_table_method(self) -> Any:
        """Get the ContourColorTableMethod field value."""
        return self._proto_message.ContourColorTableMethod
    
    @contour_color_table_method.setter
    def contour_color_table_method(self, value: Any) -> None:
        """Set the ContourColorTableMethod field value."""
        self._proto_message.ContourColorTableMethod = value


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
