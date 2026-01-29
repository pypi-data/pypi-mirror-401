from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .RectangleToolEntityInfoVal import RectangleToolEntityInfoVal
from .RectangleToolEntityInfoVal import RectangleToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class RectangleToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_RectangleToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> RectangleToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.RectangleToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return RectangleToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveRectangleTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RectangleToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveRectangleTool(functionParam)
        

    def SetRectangleToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RectangleToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetRectangleToolVisibility(functionParam)
        

    def UpdateRectangleTool(self,  RectangleToolEntityInfo: RectangleToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RectangleToolEntityInfo_RectangleToolEntityInfo(This=self.__modelRef,  Input1=(RectangleToolEntityInfo.to_proto() if hasattr(RectangleToolEntityInfo, 'to_proto') else RectangleToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateRectangleTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 