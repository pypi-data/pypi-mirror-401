from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .PolygonToolEntityInfoVal import PolygonToolEntityInfoVal
from .PolygonToolEntityInfoVal import PolygonToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class PolygonToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_PolygonToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> PolygonToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.PolygonToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return PolygonToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemovePolygonTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PolygonToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemovePolygonTool(functionParam)
        

    def SetPolygonToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PolygonToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetPolygonToolVisibility(functionParam)
        

    def UpdatePolygonTool(self,  PolygonToolEntityInfo: PolygonToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PolygonToolEntityInfo_PolygonToolEntityInfo(This=self.__modelRef,  Input1=(PolygonToolEntityInfo.to_proto() if hasattr(PolygonToolEntityInfo, 'to_proto') else PolygonToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdatePolygonTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 