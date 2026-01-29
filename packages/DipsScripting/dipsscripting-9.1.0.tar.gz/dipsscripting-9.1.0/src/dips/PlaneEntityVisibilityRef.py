from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .PlaneEntityVisibilityVal import PlaneEntityVisibilityVal
from .PlaneEntityVisibilityVal import PlaneEntityVisibilityVal
from .ValidatableResultVal import ValidatableResultVal

class PlaneEntityVisibilityRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_PlaneEntityVisibility):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> PlaneEntityVisibilityVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.PlaneEntityVisibility()
        ret.MergeFromString(bytes.data)
        return PlaneEntityVisibilityVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def SetUserPlaneEntityOptions(self,  PlaneEntityVisibility: PlaneEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PlaneEntityVisibility_PlaneEntityVisibility(This=self.__modelRef,  Input1=(PlaneEntityVisibility.to_proto() if hasattr(PlaneEntityVisibility, 'to_proto') else PlaneEntityVisibility))
        ret = self.__EntityServicesStubLocal.SetUserPlaneEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetUserPlaneEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PlaneEntityVisibility_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetUserPlaneEntityVisibility(functionParam)
        

 