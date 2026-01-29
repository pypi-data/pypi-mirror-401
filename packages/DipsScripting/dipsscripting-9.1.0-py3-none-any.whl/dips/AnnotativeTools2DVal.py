"""Generated wrapper for AnnotativeTools2D protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from .ConeToolEntityInfoVal import ConeToolEntityInfoVal
from .EllipseToolEntityInfoVal import EllipseToolEntityInfoVal
from .LineIntersectionCalculatorToolEntityInfoVal import LineIntersectionCalculatorToolEntityInfoVal
from .LineToolEntityInfoVal import LineToolEntityInfoVal
from .MeasureAngleToolEntityInfoVal import MeasureAngleToolEntityInfoVal
from .PitchGridToolEntityInfoVal import PitchGridToolEntityInfoVal
from .PlaneIntersectionCalculatorToolEntityInfoVal import PlaneIntersectionCalculatorToolEntityInfoVal
from .PolygonToolEntityInfoVal import PolygonToolEntityInfoVal
from .PolylineToolEntityInfoVal import PolylineToolEntityInfoVal
from .RectangleToolEntityInfoVal import RectangleToolEntityInfoVal
from .TextToolEntityInfoVal import TextToolEntityInfoVal
from .TrendLineToolEntityInfoVal import TrendLineToolEntityInfoVal

class AnnotativeTools2DVal:
    """Simple wrapper for AnnotativeTools2D with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.AnnotativeTools2D


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the AnnotativeTools2D wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def text_tool_entities(self) -> List[TextToolEntityInfoVal]:
        """Get the TextToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.TextToolEntities, TextToolEntityInfoVal)
    
    @text_tool_entities.setter
    def text_tool_entities(self, value: List[TextToolEntityInfoVal]) -> None:
        """Set the TextToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.TextToolEntities[:] = []
        for item in value:
            self._proto_message.TextToolEntities.append(item.to_proto())


    @property
    def arrow_tool_entities(self) -> List[ArrowToolEntityInfoVal]:
        """Get the ArrowToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.ArrowToolEntities, ArrowToolEntityInfoVal)
    
    @arrow_tool_entities.setter
    def arrow_tool_entities(self, value: List[ArrowToolEntityInfoVal]) -> None:
        """Set the ArrowToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.ArrowToolEntities[:] = []
        for item in value:
            self._proto_message.ArrowToolEntities.append(item.to_proto())


    @property
    def line_tool_entities(self) -> List[LineToolEntityInfoVal]:
        """Get the LineToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.LineToolEntities, LineToolEntityInfoVal)
    
    @line_tool_entities.setter
    def line_tool_entities(self, value: List[LineToolEntityInfoVal]) -> None:
        """Set the LineToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.LineToolEntities[:] = []
        for item in value:
            self._proto_message.LineToolEntities.append(item.to_proto())


    @property
    def polyline_tool_entities(self) -> List[PolylineToolEntityInfoVal]:
        """Get the PolylineToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.PolylineToolEntities, PolylineToolEntityInfoVal)
    
    @polyline_tool_entities.setter
    def polyline_tool_entities(self, value: List[PolylineToolEntityInfoVal]) -> None:
        """Set the PolylineToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.PolylineToolEntities[:] = []
        for item in value:
            self._proto_message.PolylineToolEntities.append(item.to_proto())


    @property
    def polygon_tool_entities(self) -> List[PolygonToolEntityInfoVal]:
        """Get the PolygonToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.PolygonToolEntities, PolygonToolEntityInfoVal)
    
    @polygon_tool_entities.setter
    def polygon_tool_entities(self, value: List[PolygonToolEntityInfoVal]) -> None:
        """Set the PolygonToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.PolygonToolEntities[:] = []
        for item in value:
            self._proto_message.PolygonToolEntities.append(item.to_proto())


    @property
    def rectangle_tool_entities(self) -> List[RectangleToolEntityInfoVal]:
        """Get the RectangleToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.RectangleToolEntities, RectangleToolEntityInfoVal)
    
    @rectangle_tool_entities.setter
    def rectangle_tool_entities(self, value: List[RectangleToolEntityInfoVal]) -> None:
        """Set the RectangleToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.RectangleToolEntities[:] = []
        for item in value:
            self._proto_message.RectangleToolEntities.append(item.to_proto())


    @property
    def ellipse_tool_entities(self) -> List[EllipseToolEntityInfoVal]:
        """Get the EllipseToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.EllipseToolEntities, EllipseToolEntityInfoVal)
    
    @ellipse_tool_entities.setter
    def ellipse_tool_entities(self, value: List[EllipseToolEntityInfoVal]) -> None:
        """Set the EllipseToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.EllipseToolEntities[:] = []
        for item in value:
            self._proto_message.EllipseToolEntities.append(item.to_proto())


    @property
    def trend_line_tool_entities(self) -> List[TrendLineToolEntityInfoVal]:
        """Get the TrendLineToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.TrendLineToolEntities, TrendLineToolEntityInfoVal)
    
    @trend_line_tool_entities.setter
    def trend_line_tool_entities(self, value: List[TrendLineToolEntityInfoVal]) -> None:
        """Set the TrendLineToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.TrendLineToolEntities[:] = []
        for item in value:
            self._proto_message.TrendLineToolEntities.append(item.to_proto())


    @property
    def cone_tool_entities(self) -> List[ConeToolEntityInfoVal]:
        """Get the ConeToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.ConeToolEntities, ConeToolEntityInfoVal)
    
    @cone_tool_entities.setter
    def cone_tool_entities(self, value: List[ConeToolEntityInfoVal]) -> None:
        """Set the ConeToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.ConeToolEntities[:] = []
        for item in value:
            self._proto_message.ConeToolEntities.append(item.to_proto())


    @property
    def pitch_grid_tool_entities(self) -> List[PitchGridToolEntityInfoVal]:
        """Get the PitchGridToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.PitchGridToolEntities, PitchGridToolEntityInfoVal)
    
    @pitch_grid_tool_entities.setter
    def pitch_grid_tool_entities(self, value: List[PitchGridToolEntityInfoVal]) -> None:
        """Set the PitchGridToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.PitchGridToolEntities[:] = []
        for item in value:
            self._proto_message.PitchGridToolEntities.append(item.to_proto())


    @property
    def measure_angle_tool_entities(self) -> List[MeasureAngleToolEntityInfoVal]:
        """Get the MeasureAngleToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.MeasureAngleToolEntities, MeasureAngleToolEntityInfoVal)
    
    @measure_angle_tool_entities.setter
    def measure_angle_tool_entities(self, value: List[MeasureAngleToolEntityInfoVal]) -> None:
        """Set the MeasureAngleToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.MeasureAngleToolEntities[:] = []
        for item in value:
            self._proto_message.MeasureAngleToolEntities.append(item.to_proto())


    @property
    def line_intersection_calculator_tool_entities(self) -> List[LineIntersectionCalculatorToolEntityInfoVal]:
        """Get the LineIntersectionCalculatorToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.LineIntersectionCalculatorToolEntities, LineIntersectionCalculatorToolEntityInfoVal)
    
    @line_intersection_calculator_tool_entities.setter
    def line_intersection_calculator_tool_entities(self, value: List[LineIntersectionCalculatorToolEntityInfoVal]) -> None:
        """Set the LineIntersectionCalculatorToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.LineIntersectionCalculatorToolEntities[:] = []
        for item in value:
            self._proto_message.LineIntersectionCalculatorToolEntities.append(item.to_proto())


    @property
    def plane_intersection_calculator_tool_entities(self) -> List[PlaneIntersectionCalculatorToolEntityInfoVal]:
        """Get the PlaneIntersectionCalculatorToolEntities field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.PlaneIntersectionCalculatorToolEntities, PlaneIntersectionCalculatorToolEntityInfoVal)
    
    @plane_intersection_calculator_tool_entities.setter
    def plane_intersection_calculator_tool_entities(self, value: List[PlaneIntersectionCalculatorToolEntityInfoVal]) -> None:
        """Set the PlaneIntersectionCalculatorToolEntities field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.PlaneIntersectionCalculatorToolEntities[:] = []
        for item in value:
            self._proto_message.PlaneIntersectionCalculatorToolEntities.append(item.to_proto())


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
