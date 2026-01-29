from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .MeasureAngleToolEntityInfoVal import MeasureAngleToolEntityInfoVal
from .MeasureAngleToolEntityInfoVal import MeasureAngleToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class MeasureAngleToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_MeasureAngleToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> MeasureAngleToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.MeasureAngleToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return MeasureAngleToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveMeasureAngleTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_MeasureAngleToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveMeasureAngleTool(functionParam)
        

    def SetMeasureAngleToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_MeasureAngleToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetMeasureAngleToolVisibility(functionParam)
        

    def UpdateMeasureAngleTool(self,  MeasureAngleToolEntityInfo: MeasureAngleToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_MeasureAngleToolEntityInfo_MeasureAngleToolEntityInfo(This=self.__modelRef,  Input1=(MeasureAngleToolEntityInfo.to_proto() if hasattr(MeasureAngleToolEntityInfo, 'to_proto') else MeasureAngleToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateMeasureAngleTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 