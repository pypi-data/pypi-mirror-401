from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .JointSpacingChartViewVal import JointSpacingChartViewVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType

class JointSpacingChartViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_JointSpacingChartView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__JointSpacingChartServicesStubLocal = DipsAPI_pb2_grpc.JointSpacingChartServicesStub(channelToConnectOn)

    
    def GetValue(self) -> JointSpacingChartViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.JointSpacingChartView()
        ret.MergeFromString(bytes.data)
        return JointSpacingChartViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CloseJointSpacingChartView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_JointSpacingChartView(This=self.__modelRef)
        ret = self.__JointSpacingChartServicesStubLocal.CloseJointSpacingChartView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_JointSpacingChartView(This=self.__modelRef)
        ret = self.__JointSpacingChartServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_JointSpacingChartView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__JointSpacingChartServicesStubLocal.SetActiveDataFilter(functionParam)
        

 