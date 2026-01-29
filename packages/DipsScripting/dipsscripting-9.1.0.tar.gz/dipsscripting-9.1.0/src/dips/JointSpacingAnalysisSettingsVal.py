"""Generated wrapper for JointSpacingAnalysisSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .CustomHistogramOptionsVal import CustomHistogramOptionsVal
from .OrientationDataSetRef import OrientationDataSetRef
from .SetEntityInfoRef import SetEntityInfoRef

class JointSpacingAnalysisSettingsVal:
    """Simple wrapper for JointSpacingAnalysisSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.JointSpacingAnalysisSettings


    def __init__(self, set: Optional[SetEntityInfoRef] = None, custom_options: Optional[CustomHistogramOptionsVal] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the JointSpacingAnalysisSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if set is not None:
            self.set = set
        if custom_options is not None:
            self._proto_message.CustomOptions.CopyFrom(custom_options.to_proto())
            self._custom_options_wrapper = custom_options


    # Properties

    @property
    def spacing_option(self) -> Any:
        """Get the SpacingOption field value."""
        return self._proto_message.SpacingOption
    
    @spacing_option.setter
    def spacing_option(self, value: Any) -> None:
        """Set the SpacingOption field value."""
        self._proto_message.SpacingOption = value


    @property
    def set(self) -> SetEntityInfoRef:
        """Get the Set field as a reference."""
        return SetEntityInfoRef(self.__channelToConnectOn, self._proto_message.Set)
    
    @set.setter
    def set(self, value: SetEntityInfoRef) -> None:
        """Set the Set field to a reference."""
        self._proto_message.Set.CopyFrom(value.get_model_ref())


    @property
    def traverses(self) -> List[OrientationDataSetRef]:
        """Get the Traverses field as a list."""
        return _ProtobufListWrapper(self._proto_message.Traverses)
    
    @traverses.setter
    def traverses(self, value: List[OrientationDataSetRef]) -> None:
        """Set the Traverses field to a list."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.Traverses[:] = []
        self._proto_message.Traverses.extend(value)


    @property
    def num_intervals(self) -> int:
        """Get the NumIntervals field value."""
        return self._proto_message.NumIntervals
    
    @num_intervals.setter
    def num_intervals(self, value: int) -> None:
        """Set the NumIntervals field value."""
        self._proto_message.NumIntervals = value


    @property
    def show_best_fit_distribution(self) -> bool:
        """Get the ShowBestFitDistribution field value."""
        return self._proto_message.ShowBestFitDistribution
    
    @show_best_fit_distribution.setter
    def show_best_fit_distribution(self, value: bool) -> None:
        """Set the ShowBestFitDistribution field value."""
        self._proto_message.ShowBestFitDistribution = value


    @property
    def custom_options(self) -> CustomHistogramOptionsVal:
        """Get the CustomOptions field as a wrapper."""
        if not hasattr(self, '_custom_options_wrapper'):
            self._custom_options_wrapper = CustomHistogramOptionsVal(proto_message=self._proto_message.CustomOptions)
        return self._custom_options_wrapper
    
    @custom_options.setter
    def custom_options(self, value: CustomHistogramOptionsVal) -> None:
        """Set the CustomOptions field to a wrapper."""
        self._proto_message.CustomOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_custom_options_wrapper'):
            self._custom_options_wrapper._proto_message.CopyFrom(self._proto_message.CustomOptions)


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
