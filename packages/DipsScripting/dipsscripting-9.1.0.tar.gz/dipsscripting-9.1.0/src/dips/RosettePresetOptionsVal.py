"""Generated wrapper for RosettePresetOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class RosettePresetOptionsVal:
    """Simple wrapper for RosettePresetOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.RosettePresetOptions


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the RosettePresetOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def user_plane_entity_group_visibility(self) -> bool:
        """Get the UserPlaneEntityGroupVisibility field value."""
        return self._proto_message.UserPlaneEntityGroupVisibility
    
    @user_plane_entity_group_visibility.setter
    def user_plane_entity_group_visibility(self, value: bool) -> None:
        """Set the UserPlaneEntityGroupVisibility field value."""
        self._proto_message.UserPlaneEntityGroupVisibility = value


    @property
    def tools_entity_group_visibility(self) -> bool:
        """Get the ToolsEntityGroupVisibility field value."""
        return self._proto_message.ToolsEntityGroupVisibility
    
    @tools_entity_group_visibility.setter
    def tools_entity_group_visibility(self, value: bool) -> None:
        """Set the ToolsEntityGroupVisibility field value."""
        self._proto_message.ToolsEntityGroupVisibility = value


    @property
    def text_tool_entity_group_visibility(self) -> bool:
        """Get the TextToolEntityGroupVisibility field value."""
        return self._proto_message.TextToolEntityGroupVisibility
    
    @text_tool_entity_group_visibility.setter
    def text_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the TextToolEntityGroupVisibility field value."""
        self._proto_message.TextToolEntityGroupVisibility = value


    @property
    def arrow_tool_entity_group_visibility(self) -> bool:
        """Get the ArrowToolEntityGroupVisibility field value."""
        return self._proto_message.ArrowToolEntityGroupVisibility
    
    @arrow_tool_entity_group_visibility.setter
    def arrow_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the ArrowToolEntityGroupVisibility field value."""
        self._proto_message.ArrowToolEntityGroupVisibility = value


    @property
    def line_tool_entity_group_visibility(self) -> bool:
        """Get the LineToolEntityGroupVisibility field value."""
        return self._proto_message.LineToolEntityGroupVisibility
    
    @line_tool_entity_group_visibility.setter
    def line_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the LineToolEntityGroupVisibility field value."""
        self._proto_message.LineToolEntityGroupVisibility = value


    @property
    def polyline_tool_entity_group_visibility(self) -> bool:
        """Get the PolylineToolEntityGroupVisibility field value."""
        return self._proto_message.PolylineToolEntityGroupVisibility
    
    @polyline_tool_entity_group_visibility.setter
    def polyline_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the PolylineToolEntityGroupVisibility field value."""
        self._proto_message.PolylineToolEntityGroupVisibility = value


    @property
    def polygon_tool_entity_group_visibility(self) -> bool:
        """Get the PolygonToolEntityGroupVisibility field value."""
        return self._proto_message.PolygonToolEntityGroupVisibility
    
    @polygon_tool_entity_group_visibility.setter
    def polygon_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the PolygonToolEntityGroupVisibility field value."""
        self._proto_message.PolygonToolEntityGroupVisibility = value


    @property
    def rectangle_tool_entity_group_visibility(self) -> bool:
        """Get the RectangleToolEntityGroupVisibility field value."""
        return self._proto_message.RectangleToolEntityGroupVisibility
    
    @rectangle_tool_entity_group_visibility.setter
    def rectangle_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the RectangleToolEntityGroupVisibility field value."""
        self._proto_message.RectangleToolEntityGroupVisibility = value


    @property
    def ellipse_tool_entity_group_visibility(self) -> bool:
        """Get the EllipseToolEntityGroupVisibility field value."""
        return self._proto_message.EllipseToolEntityGroupVisibility
    
    @ellipse_tool_entity_group_visibility.setter
    def ellipse_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the EllipseToolEntityGroupVisibility field value."""
        self._proto_message.EllipseToolEntityGroupVisibility = value


    @property
    def cone_tool_entity_group_visibility(self) -> bool:
        """Get the ConeToolEntityGroupVisibility field value."""
        return self._proto_message.ConeToolEntityGroupVisibility
    
    @cone_tool_entity_group_visibility.setter
    def cone_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the ConeToolEntityGroupVisibility field value."""
        self._proto_message.ConeToolEntityGroupVisibility = value


    @property
    def trend_line_tool_entity_group_visibility(self) -> bool:
        """Get the TrendLineToolEntityGroupVisibility field value."""
        return self._proto_message.TrendLineToolEntityGroupVisibility
    
    @trend_line_tool_entity_group_visibility.setter
    def trend_line_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the TrendLineToolEntityGroupVisibility field value."""
        self._proto_message.TrendLineToolEntityGroupVisibility = value


    @property
    def pitch_grid_tool_entity_group_visibility(self) -> bool:
        """Get the PitchGridToolEntityGroupVisibility field value."""
        return self._proto_message.PitchGridToolEntityGroupVisibility
    
    @pitch_grid_tool_entity_group_visibility.setter
    def pitch_grid_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the PitchGridToolEntityGroupVisibility field value."""
        self._proto_message.PitchGridToolEntityGroupVisibility = value


    @property
    def measure_angle_tool_entity_group_visibility(self) -> bool:
        """Get the MeasureAngleToolEntityGroupVisibility field value."""
        return self._proto_message.MeasureAngleToolEntityGroupVisibility
    
    @measure_angle_tool_entity_group_visibility.setter
    def measure_angle_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the MeasureAngleToolEntityGroupVisibility field value."""
        self._proto_message.MeasureAngleToolEntityGroupVisibility = value


    @property
    def line_intersection_calculator_tool_entity_group_visibility(self) -> bool:
        """Get the LineIntersectionCalculatorToolEntityGroupVisibility field value."""
        return self._proto_message.LineIntersectionCalculatorToolEntityGroupVisibility
    
    @line_intersection_calculator_tool_entity_group_visibility.setter
    def line_intersection_calculator_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the LineIntersectionCalculatorToolEntityGroupVisibility field value."""
        self._proto_message.LineIntersectionCalculatorToolEntityGroupVisibility = value


    @property
    def plane_intersection_calculator_tool_entity_group_visibility(self) -> bool:
        """Get the PlaneIntersectionCalculatorToolEntityGroupVisibility field value."""
        return self._proto_message.PlaneIntersectionCalculatorToolEntityGroupVisibility
    
    @plane_intersection_calculator_tool_entity_group_visibility.setter
    def plane_intersection_calculator_tool_entity_group_visibility(self, value: bool) -> None:
        """Set the PlaneIntersectionCalculatorToolEntityGroupVisibility field value."""
        self._proto_message.PlaneIntersectionCalculatorToolEntityGroupVisibility = value


    @property
    def show_legend(self) -> bool:
        """Get the ShowLegend field value."""
        return self._proto_message.ShowLegend
    
    @show_legend.setter
    def show_legend(self, value: bool) -> None:
        """Set the ShowLegend field value."""
        self._proto_message.ShowLegend = value


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
