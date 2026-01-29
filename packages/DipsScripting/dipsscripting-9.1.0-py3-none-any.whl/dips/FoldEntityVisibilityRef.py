from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .FoldEntityVisibilityVal import FoldEntityVisibilityVal
from .FoldEntityVisibilityVal import FoldEntityVisibilityVal
from .ValidatableResultVal import ValidatableResultVal

class FoldEntityVisibilityRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_FoldEntityVisibility):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> FoldEntityVisibilityVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.FoldEntityVisibility()
        ret.MergeFromString(bytes.data)
        return FoldEntityVisibilityVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def SetFoldEntityOptions(self,  FoldEntityVisibility: FoldEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_FoldEntityVisibility_FoldEntityVisibility(This=self.__modelRef,  Input1=(FoldEntityVisibility.to_proto() if hasattr(FoldEntityVisibility, 'to_proto') else FoldEntityVisibility))
        ret = self.__EntityServicesStubLocal.SetFoldEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetFoldEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_FoldEntityVisibility_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetFoldEntityVisibility(functionParam)
        

 