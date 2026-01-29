from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .JointFrequencyChartViewVal import JointFrequencyChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class JointFrequencyChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_JointFrequencyChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__JointFrequencyChartServicesStubLocal = DipsAPI_pb2_grpc.JointFrequencyChartServicesStub(channelToConnectOn)

    
    def GetValue(self) -> JointFrequencyChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.JointFrequencyChartView()
        ret.MergeFromString(bytes.data)
        return JointFrequencyChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseJointFrequencyChartView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_JointFrequencyChartView(This=self.__modelRef)
        ret = self.__JointFrequencyChartServicesStubLocal.CloseJointFrequencyChartView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_JointFrequencyChartView(This=self.__modelRef)
        ret = self.__JointFrequencyChartServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_JointFrequencyChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__JointFrequencyChartServicesStubLocal.SetActiveDataFilter(functionParam)
        

 