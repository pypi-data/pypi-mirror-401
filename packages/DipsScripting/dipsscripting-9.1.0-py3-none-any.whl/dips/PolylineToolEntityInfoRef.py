from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .PolylineToolEntityInfoVal import PolylineToolEntityInfoVal
from .PolylineToolEntityInfoVal import PolylineToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class PolylineToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_PolylineToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> PolylineToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.PolylineToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return PolylineToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemovePolylineTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PolylineToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemovePolylineTool(functionParam)
        

    def SetPolylineToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PolylineToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetPolylineToolVisibility(functionParam)
        

    def UpdatePolylineTool(self,  PolylineToolEntityInfo: PolylineToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PolylineToolEntityInfo_PolylineToolEntityInfo(This=self.__modelRef,  Input1=(PolylineToolEntityInfo.to_proto() if hasattr(PolylineToolEntityInfo, 'to_proto') else PolylineToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdatePolylineTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 