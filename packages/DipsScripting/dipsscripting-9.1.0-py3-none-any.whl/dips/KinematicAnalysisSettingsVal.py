"""Generated wrapper for KinematicAnalysisSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal

class KinematicAnalysisSettingsVal:
    """Simple wrapper for KinematicAnalysisSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.KinematicAnalysisSettings


    def __init__(self, slope_dip: Optional[AngleDataVal] = None, slope_dip_direction: Optional[AngleDataVal] = None, friction_angle: Optional[AngleDataVal] = None, lateral_limits: Optional[AngleDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the KinematicAnalysisSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if slope_dip is not None:
            self._proto_message.SlopeDip.CopyFrom(slope_dip.to_proto())
            self._slope_dip_wrapper = slope_dip
        if slope_dip_direction is not None:
            self._proto_message.SlopeDipDirection.CopyFrom(slope_dip_direction.to_proto())
            self._slope_dip_direction_wrapper = slope_dip_direction
        if friction_angle is not None:
            self._proto_message.FrictionAngle.CopyFrom(friction_angle.to_proto())
            self._friction_angle_wrapper = friction_angle
        if lateral_limits is not None:
            self._proto_message.LateralLimits.CopyFrom(lateral_limits.to_proto())
            self._lateral_limits_wrapper = lateral_limits


    # Properties

    @property
    def failure_mode_option(self) -> Any:
        """Get the FailureModeOption field value."""
        return self._proto_message.FailureModeOption
    
    @failure_mode_option.setter
    def failure_mode_option(self, value: Any) -> None:
        """Set the FailureModeOption field value."""
        self._proto_message.FailureModeOption = value


    @property
    def slope_dip(self) -> AngleDataVal:
        """Get the SlopeDip field as a wrapper."""
        if not hasattr(self, '_slope_dip_wrapper'):
            self._slope_dip_wrapper = AngleDataVal(proto_message=self._proto_message.SlopeDip)
        return self._slope_dip_wrapper
    
    @slope_dip.setter
    def slope_dip(self, value: AngleDataVal) -> None:
        """Set the SlopeDip field to a wrapper."""
        self._proto_message.SlopeDip.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_slope_dip_wrapper'):
            self._slope_dip_wrapper._proto_message.CopyFrom(self._proto_message.SlopeDip)


    @property
    def slope_dip_direction(self) -> AngleDataVal:
        """Get the SlopeDipDirection field as a wrapper."""
        if not hasattr(self, '_slope_dip_direction_wrapper'):
            self._slope_dip_direction_wrapper = AngleDataVal(proto_message=self._proto_message.SlopeDipDirection)
        return self._slope_dip_direction_wrapper
    
    @slope_dip_direction.setter
    def slope_dip_direction(self, value: AngleDataVal) -> None:
        """Set the SlopeDipDirection field to a wrapper."""
        self._proto_message.SlopeDipDirection.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_slope_dip_direction_wrapper'):
            self._slope_dip_direction_wrapper._proto_message.CopyFrom(self._proto_message.SlopeDipDirection)


    @property
    def friction_angle(self) -> AngleDataVal:
        """Get the FrictionAngle field as a wrapper."""
        if not hasattr(self, '_friction_angle_wrapper'):
            self._friction_angle_wrapper = AngleDataVal(proto_message=self._proto_message.FrictionAngle)
        return self._friction_angle_wrapper
    
    @friction_angle.setter
    def friction_angle(self, value: AngleDataVal) -> None:
        """Set the FrictionAngle field to a wrapper."""
        self._proto_message.FrictionAngle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_friction_angle_wrapper'):
            self._friction_angle_wrapper._proto_message.CopyFrom(self._proto_message.FrictionAngle)


    @property
    def lateral_limits(self) -> AngleDataVal:
        """Get the LateralLimits field as a wrapper."""
        if not hasattr(self, '_lateral_limits_wrapper'):
            self._lateral_limits_wrapper = AngleDataVal(proto_message=self._proto_message.LateralLimits)
        return self._lateral_limits_wrapper
    
    @lateral_limits.setter
    def lateral_limits(self, value: AngleDataVal) -> None:
        """Set the LateralLimits field to a wrapper."""
        self._proto_message.LateralLimits.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_lateral_limits_wrapper'):
            self._lateral_limits_wrapper._proto_message.CopyFrom(self._proto_message.LateralLimits)


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
