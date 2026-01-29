from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .EllipseToolEntityInfoVal import EllipseToolEntityInfoVal
from .EllipseToolEntityInfoVal import EllipseToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class EllipseToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_EllipseToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> EllipseToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.EllipseToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return EllipseToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveEllipseTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_EllipseToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveEllipseTool(functionParam)
        

    def SetEllipseToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_EllipseToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetEllipseToolVisibility(functionParam)
        

    def UpdateEllipseTool(self,  EllipseToolEntityInfo: EllipseToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_EllipseToolEntityInfo_EllipseToolEntityInfo(This=self.__modelRef,  Input1=(EllipseToolEntityInfo.to_proto() if hasattr(EllipseToolEntityInfo, 'to_proto') else EllipseToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateEllipseTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 