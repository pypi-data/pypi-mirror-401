from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .CumulativeChartViewVal import CumulativeChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class CumulativeChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_CumulativeChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__CumulativeChartServicesStubLocal = DipsAPI_pb2_grpc.CumulativeChartServicesStub(channelToConnectOn)

    
    def GetValue(self) -> CumulativeChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.CumulativeChartView()
        ret.MergeFromString(bytes.data)
        return CumulativeChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseCumulativeChartView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_CumulativeChartView(This=self.__modelRef)
        ret = self.__CumulativeChartServicesStubLocal.CloseCumulativeChartView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_CumulativeChartView(This=self.__modelRef)
        ret = self.__CumulativeChartServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_CumulativeChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__CumulativeChartServicesStubLocal.SetActiveDataFilter(functionParam)
        

 