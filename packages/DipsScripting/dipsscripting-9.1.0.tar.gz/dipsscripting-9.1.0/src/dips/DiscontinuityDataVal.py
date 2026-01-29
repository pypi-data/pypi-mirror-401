"""Generated wrapper for DiscontinuityData protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal
from .CustomRowRawDataVal import CustomRowRawDataVal
from .Vector3Val import Vector3Val

class DiscontinuityDataVal:
    """Simple wrapper for DiscontinuityData with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.DiscontinuityData


    def __init__(self, orientation1: Optional[AngleDataVal] = None, orientation2: Optional[AngleDataVal] = None, position: Optional[Vector3Val] = None, extra_data: Optional[CustomRowRawDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the DiscontinuityData wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if orientation1 is not None:
            self._proto_message.Orientation1.CopyFrom(orientation1.to_proto())
            self._orientation1_wrapper = orientation1
        if orientation2 is not None:
            self._proto_message.Orientation2.CopyFrom(orientation2.to_proto())
            self._orientation2_wrapper = orientation2
        if position is not None:
            self._proto_message.Position.CopyFrom(position.to_proto())
            self._position_wrapper = position
        if extra_data is not None:
            self._proto_message.ExtraData.CopyFrom(extra_data.to_proto())
            self._extra_data_wrapper = extra_data


    # Properties

    @property
    def orientation1(self) -> AngleDataVal:
        """Get the Orientation1 field as a wrapper."""
        if not hasattr(self, '_orientation1_wrapper'):
            self._orientation1_wrapper = AngleDataVal(proto_message=self._proto_message.Orientation1)
        return self._orientation1_wrapper
    
    @orientation1.setter
    def orientation1(self, value: AngleDataVal) -> None:
        """Set the Orientation1 field to a wrapper."""
        self._proto_message.Orientation1.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_orientation1_wrapper'):
            self._orientation1_wrapper._proto_message.CopyFrom(self._proto_message.Orientation1)


    @property
    def orientation2(self) -> AngleDataVal:
        """Get the Orientation2 field as a wrapper."""
        if not hasattr(self, '_orientation2_wrapper'):
            self._orientation2_wrapper = AngleDataVal(proto_message=self._proto_message.Orientation2)
        return self._orientation2_wrapper
    
    @orientation2.setter
    def orientation2(self, value: AngleDataVal) -> None:
        """Set the Orientation2 field to a wrapper."""
        self._proto_message.Orientation2.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_orientation2_wrapper'):
            self._orientation2_wrapper._proto_message.CopyFrom(self._proto_message.Orientation2)


    @property
    def quantity(self) -> float:
        """Get the Quantity field value."""
        return self._proto_message.Quantity
    
    @quantity.setter
    def quantity(self, value: float) -> None:
        """Set the Quantity field value."""
        self._proto_message.Quantity = value


    @property
    def persistence(self) -> float:
        """Get the Persistence field value."""
        return self._proto_message.Persistence
    
    @persistence.setter
    def persistence(self, value: float) -> None:
        """Set the Persistence field value."""
        self._proto_message.Persistence = value


    @property
    def distance(self) -> float:
        """Get the Distance field value."""
        return self._proto_message.Distance
    
    @distance.setter
    def distance(self, value: float) -> None:
        """Set the Distance field value."""
        self._proto_message.Distance = value


    @property
    def position(self) -> Vector3Val:
        """Get the Position field as a wrapper."""
        if not hasattr(self, '_position_wrapper'):
            self._position_wrapper = Vector3Val(proto_message=self._proto_message.Position)
        return self._position_wrapper
    
    @position.setter
    def position(self, value: Vector3Val) -> None:
        """Set the Position field to a wrapper."""
        self._proto_message.Position.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_position_wrapper'):
            self._position_wrapper._proto_message.CopyFrom(self._proto_message.Position)


    @property
    def extra_data(self) -> CustomRowRawDataVal:
        """Get the ExtraData field as a wrapper."""
        if not hasattr(self, '_extra_data_wrapper'):
            self._extra_data_wrapper = CustomRowRawDataVal(proto_message=self._proto_message.ExtraData)
        return self._extra_data_wrapper
    
    @extra_data.setter
    def extra_data(self, value: CustomRowRawDataVal) -> None:
        """Set the ExtraData field to a wrapper."""
        self._proto_message.ExtraData.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_extra_data_wrapper'):
            self._extra_data_wrapper._proto_message.CopyFrom(self._proto_message.ExtraData)


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
