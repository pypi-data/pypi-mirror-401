"""Generated wrapper for ClusterWindow protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AutomaticClusterAnalysisSettingsVal import AutomaticClusterAnalysisSettingsVal
from .FullDataFormatVal import FullDataFormatVal
from .TrendPlungeVal import TrendPlungeVal
from .DataFilterRef import DataFilterRef

class ClusterWindowVal:
    """Simple wrapper for ClusterWindow with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ClusterWindow


    def __init__(self, cluster_settings: Optional[AutomaticClusterAnalysisSettingsVal] = None, cluster_filter: Optional[DataFilterRef] = None, cluster_center: Optional[TrendPlungeVal] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the ClusterWindow wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if cluster_settings is not None:
            self._proto_message.ClusterSettings.CopyFrom(cluster_settings.to_proto())
            self._cluster_settings_wrapper = cluster_settings
        if cluster_filter is not None:
            self.cluster_filter = cluster_filter
        if cluster_center is not None:
            self._proto_message.ClusterCenter.CopyFrom(cluster_center.to_proto())
            self._cluster_center_wrapper = cluster_center


    # Properties

    @property
    def id(self) -> str:
        """Get the ID field value."""
        return self._proto_message.ID
    
    @id.setter
    def id(self, value: str) -> None:
        """Set the ID field value."""
        self._proto_message.ID = value


    @property
    def cluster_id(self) -> int:
        """Get the ClusterID field value."""
        return self._proto_message.ClusterID
    
    @cluster_id.setter
    def cluster_id(self, value: int) -> None:
        """Set the ClusterID field value."""
        self._proto_message.ClusterID = value


    @property
    def cluster_labels(self) -> list:
        """Get the ClusterLabels field as a list."""
        return _ProtobufListWrapper(self._proto_message.ClusterLabels)
    
    @cluster_labels.setter
    def cluster_labels(self, value: list) -> None:
        """Set the ClusterLabels field to a list."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.ClusterLabels[:] = []
        self._proto_message.ClusterLabels.extend(value)


    @property
    def cluster_settings(self) -> AutomaticClusterAnalysisSettingsVal:
        """Get the ClusterSettings field as a wrapper."""
        if not hasattr(self, '_cluster_settings_wrapper'):
            self._cluster_settings_wrapper = AutomaticClusterAnalysisSettingsVal(proto_message=self._proto_message.ClusterSettings)
        return self._cluster_settings_wrapper
    
    @cluster_settings.setter
    def cluster_settings(self, value: AutomaticClusterAnalysisSettingsVal) -> None:
        """Set the ClusterSettings field to a wrapper."""
        self._proto_message.ClusterSettings.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_cluster_settings_wrapper'):
            self._cluster_settings_wrapper._proto_message.CopyFrom(self._proto_message.ClusterSettings)


    @property
    def cluster_filter(self) -> DataFilterRef:
        """Get the ClusterFilter field as a reference."""
        return DataFilterRef(self.__channelToConnectOn, self._proto_message.ClusterFilter)
    
    @cluster_filter.setter
    def cluster_filter(self, value: DataFilterRef) -> None:
        """Set the ClusterFilter field to a reference."""
        self._proto_message.ClusterFilter.CopyFrom(value.get_model_ref())


    @property
    def used_column_headers(self) -> List[FullDataFormatVal]:
        """Get the UsedColumnHeaders field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.UsedColumnHeaders, FullDataFormatVal)
    
    @used_column_headers.setter
    def used_column_headers(self, value: List[FullDataFormatVal]) -> None:
        """Set the UsedColumnHeaders field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.UsedColumnHeaders[:] = []
        for item in value:
            self._proto_message.UsedColumnHeaders.append(item.to_proto())


    @property
    def cluster_bearings(self) -> List[TrendPlungeVal]:
        """Get the ClusterBearings field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.ClusterBearings, TrendPlungeVal)
    
    @cluster_bearings.setter
    def cluster_bearings(self, value: List[TrendPlungeVal]) -> None:
        """Set the ClusterBearings field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.ClusterBearings[:] = []
        for item in value:
            self._proto_message.ClusterBearings.append(item.to_proto())


    @property
    def cluster_center(self) -> TrendPlungeVal:
        """Get the ClusterCenter field as a wrapper."""
        if not hasattr(self, '_cluster_center_wrapper'):
            self._cluster_center_wrapper = TrendPlungeVal(proto_message=self._proto_message.ClusterCenter)
        return self._cluster_center_wrapper
    
    @cluster_center.setter
    def cluster_center(self, value: TrendPlungeVal) -> None:
        """Set the ClusterCenter field to a wrapper."""
        self._proto_message.ClusterCenter.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_cluster_center_wrapper'):
            self._cluster_center_wrapper._proto_message.CopyFrom(self._proto_message.ClusterCenter)


    @property
    def is_wrapped_cluster(self) -> bool:
        """Get the IsWrappedCluster field value."""
        return self._proto_message.IsWrappedCluster
    
    @is_wrapped_cluster.setter
    def is_wrapped_cluster(self, value: bool) -> None:
        """Set the IsWrappedCluster field value."""
        self._proto_message.IsWrappedCluster = value


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
