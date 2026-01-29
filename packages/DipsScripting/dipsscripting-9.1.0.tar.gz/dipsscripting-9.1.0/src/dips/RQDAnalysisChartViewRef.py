from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .RQDAnalysisChartViewVal import RQDAnalysisChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class RQDAnalysisChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_RQDAnalysisChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__RQDAnalysisChartServicesStubLocal = DipsAPI_pb2_grpc.RQDAnalysisChartServicesStub(channelToConnectOn)

    
    def GetValue(self) -> RQDAnalysisChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.RQDAnalysisChartView()
        ret.MergeFromString(bytes.data)
        return RQDAnalysisChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseRQDAnalysisChartView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RQDAnalysisChartView(This=self.__modelRef)
        ret = self.__RQDAnalysisChartServicesStubLocal.CloseRQDAnalysisChartView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RQDAnalysisChartView(This=self.__modelRef)
        ret = self.__RQDAnalysisChartServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RQDAnalysisChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__RQDAnalysisChartServicesStubLocal.SetActiveDataFilter(functionParam)
        

 