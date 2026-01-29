from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .SetEntityVisibilityVal import SetEntityVisibilityVal
from .SetEntityVisibilityVal import SetEntityVisibilityVal
from .ValidatableResultVal import ValidatableResultVal

class SetEntityVisibilityRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_SetEntityVisibility):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> SetEntityVisibilityVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.SetEntityVisibility()
        ret.MergeFromString(bytes.data)
        return SetEntityVisibilityVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def SetMeanSetPlaneEntityOptions(self,  SetEntityVisibility: SetEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_SetEntityVisibility_SetEntityVisibility(This=self.__modelRef,  Input1=(SetEntityVisibility.to_proto() if hasattr(SetEntityVisibility, 'to_proto') else SetEntityVisibility))
        ret = self.__EntityServicesStubLocal.SetMeanSetPlaneEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetMeanSetPlaneEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_SetEntityVisibility_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetMeanSetPlaneEntityVisibility(functionParam)
        

 