"""Generated wrapper for Stereonet2DPresetOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ContourEntityVisibilityVal import ContourEntityVisibilityVal
from .GlobalPlaneEntityVisibilityVal import GlobalPlaneEntityVisibilityVal
from .IntersectionEntityVisibilityVal import IntersectionEntityVisibilityVal
from .KinematicAnalysisEntityVisibilityVal import KinematicAnalysisEntityVisibilityVal
from .PoleEntityVisibilityVal import PoleEntityVisibilityVal
from .StereonetOverlayEntityVisibilityVal import StereonetOverlayEntityVisibilityVal

class Stereonet2DPresetOptionsVal:
    """Simple wrapper for Stereonet2DPresetOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Stereonet2DPresetOptions


    def __init__(self, pole_entity_visibility: Optional[PoleEntityVisibilityVal] = None, intersection_entity_visibility: Optional[IntersectionEntityVisibilityVal] = None, contour_entity_visibility: Optional[ContourEntityVisibilityVal] = None, global_mean_plane_entity_visibility: Optional[GlobalPlaneEntityVisibilityVal] = None, global_best_fit_plane_entity_visibility: Optional[GlobalPlaneEntityVisibilityVal] = None, kinematic_analysis_entity_visibility: Optional[KinematicAnalysisEntityVisibilityVal] = None, stereonet_overlay_entity_visibility: Optional[StereonetOverlayEntityVisibilityVal] = None, proto_message: Optional[Any] = None):
        """Initialize the Stereonet2DPresetOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if pole_entity_visibility is not None:
            self._proto_message.PoleEntityVisibility.CopyFrom(pole_entity_visibility.to_proto())
            self._pole_entity_visibility_wrapper = pole_entity_visibility
        if intersection_entity_visibility is not None:
            self._proto_message.IntersectionEntityVisibility.CopyFrom(intersection_entity_visibility.to_proto())
            self._intersection_entity_visibility_wrapper = intersection_entity_visibility
        if contour_entity_visibility is not None:
            self._proto_message.ContourEntityVisibility.CopyFrom(contour_entity_visibility.to_proto())
            self._contour_entity_visibility_wrapper = contour_entity_visibility
        if global_mean_plane_entity_visibility is not None:
            self._proto_message.GlobalMeanPlaneEntityVisibility.CopyFrom(global_mean_plane_entity_visibility.to_proto())
            self._global_mean_plane_entity_visibility_wrapper = global_mean_plane_entity_visibility
        if global_best_fit_plane_entity_visibility is not None:
            self._proto_message.GlobalBestFitPlaneEntityVisibility.CopyFrom(global_best_fit_plane_entity_visibility.to_proto())
            self._global_best_fit_plane_entity_visibility_wrapper = global_best_fit_plane_entity_visibility
        if kinematic_analysis_entity_visibility is not None:
            self._proto_message.KinematicAnalysisEntityVisibility.CopyFrom(kinematic_analysis_entity_visibility.to_proto())
            self._kinematic_analysis_entity_visibility_wrapper = kinematic_analysis_entity_visibility
        if stereonet_overlay_entity_visibility is not None:
            self._proto_message.StereonetOverlayEntityVisibility.CopyFrom(stereonet_overlay_entity_visibility.to_proto())
            self._stereonet_overlay_entity_visibility_wrapper = stereonet_overlay_entity_visibility


    # Properties

    @property
    def pole_entity_visibility(self) -> PoleEntityVisibilityVal:
        """Get the PoleEntityVisibility field as a wrapper."""
        if not hasattr(self, '_pole_entity_visibility_wrapper'):
            self._pole_entity_visibility_wrapper = PoleEntityVisibilityVal(proto_message=self._proto_message.PoleEntityVisibility)
        return self._pole_entity_visibility_wrapper
    
    @pole_entity_visibility.setter
    def pole_entity_visibility(self, value: PoleEntityVisibilityVal) -> None:
        """Set the PoleEntityVisibility field to a wrapper."""
        self._proto_message.PoleEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_pole_entity_visibility_wrapper'):
            self._pole_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.PoleEntityVisibility)


    @property
    def intersection_entity_visibility(self) -> IntersectionEntityVisibilityVal:
        """Get the IntersectionEntityVisibility field as a wrapper."""
        if not hasattr(self, '_intersection_entity_visibility_wrapper'):
            self._intersection_entity_visibility_wrapper = IntersectionEntityVisibilityVal(proto_message=self._proto_message.IntersectionEntityVisibility)
        return self._intersection_entity_visibility_wrapper
    
    @intersection_entity_visibility.setter
    def intersection_entity_visibility(self, value: IntersectionEntityVisibilityVal) -> None:
        """Set the IntersectionEntityVisibility field to a wrapper."""
        self._proto_message.IntersectionEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_intersection_entity_visibility_wrapper'):
            self._intersection_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.IntersectionEntityVisibility)


    @property
    def contour_entity_visibility(self) -> ContourEntityVisibilityVal:
        """Get the ContourEntityVisibility field as a wrapper."""
        if not hasattr(self, '_contour_entity_visibility_wrapper'):
            self._contour_entity_visibility_wrapper = ContourEntityVisibilityVal(proto_message=self._proto_message.ContourEntityVisibility)
        return self._contour_entity_visibility_wrapper
    
    @contour_entity_visibility.setter
    def contour_entity_visibility(self, value: ContourEntityVisibilityVal) -> None:
        """Set the ContourEntityVisibility field to a wrapper."""
        self._proto_message.ContourEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_contour_entity_visibility_wrapper'):
            self._contour_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.ContourEntityVisibility)


    @property
    def set_window_entity_group_visibility(self) -> bool:
        """Get the SetWindowEntityGroupVisibility field value."""
        return self._proto_message.SetWindowEntityGroupVisibility
    
    @set_window_entity_group_visibility.setter
    def set_window_entity_group_visibility(self, value: bool) -> None:
        """Set the SetWindowEntityGroupVisibility field value."""
        self._proto_message.SetWindowEntityGroupVisibility = value


    @property
    def mean_set_plane_entity_group_visibility(self) -> bool:
        """Get the MeanSetPlaneEntityGroupVisibility field value."""
        return self._proto_message.MeanSetPlaneEntityGroupVisibility
    
    @mean_set_plane_entity_group_visibility.setter
    def mean_set_plane_entity_group_visibility(self, value: bool) -> None:
        """Set the MeanSetPlaneEntityGroupVisibility field value."""
        self._proto_message.MeanSetPlaneEntityGroupVisibility = value


    @property
    def user_plane_entity_group_visibility(self) -> bool:
        """Get the UserPlaneEntityGroupVisibility field value."""
        return self._proto_message.UserPlaneEntityGroupVisibility
    
    @user_plane_entity_group_visibility.setter
    def user_plane_entity_group_visibility(self, value: bool) -> None:
        """Set the UserPlaneEntityGroupVisibility field value."""
        self._proto_message.UserPlaneEntityGroupVisibility = value


    @property
    def traverse_entity_group_visibility(self) -> bool:
        """Get the TraverseEntityGroupVisibility field value."""
        return self._proto_message.TraverseEntityGroupVisibility
    
    @traverse_entity_group_visibility.setter
    def traverse_entity_group_visibility(self, value: bool) -> None:
        """Set the TraverseEntityGroupVisibility field value."""
        self._proto_message.TraverseEntityGroupVisibility = value


    @property
    def fold_window_entity_group_visibility(self) -> bool:
        """Get the FoldWindowEntityGroupVisibility field value."""
        return self._proto_message.FoldWindowEntityGroupVisibility
    
    @fold_window_entity_group_visibility.setter
    def fold_window_entity_group_visibility(self, value: bool) -> None:
        """Set the FoldWindowEntityGroupVisibility field value."""
        self._proto_message.FoldWindowEntityGroupVisibility = value


    @property
    def fold_entity_group_visibility(self) -> bool:
        """Get the FoldEntityGroupVisibility field value."""
        return self._proto_message.FoldEntityGroupVisibility
    
    @fold_entity_group_visibility.setter
    def fold_entity_group_visibility(self, value: bool) -> None:
        """Set the FoldEntityGroupVisibility field value."""
        self._proto_message.FoldEntityGroupVisibility = value


    @property
    def global_mean_plane_entity_visibility(self) -> GlobalPlaneEntityVisibilityVal:
        """Get the GlobalMeanPlaneEntityVisibility field as a wrapper."""
        if not hasattr(self, '_global_mean_plane_entity_visibility_wrapper'):
            self._global_mean_plane_entity_visibility_wrapper = GlobalPlaneEntityVisibilityVal(proto_message=self._proto_message.GlobalMeanPlaneEntityVisibility)
        return self._global_mean_plane_entity_visibility_wrapper
    
    @global_mean_plane_entity_visibility.setter
    def global_mean_plane_entity_visibility(self, value: GlobalPlaneEntityVisibilityVal) -> None:
        """Set the GlobalMeanPlaneEntityVisibility field to a wrapper."""
        self._proto_message.GlobalMeanPlaneEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_global_mean_plane_entity_visibility_wrapper'):
            self._global_mean_plane_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.GlobalMeanPlaneEntityVisibility)


    @property
    def global_best_fit_plane_entity_visibility(self) -> GlobalPlaneEntityVisibilityVal:
        """Get the GlobalBestFitPlaneEntityVisibility field as a wrapper."""
        if not hasattr(self, '_global_best_fit_plane_entity_visibility_wrapper'):
            self._global_best_fit_plane_entity_visibility_wrapper = GlobalPlaneEntityVisibilityVal(proto_message=self._proto_message.GlobalBestFitPlaneEntityVisibility)
        return self._global_best_fit_plane_entity_visibility_wrapper
    
    @global_best_fit_plane_entity_visibility.setter
    def global_best_fit_plane_entity_visibility(self, value: GlobalPlaneEntityVisibilityVal) -> None:
        """Set the GlobalBestFitPlaneEntityVisibility field to a wrapper."""
        self._proto_message.GlobalBestFitPlaneEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_global_best_fit_plane_entity_visibility_wrapper'):
            self._global_best_fit_plane_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.GlobalBestFitPlaneEntityVisibility)


    @property
    def kinematic_analysis_entity_visibility(self) -> KinematicAnalysisEntityVisibilityVal:
        """Get the KinematicAnalysisEntityVisibility field as a wrapper."""
        if not hasattr(self, '_kinematic_analysis_entity_visibility_wrapper'):
            self._kinematic_analysis_entity_visibility_wrapper = KinematicAnalysisEntityVisibilityVal(proto_message=self._proto_message.KinematicAnalysisEntityVisibility)
        return self._kinematic_analysis_entity_visibility_wrapper
    
    @kinematic_analysis_entity_visibility.setter
    def kinematic_analysis_entity_visibility(self, value: KinematicAnalysisEntityVisibilityVal) -> None:
        """Set the KinematicAnalysisEntityVisibility field to a wrapper."""
        self._proto_message.KinematicAnalysisEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_kinematic_analysis_entity_visibility_wrapper'):
            self._kinematic_analysis_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.KinematicAnalysisEntityVisibility)


    @property
    def stereonet_overlay_entity_visibility(self) -> StereonetOverlayEntityVisibilityVal:
        """Get the StereonetOverlayEntityVisibility field as a wrapper."""
        if not hasattr(self, '_stereonet_overlay_entity_visibility_wrapper'):
            self._stereonet_overlay_entity_visibility_wrapper = StereonetOverlayEntityVisibilityVal(proto_message=self._proto_message.StereonetOverlayEntityVisibility)
        return self._stereonet_overlay_entity_visibility_wrapper
    
    @stereonet_overlay_entity_visibility.setter
    def stereonet_overlay_entity_visibility(self, value: StereonetOverlayEntityVisibilityVal) -> None:
        """Set the StereonetOverlayEntityVisibility field to a wrapper."""
        self._proto_message.StereonetOverlayEntityVisibility.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_stereonet_overlay_entity_visibility_wrapper'):
            self._stereonet_overlay_entity_visibility_wrapper._proto_message.CopyFrom(self._proto_message.StereonetOverlayEntityVisibility)


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


    @property
    def show_major_planes_legend(self) -> bool:
        """Get the ShowMajorPlanesLegend field value."""
        return self._proto_message.ShowMajorPlanesLegend
    
    @show_major_planes_legend.setter
    def show_major_planes_legend(self, value: bool) -> None:
        """Set the ShowMajorPlanesLegend field value."""
        self._proto_message.ShowMajorPlanesLegend = value


    @property
    def show_major_intersections_legend(self) -> bool:
        """Get the ShowMajorIntersectionsLegend field value."""
        return self._proto_message.ShowMajorIntersectionsLegend
    
    @show_major_intersections_legend.setter
    def show_major_intersections_legend(self, value: bool) -> None:
        """Set the ShowMajorIntersectionsLegend field value."""
        self._proto_message.ShowMajorIntersectionsLegend = value


    @property
    def show_kinematic_analysis_legend(self) -> bool:
        """Get the ShowKinematicAnalysisLegend field value."""
        return self._proto_message.ShowKinematicAnalysisLegend
    
    @show_kinematic_analysis_legend.setter
    def show_kinematic_analysis_legend(self, value: bool) -> None:
        """Set the ShowKinematicAnalysisLegend field value."""
        self._proto_message.ShowKinematicAnalysisLegend = value


    @property
    def show_properties_legend(self) -> bool:
        """Get the ShowPropertiesLegend field value."""
        return self._proto_message.ShowPropertiesLegend
    
    @show_properties_legend.setter
    def show_properties_legend(self, value: bool) -> None:
        """Set the ShowPropertiesLegend field value."""
        self._proto_message.ShowPropertiesLegend = value


    @property
    def show_symbols_legend(self) -> bool:
        """Get the ShowSymbolsLegend field value."""
        return self._proto_message.ShowSymbolsLegend
    
    @show_symbols_legend.setter
    def show_symbols_legend(self, value: bool) -> None:
        """Set the ShowSymbolsLegend field value."""
        self._proto_message.ShowSymbolsLegend = value


    @property
    def show_contours_legend(self) -> bool:
        """Get the ShowContoursLegend field value."""
        return self._proto_message.ShowContoursLegend
    
    @show_contours_legend.setter
    def show_contours_legend(self, value: bool) -> None:
        """Set the ShowContoursLegend field value."""
        self._proto_message.ShowContoursLegend = value


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
