"""Generated wrapper for AutomaticClusterAnalysisSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class AutomaticClusterAnalysisSettingsVal:
    """Simple wrapper for AutomaticClusterAnalysisSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.AutomaticClusterAnalysisSettings


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the AutomaticClusterAnalysisSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def is_weighted(self) -> bool:
        """Get the IsWeighted field value."""
        return self._proto_message.IsWeighted
    
    @is_weighted.setter
    def is_weighted(self, value: bool) -> None:
        """Set the IsWeighted field value."""
        self._proto_message.IsWeighted = value


    @property
    def min_num_clusters(self) -> int:
        """Get the MinNumClusters field value."""
        return self._proto_message.MinNumClusters
    
    @min_num_clusters.setter
    def min_num_clusters(self, value: int) -> None:
        """Set the MinNumClusters field value."""
        self._proto_message.MinNumClusters = value


    @property
    def max_num_clusters(self) -> int:
        """Get the MaxNumClusters field value."""
        return self._proto_message.MaxNumClusters
    
    @max_num_clusters.setter
    def max_num_clusters(self, value: int) -> None:
        """Set the MaxNumClusters field value."""
        self._proto_message.MaxNumClusters = value


    @property
    def minimum_membership_degree_percent(self) -> float:
        """Get the MinimumMembershipDegreePercent field value."""
        return self._proto_message.MinimumMembershipDegreePercent
    
    @minimum_membership_degree_percent.setter
    def minimum_membership_degree_percent(self, value: float) -> None:
        """Set the MinimumMembershipDegreePercent field value."""
        self._proto_message.MinimumMembershipDegreePercent = value


    @property
    def confidence_interval(self) -> float:
        """Get the ConfidenceInterval field value."""
        return self._proto_message.ConfidenceInterval
    
    @confidence_interval.setter
    def confidence_interval(self, value: float) -> None:
        """Set the ConfidenceInterval field value."""
        self._proto_message.ConfidenceInterval = value


    @property
    def number_of_runs(self) -> int:
        """Get the NumberOfRuns field value."""
        return self._proto_message.NumberOfRuns
    
    @number_of_runs.setter
    def number_of_runs(self, value: int) -> None:
        """Set the NumberOfRuns field value."""
        self._proto_message.NumberOfRuns = value


    @property
    def convergence_tolerance(self) -> float:
        """Get the ConvergenceTolerance field value."""
        return self._proto_message.ConvergenceTolerance
    
    @convergence_tolerance.setter
    def convergence_tolerance(self, value: float) -> None:
        """Set the ConvergenceTolerance field value."""
        self._proto_message.ConvergenceTolerance = value


    @property
    def max_iterations(self) -> int:
        """Get the MaxIterations field value."""
        return self._proto_message.MaxIterations
    
    @max_iterations.setter
    def max_iterations(self, value: int) -> None:
        """Set the MaxIterations field value."""
        self._proto_message.MaxIterations = value


    @property
    def random_seed(self) -> int:
        """Get the RandomSeed field value."""
        return self._proto_message.RandomSeed
    
    @random_seed.setter
    def random_seed(self, value: int) -> None:
        """Set the RandomSeed field value."""
        self._proto_message.RandomSeed = value


    @property
    def fuzziness_parameter(self) -> float:
        """Get the FuzzinessParameter field value."""
        return self._proto_message.FuzzinessParameter
    
    @fuzziness_parameter.setter
    def fuzziness_parameter(self, value: float) -> None:
        """Set the FuzzinessParameter field value."""
        self._proto_message.FuzzinessParameter = value


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
