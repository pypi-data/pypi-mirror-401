"""Generated wrapper for CustomHistogramOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .CustomRangeVal import CustomRangeVal
from .StatisticalDistributionFilterVal import StatisticalDistributionFilterVal

class CustomHistogramOptionsVal:
    """Simple wrapper for CustomHistogramOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CustomHistogramOptions


    def __init__(self, custom_range: Optional[CustomRangeVal] = None, distribution_filter: Optional[StatisticalDistributionFilterVal] = None, proto_message: Optional[Any] = None):
        """Initialize the CustomHistogramOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if custom_range is not None:
            self._proto_message.CustomRange.CopyFrom(custom_range.to_proto())
            self._custom_range_wrapper = custom_range
        if distribution_filter is not None:
            self._proto_message.DistributionFilter.CopyFrom(distribution_filter.to_proto())
            self._distribution_filter_wrapper = distribution_filter


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
    def apply_distribution_filter(self) -> bool:
        """Get the ApplyDistributionFilter field value."""
        return self._proto_message.ApplyDistributionFilter
    
    @apply_distribution_filter.setter
    def apply_distribution_filter(self, value: bool) -> None:
        """Set the ApplyDistributionFilter field value."""
        self._proto_message.ApplyDistributionFilter = value


    @property
    def distribution_filter(self) -> StatisticalDistributionFilterVal:
        """Get the DistributionFilter field as a wrapper."""
        if not hasattr(self, '_distribution_filter_wrapper'):
            self._distribution_filter_wrapper = StatisticalDistributionFilterVal(proto_message=self._proto_message.DistributionFilter)
        return self._distribution_filter_wrapper
    
    @distribution_filter.setter
    def distribution_filter(self, value: StatisticalDistributionFilterVal) -> None:
        """Set the DistributionFilter field to a wrapper."""
        self._proto_message.DistributionFilter.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_distribution_filter_wrapper'):
            self._distribution_filter_wrapper._proto_message.CopyFrom(self._proto_message.DistributionFilter)


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
