"""
Dips Python API

Public API for interacting with Dips application via gRPC.
"""

# Main application interface
from .DipsApp import DipsApp

# Built-in data formatters and descriptors
from .BuiltInDataFormatters import *
from .BuiltInDataDescriptors import *

# Re-export commonly used protobuf modules for convenience
from . import DipsAPI_pb2
from . import DipsAPI_pb2_grpc

# Optionally expose commonly used classes - uncomment if desired
# from .ProjStubRef import ProjStubRef
# from .OrientationDataSetRef import OrientationDataSetRef
# from .SetEntityInfoRef import SetEntityInfoRef
# etc.

__all__ = [
    'DipsApp',
    'DipsAPI_pb2',
    'DipsAPI_pb2_grpc',
    # Add other public exports here
]
