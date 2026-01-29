from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .FoldWindowEntityVisibilityVal import FoldWindowEntityVisibilityVal

class FoldWindowEntityVisibilityRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_FoldWindowEntityVisibility):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> FoldWindowEntityVisibilityVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.FoldWindowEntityVisibility()
        ret.MergeFromString(bytes.data)
        return FoldWindowEntityVisibilityVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def SetFoldWindowEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_FoldWindowEntityVisibility_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetFoldWindowEntityVisibility(functionParam)
        

 