from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .QualitativeQuantitativeChartViewVal import QualitativeQuantitativeChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class QualitativeQuantitativeChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_QualitativeQuantitativeChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__QualitativeQuantitativeChartServicesStubLocal = DipsAPI_pb2_grpc.QualitativeQuantitativeChartServicesStub(channelToConnectOn)

    
    def GetValue(self) -> QualitativeQuantitativeChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.QualitativeQuantitativeChartView()
        ret.MergeFromString(bytes.data)
        return QualitativeQuantitativeChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseQualitativeQuantitativeChartView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_QualitativeQuantitativeChartView(This=self.__modelRef)
        ret = self.__QualitativeQuantitativeChartServicesStubLocal.CloseQualitativeQuantitativeChartView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_QualitativeQuantitativeChartView(This=self.__modelRef)
        ret = self.__QualitativeQuantitativeChartServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_QualitativeQuantitativeChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__QualitativeQuantitativeChartServicesStubLocal.SetActiveDataFilter(functionParam)
        

 