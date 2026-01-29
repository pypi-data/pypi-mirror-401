from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .TrendLineToolEntityInfoVal import TrendLineToolEntityInfoVal
from .TrendLineToolEntityInfoVal import TrendLineToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class TrendLineToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_TrendLineToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> TrendLineToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.TrendLineToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return TrendLineToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveTrendLineTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TrendLineToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveTrendLineTool(functionParam)
        

    def SetTrendLineToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TrendLineToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetTrendLineToolVisibility(functionParam)
        

    def UpdateTrendLineTool(self,  TrendLineToolEntityInfo: TrendLineToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TrendLineToolEntityInfo_TrendLineToolEntityInfo(This=self.__modelRef,  Input1=(TrendLineToolEntityInfo.to_proto() if hasattr(TrendLineToolEntityInfo, 'to_proto') else TrendLineToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateTrendLineTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 