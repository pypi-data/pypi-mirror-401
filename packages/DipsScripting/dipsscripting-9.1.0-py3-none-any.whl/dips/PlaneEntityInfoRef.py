from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .PlaneEntityInfoVal import PlaneEntityInfoVal

class PlaneEntityInfoRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_PlaneEntityInfo):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        
    
    def GetValue(self) -> PlaneEntityInfoVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.PlaneEntityInfo()
        ret.MergeFromString(bytes.data)
        return PlaneEntityInfoVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
 