"""Generated wrapper for ArrowToolEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AnchorPointVal import AnchorPointVal
from .LineFormatVal import LineFormatVal

class ArrowToolEntityInfoVal:
    """Simple wrapper for ArrowToolEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ArrowToolEntityInfo


    def __init__(self, anchor_point: Optional[AnchorPointVal] = None, anchor_point_secondary: Optional[AnchorPointVal] = None, line_format: Optional[LineFormatVal] = None, proto_message: Optional[Any] = None):
        """Initialize the ArrowToolEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if anchor_point is not None:
            self._proto_message.AnchorPoint.CopyFrom(anchor_point.to_proto())
            self._anchor_point_wrapper = anchor_point
        if anchor_point_secondary is not None:
            self._proto_message.AnchorPointSecondary.CopyFrom(anchor_point_secondary.to_proto())
            self._anchor_point_secondary_wrapper = anchor_point_secondary
        if line_format is not None:
            self._proto_message.LineFormat.CopyFrom(line_format.to_proto())
            self._line_format_wrapper = line_format


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
    def name(self) -> str:
        """Get the Name field value."""
        return self._proto_message.Name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the Name field value."""
        self._proto_message.Name = value


    @property
    def anchor_point(self) -> AnchorPointVal:
        """Get the AnchorPoint field as a wrapper."""
        if not hasattr(self, '_anchor_point_wrapper'):
            self._anchor_point_wrapper = AnchorPointVal(proto_message=self._proto_message.AnchorPoint)
        return self._anchor_point_wrapper
    
    @anchor_point.setter
    def anchor_point(self, value: AnchorPointVal) -> None:
        """Set the AnchorPoint field to a wrapper."""
        self._proto_message.AnchorPoint.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_anchor_point_wrapper'):
            self._anchor_point_wrapper._proto_message.CopyFrom(self._proto_message.AnchorPoint)


    @property
    def anchor_point_secondary(self) -> AnchorPointVal:
        """Get the AnchorPointSecondary field as a wrapper."""
        if not hasattr(self, '_anchor_point_secondary_wrapper'):
            self._anchor_point_secondary_wrapper = AnchorPointVal(proto_message=self._proto_message.AnchorPointSecondary)
        return self._anchor_point_secondary_wrapper
    
    @anchor_point_secondary.setter
    def anchor_point_secondary(self, value: AnchorPointVal) -> None:
        """Set the AnchorPointSecondary field to a wrapper."""
        self._proto_message.AnchorPointSecondary.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_anchor_point_secondary_wrapper'):
            self._anchor_point_secondary_wrapper._proto_message.CopyFrom(self._proto_message.AnchorPointSecondary)


    @property
    def line_format(self) -> LineFormatVal:
        """Get the LineFormat field as a wrapper."""
        if not hasattr(self, '_line_format_wrapper'):
            self._line_format_wrapper = LineFormatVal(proto_message=self._proto_message.LineFormat)
        return self._line_format_wrapper
    
    @line_format.setter
    def line_format(self, value: LineFormatVal) -> None:
        """Set the LineFormat field to a wrapper."""
        self._proto_message.LineFormat.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_line_format_wrapper'):
            self._line_format_wrapper._proto_message.CopyFrom(self._proto_message.LineFormat)


    @property
    def show_arrow(self) -> bool:
        """Get the ShowArrow field value."""
        return self._proto_message.ShowArrow
    
    @show_arrow.setter
    def show_arrow(self, value: bool) -> None:
        """Set the ShowArrow field value."""
        self._proto_message.ShowArrow = value


    @property
    def show_arrow_secondary(self) -> bool:
        """Get the ShowArrowSecondary field value."""
        return self._proto_message.ShowArrowSecondary
    
    @show_arrow_secondary.setter
    def show_arrow_secondary(self, value: bool) -> None:
        """Set the ShowArrowSecondary field value."""
        self._proto_message.ShowArrowSecondary = value


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
