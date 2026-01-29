"""Generated wrapper for StatisticalDistributionFilter protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class StatisticalDistributionFilterVal:
    """Simple wrapper for StatisticalDistributionFilter with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.StatisticalDistributionFilter


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the StatisticalDistributionFilter wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def normal_distribution(self) -> bool:
        """Get the NormalDistribution field value."""
        return self._proto_message.NormalDistribution
    
    @normal_distribution.setter
    def normal_distribution(self, value: bool) -> None:
        """Set the NormalDistribution field value."""
        self._proto_message.NormalDistribution = value


    @property
    def uniform_distribution(self) -> bool:
        """Get the UniformDistribution field value."""
        return self._proto_message.UniformDistribution
    
    @uniform_distribution.setter
    def uniform_distribution(self, value: bool) -> None:
        """Set the UniformDistribution field value."""
        self._proto_message.UniformDistribution = value


    @property
    def triangular_distribution(self) -> bool:
        """Get the TriangularDistribution field value."""
        return self._proto_message.TriangularDistribution
    
    @triangular_distribution.setter
    def triangular_distribution(self, value: bool) -> None:
        """Set the TriangularDistribution field value."""
        self._proto_message.TriangularDistribution = value


    @property
    def beta_distribution(self) -> bool:
        """Get the BetaDistribution field value."""
        return self._proto_message.BetaDistribution
    
    @beta_distribution.setter
    def beta_distribution(self, value: bool) -> None:
        """Set the BetaDistribution field value."""
        self._proto_message.BetaDistribution = value


    @property
    def exponential_distribution(self) -> bool:
        """Get the ExponentialDistribution field value."""
        return self._proto_message.ExponentialDistribution
    
    @exponential_distribution.setter
    def exponential_distribution(self, value: bool) -> None:
        """Set the ExponentialDistribution field value."""
        self._proto_message.ExponentialDistribution = value


    @property
    def lognormal_distribution(self) -> bool:
        """Get the LognormalDistribution field value."""
        return self._proto_message.LognormalDistribution
    
    @lognormal_distribution.setter
    def lognormal_distribution(self, value: bool) -> None:
        """Set the LognormalDistribution field value."""
        self._proto_message.LognormalDistribution = value


    @property
    def gamma_distribution(self) -> bool:
        """Get the GammaDistribution field value."""
        return self._proto_message.GammaDistribution
    
    @gamma_distribution.setter
    def gamma_distribution(self, value: bool) -> None:
        """Set the GammaDistribution field value."""
        self._proto_message.GammaDistribution = value


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
