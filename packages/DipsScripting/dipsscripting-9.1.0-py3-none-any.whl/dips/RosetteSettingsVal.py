"""Generated wrapper for RosetteSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal
from .TrendPlungeVal import TrendPlungeVal

class RosetteSettingsVal:
    """Simple wrapper for RosetteSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.RosetteSettings


    def __init__(self, sight_line_orientation: Optional[TrendPlungeVal] = None, min_angle: Optional[AngleDataVal] = None, max_angle: Optional[AngleDataVal] = None, start_bin_strike: Optional[AngleDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the RosetteSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if sight_line_orientation is not None:
            self._proto_message.SightLineOrientation.CopyFrom(sight_line_orientation.to_proto())
            self._sight_line_orientation_wrapper = sight_line_orientation
        if min_angle is not None:
            self._proto_message.MinAngle.CopyFrom(min_angle.to_proto())
            self._min_angle_wrapper = min_angle
        if max_angle is not None:
            self._proto_message.MaxAngle.CopyFrom(max_angle.to_proto())
            self._max_angle_wrapper = max_angle
        if start_bin_strike is not None:
            self._proto_message.StartBinStrike.CopyFrom(start_bin_strike.to_proto())
            self._start_bin_strike_wrapper = start_bin_strike


    # Properties

    @property
    def sight_line_orientation(self) -> TrendPlungeVal:
        """Get the SightLineOrientation field as a wrapper."""
        if not hasattr(self, '_sight_line_orientation_wrapper'):
            self._sight_line_orientation_wrapper = TrendPlungeVal(proto_message=self._proto_message.SightLineOrientation)
        return self._sight_line_orientation_wrapper
    
    @sight_line_orientation.setter
    def sight_line_orientation(self, value: TrendPlungeVal) -> None:
        """Set the SightLineOrientation field to a wrapper."""
        self._proto_message.SightLineOrientation.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_sight_line_orientation_wrapper'):
            self._sight_line_orientation_wrapper._proto_message.CopyFrom(self._proto_message.SightLineOrientation)


    @property
    def min_angle(self) -> AngleDataVal:
        """Get the MinAngle field as a wrapper."""
        if not hasattr(self, '_min_angle_wrapper'):
            self._min_angle_wrapper = AngleDataVal(proto_message=self._proto_message.MinAngle)
        return self._min_angle_wrapper
    
    @min_angle.setter
    def min_angle(self, value: AngleDataVal) -> None:
        """Set the MinAngle field to a wrapper."""
        self._proto_message.MinAngle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_min_angle_wrapper'):
            self._min_angle_wrapper._proto_message.CopyFrom(self._proto_message.MinAngle)


    @property
    def max_angle(self) -> AngleDataVal:
        """Get the MaxAngle field as a wrapper."""
        if not hasattr(self, '_max_angle_wrapper'):
            self._max_angle_wrapper = AngleDataVal(proto_message=self._proto_message.MaxAngle)
        return self._max_angle_wrapper
    
    @max_angle.setter
    def max_angle(self, value: AngleDataVal) -> None:
        """Set the MaxAngle field to a wrapper."""
        self._proto_message.MaxAngle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_max_angle_wrapper'):
            self._max_angle_wrapper._proto_message.CopyFrom(self._proto_message.MaxAngle)


    @property
    def start_bin_strike(self) -> AngleDataVal:
        """Get the StartBinStrike field as a wrapper."""
        if not hasattr(self, '_start_bin_strike_wrapper'):
            self._start_bin_strike_wrapper = AngleDataVal(proto_message=self._proto_message.StartBinStrike)
        return self._start_bin_strike_wrapper
    
    @start_bin_strike.setter
    def start_bin_strike(self, value: AngleDataVal) -> None:
        """Set the StartBinStrike field to a wrapper."""
        self._proto_message.StartBinStrike.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_start_bin_strike_wrapper'):
            self._start_bin_strike_wrapper._proto_message.CopyFrom(self._proto_message.StartBinStrike)


    @property
    def num_bins(self) -> int:
        """Get the NumBins field value."""
        return self._proto_message.NumBins
    
    @num_bins.setter
    def num_bins(self, value: int) -> None:
        """Set the NumBins field value."""
        self._proto_message.NumBins = value


    @property
    def custom_scaling(self) -> bool:
        """Get the CustomScaling field value."""
        return self._proto_message.CustomScaling
    
    @custom_scaling.setter
    def custom_scaling(self, value: bool) -> None:
        """Set the CustomScaling field value."""
        self._proto_message.CustomScaling = value


    @property
    def num_planes_per_circle_increment(self) -> int:
        """Get the NumPlanesPerCircleIncrement field value."""
        return self._proto_message.NumPlanesPerCircleIncrement
    
    @num_planes_per_circle_increment.setter
    def num_planes_per_circle_increment(self, value: int) -> None:
        """Set the NumPlanesPerCircleIncrement field value."""
        self._proto_message.NumPlanesPerCircleIncrement = value


    @property
    def is_weighted(self) -> bool:
        """Get the IsWeighted field value."""
        return self._proto_message.IsWeighted
    
    @is_weighted.setter
    def is_weighted(self, value: bool) -> None:
        """Set the IsWeighted field value."""
        self._proto_message.IsWeighted = value


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
