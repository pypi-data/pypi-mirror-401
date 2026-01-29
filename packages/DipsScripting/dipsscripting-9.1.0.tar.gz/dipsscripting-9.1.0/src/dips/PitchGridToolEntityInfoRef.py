from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .PitchGridToolEntityInfoVal import PitchGridToolEntityInfoVal
from .PitchGridToolEntityInfoVal import PitchGridToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class PitchGridToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_PitchGridToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> PitchGridToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.PitchGridToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return PitchGridToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemovePitchGridTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PitchGridToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemovePitchGridTool(functionParam)
        

    def SetPitchGridToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PitchGridToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetPitchGridToolVisibility(functionParam)
        

    def UpdatePitchGridTool(self,  PitchGridToolEntityInfo: PitchGridToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_PitchGridToolEntityInfo_PitchGridToolEntityInfo(This=self.__modelRef,  Input1=(PitchGridToolEntityInfo.to_proto() if hasattr(PitchGridToolEntityInfo, 'to_proto') else PitchGridToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdatePitchGridTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 