from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .ScatterChartViewVal import ScatterChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class ScatterChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_ScatterChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__ScatterChartServicesStubLocal = DipsAPI_pb2_grpc.ScatterChartServicesStub(channelToConnectOn)

    
    def GetValue(self) -> ScatterChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.ScatterChartView()
        ret.MergeFromString(bytes.data)
        return ScatterChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseScatterChartView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ScatterChartView(This=self.__modelRef)
        ret = self.__ScatterChartServicesStubLocal.CloseScatterChartView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ScatterChartView(This=self.__modelRef)
        ret = self.__ScatterChartServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ScatterChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__ScatterChartServicesStubLocal.SetActiveDataFilter(functionParam)
        

 