"""Generated wrapper for TextToolEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AnchorPointVal import AnchorPointVal
from .FillFormatVal import FillFormatVal
from .LineFormatVal import LineFormatVal
from .TextFormatVal import TextFormatVal

class TextToolEntityInfoVal:
    """Simple wrapper for TextToolEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.TextToolEntityInfo


    def __init__(self, anchor_point: Optional[AnchorPointVal] = None, line_format: Optional[LineFormatVal] = None, fill_format: Optional[FillFormatVal] = None, text_format: Optional[TextFormatVal] = None, proto_message: Optional[Any] = None):
        """Initialize the TextToolEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if anchor_point is not None:
            self._proto_message.AnchorPoint.CopyFrom(anchor_point.to_proto())
            self._anchor_point_wrapper = anchor_point
        if line_format is not None:
            self._proto_message.LineFormat.CopyFrom(line_format.to_proto())
            self._line_format_wrapper = line_format
        if fill_format is not None:
            self._proto_message.FillFormat.CopyFrom(fill_format.to_proto())
            self._fill_format_wrapper = fill_format
        if text_format is not None:
            self._proto_message.TextFormat.CopyFrom(text_format.to_proto())
            self._text_format_wrapper = text_format


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
    def fill_format(self) -> FillFormatVal:
        """Get the FillFormat field as a wrapper."""
        if not hasattr(self, '_fill_format_wrapper'):
            self._fill_format_wrapper = FillFormatVal(proto_message=self._proto_message.FillFormat)
        return self._fill_format_wrapper
    
    @fill_format.setter
    def fill_format(self, value: FillFormatVal) -> None:
        """Set the FillFormat field to a wrapper."""
        self._proto_message.FillFormat.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_fill_format_wrapper'):
            self._fill_format_wrapper._proto_message.CopyFrom(self._proto_message.FillFormat)


    @property
    def text_format(self) -> TextFormatVal:
        """Get the TextFormat field as a wrapper."""
        if not hasattr(self, '_text_format_wrapper'):
            self._text_format_wrapper = TextFormatVal(proto_message=self._proto_message.TextFormat)
        return self._text_format_wrapper
    
    @text_format.setter
    def text_format(self, value: TextFormatVal) -> None:
        """Set the TextFormat field to a wrapper."""
        self._proto_message.TextFormat.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_text_format_wrapper'):
            self._text_format_wrapper._proto_message.CopyFrom(self._proto_message.TextFormat)


    @property
    def text(self) -> str:
        """Get the Text field value."""
        return self._proto_message.Text
    
    @text.setter
    def text(self, value: str) -> None:
        """Set the Text field value."""
        self._proto_message.Text = value


    @property
    def autogenerated_text(self) -> str:
        """Get the AutogeneratedText field value."""
        return self._proto_message.AutogeneratedText
    
    @autogenerated_text.setter
    def autogenerated_text(self, value: str) -> None:
        """Set the AutogeneratedText field value."""
        self._proto_message.AutogeneratedText = value


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
