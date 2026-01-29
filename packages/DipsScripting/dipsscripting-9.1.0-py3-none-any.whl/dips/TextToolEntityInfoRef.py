from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .TextToolEntityInfoVal import TextToolEntityInfoVal
from .TextToolEntityInfoVal import TextToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class TextToolEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_TextToolEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__EntityServicesStubLocal = DipsAPI_pb2_grpc.EntityServicesStub(channelToConnectOn)

    
    def GetValue(self) -> TextToolEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.TextToolEntityInfo()
        ret.MergeFromString(bytes.data)
        return TextToolEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def RemoveTextTool(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TextToolEntityInfo(This=self.__modelRef)
        ret = self.__EntityServicesStubLocal.RemoveTextTool(functionParam)
        

    def SetTextToolVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TextToolEntityInfo_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__EntityServicesStubLocal.SetTextToolVisibility(functionParam)
        

    def UpdateTextTool(self,  TextToolEntityInfo: TextToolEntityInfoVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_TextToolEntityInfo_TextToolEntityInfo(This=self.__modelRef,  Input1=(TextToolEntityInfo.to_proto() if hasattr(TextToolEntityInfo, 'to_proto') else TextToolEntityInfo))
        ret = self.__EntityServicesStubLocal.UpdateTextTool(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

 