from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .LineToolEntityInfoVal import LineToolEntityInfoVal
from .LineToolEntityInfoVal import LineToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class LineToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_LineToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> LineToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.LineToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return LineToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveLineTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_LineToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveLineTool(functionParam)
        

    def SetLineToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_LineToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetLineToolVisibility(functionParam)
        

    def UpdateLineTool(self,  LineToolEntityInfo: LineToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_LineToolEntityInfo_LineToolEntityInfo(This=self.__modelRef,  Input1=(LineToolEntityInfo.to_proto() if hasattr(LineToolEntityInfo, 'to_proto') else LineToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateLineTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 