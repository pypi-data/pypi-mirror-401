from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .LineIntersectionCalculatorToolEntityInfoVal import LineIntersectionCalculatorToolEntityInfoVal
from .LineIntersectionCalculatorToolEntityInfoVal import LineIntersectionCalculatorToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class LineIntersectionCalculatorToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_LineIntersectionCalculatorToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> LineIntersectionCalculatorToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.LineIntersectionCalculatorToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return LineIntersectionCalculatorToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveLineIntersectionCalculatorTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_LineIntersectionCalculatorToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveLineIntersectionCalculatorTool(functionParam)
        

    def SetLineIntersectionCalculatorToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_LineIntersectionCalculatorToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetLineIntersectionCalculatorToolVisibility(functionParam)
        

    def UpdateLineIntersectionCalculatorTool(self,  LineIntersectionCalculatorToolEntityInfo: LineIntersectionCalculatorToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_LineIntersectionCalculatorToolEntityInfo_LineIntersectionCalculatorToolEntityInfo(This=self.__modelRef,  Input1=(LineIntersectionCalculatorToolEntityInfo.to_proto() if hasattr(LineIntersectionCalculatorToolEntityInfo, 'to_proto') else LineIntersectionCalculatorToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateLineIntersectionCalculatorTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 