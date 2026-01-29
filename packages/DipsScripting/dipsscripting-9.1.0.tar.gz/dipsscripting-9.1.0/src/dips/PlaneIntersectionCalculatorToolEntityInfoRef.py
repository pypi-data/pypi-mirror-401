from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .PlaneIntersectionCalculatorToolEntityInfoVal import PlaneIntersectionCalculatorToolEntityInfoVal
from .PlaneIntersectionCalculatorToolEntityInfoVal import PlaneIntersectionCalculatorToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class PlaneIntersectionCalculatorToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_PlaneIntersectionCalculatorToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> PlaneIntersectionCalculatorToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.PlaneIntersectionCalculatorToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return PlaneIntersectionCalculatorToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemovePlaneIntersectionCalculatorTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PlaneIntersectionCalculatorToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemovePlaneIntersectionCalculatorTool(functionParam)
        

    def SetPlaneIntersectionCalculatorToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PlaneIntersectionCalculatorToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetPlaneIntersectionCalculatorToolVisibility(functionParam)
        

    def UpdatePlaneIntersectionCalculatorTool(self,  PlaneIntersectionCalculatorToolEntityInfo: PlaneIntersectionCalculatorToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PlaneIntersectionCalculatorToolEntityInfo_PlaneIntersectionCalculatorToolEntityInfo(This=self.__modelRef,  Input1=(PlaneIntersectionCalculatorToolEntityInfo.to_proto() if hasattr(PlaneIntersectionCalculatorToolEntityInfo, 'to_proto') else PlaneIntersectionCalculatorToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdatePlaneIntersectionCalculatorTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 