from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from .ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class ArrowToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_ArrowToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> ArrowToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.ArrowToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return ArrowToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveArrowTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ArrowToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveArrowTool(functionParam)
        

    def SetArrowToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ArrowToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetArrowToolVisibility(functionParam)
        

    def UpdateArrowTool(self,  ArrowToolEntityInfo: ArrowToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ArrowToolEntityInfo_ArrowToolEntityInfo(This=self.__modelRef,  Input1=(ArrowToolEntityInfo.to_proto() if hasattr(ArrowToolEntityInfo, 'to_proto') else ArrowToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateArrowTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 