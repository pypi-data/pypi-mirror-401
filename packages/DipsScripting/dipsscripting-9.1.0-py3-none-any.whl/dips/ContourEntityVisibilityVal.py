"""Generated wrapper for ContourEntityVisibility protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ContourOptionsVal import ContourOptionsVal

class ContourEntityVisibilityVal:
    """Simple wrapper for ContourEntityVisibility with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ContourEntityVisibility


    def __init__(self, pole_vector_density_contour_options: Optional[ContourOptionsVal] = None, intersection_vector_density_contour_options: Optional[ContourOptionsVal] = None, quantitative_contour_options: Optional[ContourOptionsVal] = None, proto_message: Optional[Any] = None):
        """Initialize the ContourEntityVisibility wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if pole_vector_density_contour_options is not None:
            self._proto_message.PoleVectorDensityContourOptions.CopyFrom(pole_vector_density_contour_options.to_proto())
            self._pole_vector_density_contour_options_wrapper = pole_vector_density_contour_options
        if intersection_vector_density_contour_options is not None:
            self._proto_message.IntersectionVectorDensityContourOptions.CopyFrom(intersection_vector_density_contour_options.to_proto())
            self._intersection_vector_density_contour_options_wrapper = intersection_vector_density_contour_options
        if quantitative_contour_options is not None:
            self._proto_message.QuantitativeContourOptions.CopyFrom(quantitative_contour_options.to_proto())
            self._quantitative_contour_options_wrapper = quantitative_contour_options


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
    def contour_type(self) -> Any:
        """Get the ContourType field value."""
        return self._proto_message.ContourType
    
    @contour_type.setter
    def contour_type(self, value: Any) -> None:
        """Set the ContourType field value."""
        self._proto_message.ContourType = value


    @property
    def pole_vector_density_contour_options(self) -> ContourOptionsVal:
        """Get the PoleVectorDensityContourOptions field as a wrapper."""
        if not hasattr(self, '_pole_vector_density_contour_options_wrapper'):
            self._pole_vector_density_contour_options_wrapper = ContourOptionsVal(proto_message=self._proto_message.PoleVectorDensityContourOptions)
        return self._pole_vector_density_contour_options_wrapper
    
    @pole_vector_density_contour_options.setter
    def pole_vector_density_contour_options(self, value: ContourOptionsVal) -> None:
        """Set the PoleVectorDensityContourOptions field to a wrapper."""
        self._proto_message.PoleVectorDensityContourOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_pole_vector_density_contour_options_wrapper'):
            self._pole_vector_density_contour_options_wrapper._proto_message.CopyFrom(self._proto_message.PoleVectorDensityContourOptions)


    @property
    def intersection_vector_density_contour_options(self) -> ContourOptionsVal:
        """Get the IntersectionVectorDensityContourOptions field as a wrapper."""
        if not hasattr(self, '_intersection_vector_density_contour_options_wrapper'):
            self._intersection_vector_density_contour_options_wrapper = ContourOptionsVal(proto_message=self._proto_message.IntersectionVectorDensityContourOptions)
        return self._intersection_vector_density_contour_options_wrapper
    
    @intersection_vector_density_contour_options.setter
    def intersection_vector_density_contour_options(self, value: ContourOptionsVal) -> None:
        """Set the IntersectionVectorDensityContourOptions field to a wrapper."""
        self._proto_message.IntersectionVectorDensityContourOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_intersection_vector_density_contour_options_wrapper'):
            self._intersection_vector_density_contour_options_wrapper._proto_message.CopyFrom(self._proto_message.IntersectionVectorDensityContourOptions)


    @property
    def quantitative_contour_options(self) -> ContourOptionsVal:
        """Get the QuantitativeContourOptions field as a wrapper."""
        if not hasattr(self, '_quantitative_contour_options_wrapper'):
            self._quantitative_contour_options_wrapper = ContourOptionsVal(proto_message=self._proto_message.QuantitativeContourOptions)
        return self._quantitative_contour_options_wrapper
    
    @quantitative_contour_options.setter
    def quantitative_contour_options(self, value: ContourOptionsVal) -> None:
        """Set the QuantitativeContourOptions field to a wrapper."""
        self._proto_message.QuantitativeContourOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_quantitative_contour_options_wrapper'):
            self._quantitative_contour_options_wrapper._proto_message.CopyFrom(self._proto_message.QuantitativeContourOptions)


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
