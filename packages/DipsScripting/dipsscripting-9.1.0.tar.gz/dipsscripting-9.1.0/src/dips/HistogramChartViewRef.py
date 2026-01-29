from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .HistogramChartViewVal import HistogramChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class HistogramChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_HistogramChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__HistogramServicesStubLocal = DipsAPI_pb2_grpc.HistogramServicesStub(channelToConnectOn)

    
    def GetValue(self) -> HistogramChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.HistogramChartView()
        ret.MergeFromString(bytes.data)
        return HistogramChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseHistogramView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_HistogramChartView(This=self.__modelRef)
        ret = self.__HistogramServicesStubLocal.CloseHistogramView(functionParam)
        

    def GetActivePoleDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_HistogramChartView(This=self.__modelRef)
        ret = self.__HistogramServicesStubLocal.GetActivePoleDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActivePoleDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_HistogramChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__HistogramServicesStubLocal.SetActivePoleDataFilter(functionParam)
        

 