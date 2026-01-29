"""Generated wrapper for Stereonet3DPresetOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ContourEntityVisibilityVal import ContourEntityVisibilityVal
from .GlobalPlaneEntityVisibilityVal import GlobalPlaneEntityVisibilityVal
from .IntersectionEntityVisibilityVal import IntersectionEntityVisibilityVal
from .PoleEntityVisibilityVal import PoleEntityVisibilityVal
from .StereonetOverlayEntityVisibilityVal import StereonetOverlayEntityVisibilityVal

class Stereonet3DPresetOptionsVal:
    """Simple wrapper for Stereonet3DPresetOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Stereonet3DPresetOptions


    def __init__(self, pole_entity_visibility: Optional[PoleEntityVisibilityVal] = None, intersection_entity_visibility: Optional[IntersectionEntityVisibilityVal] = None, contour_entity_visibility: Optional[ContourEntityVisibilityVal] = None, global_mean_plane_entity_visibility: Optional[GlobalPlaneEntityVisibilityVal] = None, global_best_fit_plane_entity_visibility: Optional[GlobalPlaneEntityVisibilityVal] = None, stereonet_overlay_entity_visibility: Optional[StereonetOverlayEntityVisibilityVal] = None, proto_message: Optional[Any] = None):
        """Initialize the Stereonet3DPresetOptions wrapper."""
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
    def show_legend(self) -> bool:
        """Get the ShowLegend field value."""
        return self._proto_message.ShowLegend
    
    @show_legend.setter
    def show_legend(self, value: bool) -> None:
        """Set the ShowLegend field value."""
        self._proto_message.ShowLegend = value


    @property
    def show_properties_legend(self) -> bool:
        """Get the ShowPropertiesLegend field value."""
        return self._proto_message.ShowPropertiesLegend
    
    @show_properties_legend.setter
    def show_properties_legend(self, value: bool) -> None:
        """Set the ShowPropertiesLegend field value."""
        self._proto_message.ShowPropertiesLegend = value


    @property
    def show_contours_legend(self) -> bool:
        """Get the ShowContoursLegend field value."""
        return self._proto_message.ShowContoursLegend
    
    @show_contours_legend.setter
    def show_contours_legend(self, value: bool) -> None:
        """Set the ShowContoursLegend field value."""
        self._proto_message.ShowContoursLegend = value


    @property
    def show_major_planes_legend(self) -> bool:
        """Get the ShowMajorPlanesLegend field value."""
        return self._proto_message.ShowMajorPlanesLegend
    
    @show_major_planes_legend.setter
    def show_major_planes_legend(self, value: bool) -> None:
        """Set the ShowMajorPlanesLegend field value."""
        self._proto_message.ShowMajorPlanesLegend = value


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
