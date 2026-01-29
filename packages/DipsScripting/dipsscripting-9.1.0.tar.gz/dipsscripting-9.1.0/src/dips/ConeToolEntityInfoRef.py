from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .ConeToolEntityInfoVal import ConeToolEntityInfoVal
from .ConeToolEntityInfoVal import ConeToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class ConeToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_ConeToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> ConeToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.ConeToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return ConeToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveConeTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ConeToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveConeTool(functionParam)
        

    def SetConeToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ConeToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetConeToolVisibility(functionParam)
        

    def UpdateConeTool(self,  ConeToolEntityInfo: ConeToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ConeToolEntityInfo_ConeToolEntityInfo(This=self.__modelRef,  Input1=(ConeToolEntityInfo.to_proto() if hasattr(ConeToolEntityInfo, 'to_proto') else ConeToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateConeTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 