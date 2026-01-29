from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .SetEntityInfoVal import SetEntityInfoVal

class SetEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_SetEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        
    
    def GetValue(self) -> SetEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.SetEntityInfo()
        ret.MergeFromString(bytes.data)
        return SetEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
 