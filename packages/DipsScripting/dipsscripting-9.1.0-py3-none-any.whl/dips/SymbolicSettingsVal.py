"""Generated wrapper for SymbolicSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .QualitativeQuantitativeAnalysisSettingsVal import QualitativeQuantitativeAnalysisSettingsVal
from .SymbolDisplaySettingVal import SymbolDisplaySettingVal

class SymbolicSettingsVal:
    """Simple wrapper for SymbolicSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SymbolicSettings


    def __init__(self, qualitative_quantitative_analysis_settings: Optional[QualitativeQuantitativeAnalysisSettingsVal] = None, proto_message: Optional[Any] = None):
        """Initialize the SymbolicSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if qualitative_quantitative_analysis_settings is not None:
            self._proto_message.QualitativeQuantitativeAnalysisSettings.CopyFrom(qualitative_quantitative_analysis_settings.to_proto())
            self._qualitative_quantitative_analysis_settings_wrapper = qualitative_quantitative_analysis_settings


    # Properties

    @property
    def qualitative_quantitative_analysis_settings(self) -> QualitativeQuantitativeAnalysisSettingsVal:
        """Get the QualitativeQuantitativeAnalysisSettings field as a wrapper."""
        if not hasattr(self, '_qualitative_quantitative_analysis_settings_wrapper'):
            self._qualitative_quantitative_analysis_settings_wrapper = QualitativeQuantitativeAnalysisSettingsVal(proto_message=self._proto_message.QualitativeQuantitativeAnalysisSettings)
        return self._qualitative_quantitative_analysis_settings_wrapper
    
    @qualitative_quantitative_analysis_settings.setter
    def qualitative_quantitative_analysis_settings(self, value: QualitativeQuantitativeAnalysisSettingsVal) -> None:
        """Set the QualitativeQuantitativeAnalysisSettings field to a wrapper."""
        self._proto_message.QualitativeQuantitativeAnalysisSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_qualitative_quantitative_analysis_settings_wrapper'):
            self._qualitative_quantitative_analysis_settings_wrapper._proto_message.CopyFrom(self._proto_message.QualitativeQuantitativeAnalysisSettings)


    @property
    def legend_symbols(self) -> List[SymbolDisplaySettingVal]:
        """Get the LegendSymbols field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.LegendSymbols, SymbolDisplaySettingVal)
    
    @legend_symbols.setter
    def legend_symbols(self, value: List[SymbolDisplaySettingVal]) -> None:
        """Set the LegendSymbols field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.LegendSymbols[:] = []
        for item in value:
            self._proto_message.LegendSymbols.append(item.to_proto())


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
