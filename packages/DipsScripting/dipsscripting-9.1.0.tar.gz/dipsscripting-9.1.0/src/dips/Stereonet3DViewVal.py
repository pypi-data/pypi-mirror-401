"""Generated wrapper for Stereonet3DView protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .FoldEntityVisibilityVal import FoldEntityVisibilityVal
from .FoldWindowEntityVisibilityVal import FoldWindowEntityVisibilityVal
from .PlaneEntityVisibilityVal import PlaneEntityVisibilityVal
from .QuantitativeContourSettingsVal import QuantitativeContourSettingsVal
from .SetEntityVisibilityVal import SetEntityVisibilityVal
from .SetWindowEntityVisibilityVal import SetWindowEntityVisibilityVal
from .Stereonet3DPresetOptionsVal import Stereonet3DPresetOptionsVal
from .SymbolicSettingsVal import SymbolicSettingsVal
from .TraverseEntityVisibilityVal import TraverseEntityVisibilityVal
from .VectorDensityContourSettingsVal import VectorDensityContourSettingsVal
from .DataFilterRef import DataFilterRef

class Stereonet3DViewVal:
    """Simple wrapper for Stereonet3DView with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Stereonet3DView


    def __init__(self, symbolic_settings: Optional[SymbolicSettingsVal] = None, pole_vector_density_contour_settings: Optional[VectorDensityContourSettingsVal] = None, intersection_vector_density_contour_settings: Optional[VectorDensityContourSettingsVal] = None, quantitative_contour_settings: Optional[QuantitativeContourSettingsVal] = None, preset_options: Optional[Stereonet3DPresetOptionsVal] = None, active_filter: Optional[DataFilterRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the Stereonet3DView wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if symbolic_settings is not None:
            self._proto_message.SymbolicSettings.CopyFrom(symbolic_settings.to_proto())
            self._symbolic_settings_wrapper = symbolic_settings
        if pole_vector_density_contour_settings is not None:
            self._proto_message.PoleVectorDensityContourSettings.CopyFrom(pole_vector_density_contour_settings.to_proto())
            self._pole_vector_density_contour_settings_wrapper = pole_vector_density_contour_settings
        if intersection_vector_density_contour_settings is not None:
            self._proto_message.IntersectionVectorDensityContourSettings.CopyFrom(intersection_vector_density_contour_settings.to_proto())
            self._intersection_vector_density_contour_settings_wrapper = intersection_vector_density_contour_settings
        if quantitative_contour_settings is not None:
            self._proto_message.QuantitativeContourSettings.CopyFrom(quantitative_contour_settings.to_proto())
            self._quantitative_contour_settings_wrapper = quantitative_contour_settings
        if preset_options is not None:
            self._proto_message.PresetOptions.CopyFrom(preset_options.to_proto())
            self._preset_options_wrapper = preset_options
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
    def vector_mode(self) -> Any:
        """Get the VectorMode field value."""
        return self._proto_message.VectorMode
    
    @vector_mode.setter
    def vector_mode(self, value: Any) -> None:
        """Set the VectorMode field value."""
        self._proto_message.VectorMode = value


    @property
    def is_weighted(self) -> bool:
        """Get the IsWeighted field value."""
        return self._proto_message.IsWeighted
    
    @is_weighted.setter
    def is_weighted(self, value: bool) -> None:
        """Set the IsWeighted field value."""
        self._proto_message.IsWeighted = value


    @property
    def symbolic_settings(self) -> SymbolicSettingsVal:
        """Get the SymbolicSettings field as a wrapper."""
        if not hasattr(self, '_symbolic_settings_wrapper'):
            self._symbolic_settings_wrapper = SymbolicSettingsVal(proto_message=self._proto_message.SymbolicSettings)
        return self._symbolic_settings_wrapper
    
    @symbolic_settings.setter
    def symbolic_settings(self, value: SymbolicSettingsVal) -> None:
        """Set the SymbolicSettings field to a wrapper."""
        self._proto_message.SymbolicSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_symbolic_settings_wrapper'):
            self._symbolic_settings_wrapper._proto_message.CopyFrom(self._proto_message.SymbolicSettings)


    @property
    def pole_vector_density_contour_settings(self) -> VectorDensityContourSettingsVal:
        """Get the PoleVectorDensityContourSettings field as a wrapper."""
        if not hasattr(self, '_pole_vector_density_contour_settings_wrapper'):
            self._pole_vector_density_contour_settings_wrapper = VectorDensityContourSettingsVal(proto_message=self._proto_message.PoleVectorDensityContourSettings)
        return self._pole_vector_density_contour_settings_wrapper
    
    @pole_vector_density_contour_settings.setter
    def pole_vector_density_contour_settings(self, value: VectorDensityContourSettingsVal) -> None:
        """Set the PoleVectorDensityContourSettings field to a wrapper."""
        self._proto_message.PoleVectorDensityContourSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_pole_vector_density_contour_settings_wrapper'):
            self._pole_vector_density_contour_settings_wrapper._proto_message.CopyFrom(self._proto_message.PoleVectorDensityContourSettings)


    @property
    def intersection_vector_density_contour_settings(self) -> VectorDensityContourSettingsVal:
        """Get the IntersectionVectorDensityContourSettings field as a wrapper."""
        if not hasattr(self, '_intersection_vector_density_contour_settings_wrapper'):
            self._intersection_vector_density_contour_settings_wrapper = VectorDensityContourSettingsVal(proto_message=self._proto_message.IntersectionVectorDensityContourSettings)
        return self._intersection_vector_density_contour_settings_wrapper
    
    @intersection_vector_density_contour_settings.setter
    def intersection_vector_density_contour_settings(self, value: VectorDensityContourSettingsVal) -> None:
        """Set the IntersectionVectorDensityContourSettings field to a wrapper."""
        self._proto_message.IntersectionVectorDensityContourSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_intersection_vector_density_contour_settings_wrapper'):
            self._intersection_vector_density_contour_settings_wrapper._proto_message.CopyFrom(self._proto_message.IntersectionVectorDensityContourSettings)


    @property
    def quantitative_contour_settings(self) -> QuantitativeContourSettingsVal:
        """Get the QuantitativeContourSettings field as a wrapper."""
        if not hasattr(self, '_quantitative_contour_settings_wrapper'):
            self._quantitative_contour_settings_wrapper = QuantitativeContourSettingsVal(proto_message=self._proto_message.QuantitativeContourSettings)
        return self._quantitative_contour_settings_wrapper
    
    @quantitative_contour_settings.setter
    def quantitative_contour_settings(self, value: QuantitativeContourSettingsVal) -> None:
        """Set the QuantitativeContourSettings field to a wrapper."""
        self._proto_message.QuantitativeContourSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_quantitative_contour_settings_wrapper'):
            self._quantitative_contour_settings_wrapper._proto_message.CopyFrom(self._proto_message.QuantitativeContourSettings)


    @property
    def preset_options(self) -> Stereonet3DPresetOptionsVal:
        """Get the PresetOptions field as a wrapper."""
        if not hasattr(self, '_preset_options_wrapper'):
            self._preset_options_wrapper = Stereonet3DPresetOptionsVal(proto_message=self._proto_message.PresetOptions)
        return self._preset_options_wrapper
    
    @preset_options.setter
    def preset_options(self, value: Stereonet3DPresetOptionsVal) -> None:
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
    def traverse_entity_visibilities(self) -> List[TraverseEntityVisibilityVal]:
        """Get the TraverseEntityVisibilities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.TraverseEntityVisibilities, TraverseEntityVisibilityVal)
    
    @traverse_entity_visibilities.setter
    def traverse_entity_visibilities(self, value: List[TraverseEntityVisibilityVal]) -> None:
        """Set the TraverseEntityVisibilities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.TraverseEntityVisibilities[:] = []
        for item in value:
            self._proto_message.TraverseEntityVisibilities.append(item.to_proto())


    @property
    def active_filter(self) -> DataFilterRef:
        """Get the ActiveFilter field as a reference."""
        return DataFilterRef(self.__channelToConnectOn, self._proto_message.ActiveFilter)
    
    @active_filter.setter
    def active_filter(self, value: DataFilterRef) -> None:
        """Set the ActiveFilter field to a reference."""
        self._proto_message.ActiveFilter.CopyFrom(value.get_model_ref())


    @property
    def set_window_entity_visibilities(self) -> List[SetWindowEntityVisibilityVal]:
        """Get the SetWindowEntityVisibilities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.SetWindowEntityVisibilities, SetWindowEntityVisibilityVal)
    
    @set_window_entity_visibilities.setter
    def set_window_entity_visibilities(self, value: List[SetWindowEntityVisibilityVal]) -> None:
        """Set the SetWindowEntityVisibilities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.SetWindowEntityVisibilities[:] = []
        for item in value:
            self._proto_message.SetWindowEntityVisibilities.append(item.to_proto())


    @property
    def mean_set_plane_entity_visibilities(self) -> List[SetEntityVisibilityVal]:
        """Get the MeanSetPlaneEntityVisibilities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.MeanSetPlaneEntityVisibilities, SetEntityVisibilityVal)
    
    @mean_set_plane_entity_visibilities.setter
    def mean_set_plane_entity_visibilities(self, value: List[SetEntityVisibilityVal]) -> None:
        """Set the MeanSetPlaneEntityVisibilities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.MeanSetPlaneEntityVisibilities[:] = []
        for item in value:
            self._proto_message.MeanSetPlaneEntityVisibilities.append(item.to_proto())


    @property
    def fold_window_entity_visibilities(self) -> List[FoldWindowEntityVisibilityVal]:
        """Get the FoldWindowEntityVisibilities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.FoldWindowEntityVisibilities, FoldWindowEntityVisibilityVal)
    
    @fold_window_entity_visibilities.setter
    def fold_window_entity_visibilities(self, value: List[FoldWindowEntityVisibilityVal]) -> None:
        """Set the FoldWindowEntityVisibilities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.FoldWindowEntityVisibilities[:] = []
        for item in value:
            self._proto_message.FoldWindowEntityVisibilities.append(item.to_proto())


    @property
    def fold_entity_visibilities(self) -> List[FoldEntityVisibilityVal]:
        """Get the FoldEntityVisibilities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.FoldEntityVisibilities, FoldEntityVisibilityVal)
    
    @fold_entity_visibilities.setter
    def fold_entity_visibilities(self, value: List[FoldEntityVisibilityVal]) -> None:
        """Set the FoldEntityVisibilities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.FoldEntityVisibilities[:] = []
        for item in value:
            self._proto_message.FoldEntityVisibilities.append(item.to_proto())


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
