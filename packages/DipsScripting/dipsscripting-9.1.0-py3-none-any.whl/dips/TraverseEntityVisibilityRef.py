from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .TraverseEntityVisibilityVal import TraverseEntityVisibilityVal
from .TraverseEntityVisibilityVal import TraverseEntityVisibilityVal
from .ValidatableResultVal import ValidatableResultVal

class TraverseEntityVisibilityRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_TraverseEntityVisibility):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> TraverseEntityVisibilityVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.TraverseEntityVisibility()
        ret.MergeFromString(bytes.data)
        return TraverseEntityVisibilityVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def SetTraverseEntityOptions(self,  TraverseEntityVisibility: TraverseEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TraverseEntityVisibility_TraverseEntityVisibility(This=self.__modelRef,  Input1=(TraverseEntityVisibility.to_proto() if hasattr(TraverseEntityVisibility, 'to_proto') else TraverseEntityVisibility))
        ret = self.__EntityServicesStubLocal.SetTraverseEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetTraverseEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TraverseEntityVisibility_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetTraverseEntityVisibility(functionParam)
        

 