from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .ProjStubVal import ProjStubVal
from .CumulativeChartViewRef import CumulativeChartViewRef
from .CumulativeChartViewRef import CumulativeChartViewRef as CumulativeChartView_RefType
from .CumulativeChartViewVal import CumulativeChartViewVal
from .DataDescriptorVal import DataDescriptorVal
from .DataFilterRef import DataFilterRef
from .FoldEntityInfoRef import FoldEntityInfoRef as FoldEntityInfo_RefType
from .FoldEntityInfoVal import FoldEntityInfoVal
from .HistogramChartViewRef import HistogramChartViewRef
from .HistogramChartViewRef import HistogramChartViewRef as HistogramChartView_RefType
from .HistogramChartViewVal import HistogramChartViewVal
from .JointFrequencyChartViewRef import JointFrequencyChartViewRef
from .JointFrequencyChartViewRef import JointFrequencyChartViewRef as JointFrequencyChartView_RefType
from .JointFrequencyChartViewVal import JointFrequencyChartViewVal
from .JointSpacingChartViewRef import JointSpacingChartViewRef
from .JointSpacingChartViewRef import JointSpacingChartViewRef as JointSpacingChartView_RefType
from .JointSpacingChartViewVal import JointSpacingChartViewVal
from .OrientationDataSetRef import OrientationDataSetRef
from .OrientationDataSetRef import OrientationDataSetRef as OrientationDataSet_RefType
from .OrientationDataSetVal import OrientationDataSetVal
from .PlaneEntityInfoRef import PlaneEntityInfoRef as PlaneEntityInfo_RefType
from .PlaneEntityInfoVal import PlaneEntityInfoVal
from .ProcessedDataVal import ProcessedDataVal
from .QualitativeQuantitativeChartViewRef import QualitativeQuantitativeChartViewRef
from .QualitativeQuantitativeChartViewRef import QualitativeQuantitativeChartViewRef as QualitativeQuantitativeChartView_RefType
from .QualitativeQuantitativeChartViewVal import QualitativeQuantitativeChartViewVal
from .RQDAnalysisChartViewRef import RQDAnalysisChartViewRef
from .RQDAnalysisChartViewRef import RQDAnalysisChartViewRef as RQDAnalysisChartView_RefType
from .RQDAnalysisChartViewVal import RQDAnalysisChartViewVal
from .RosetteViewRef import RosetteViewRef
from .RosetteViewRef import RosetteViewRef as RosetteView_RefType
from .ScatterChartViewRef import ScatterChartViewRef
from .ScatterChartViewRef import ScatterChartViewRef as ScatterChartView_RefType
from .ScatterChartViewVal import ScatterChartViewVal
from .SetEntityInfoRef import SetEntityInfoRef
from .SetEntityInfoRef import SetEntityInfoRef as SetEntityInfo_RefType
from .SetEntityInfoVal import SetEntityInfoVal
from .Stereonet2DViewRef import Stereonet2DViewRef
from .Stereonet2DViewRef import Stereonet2DViewRef as Stereonet2DView_RefType
from .Stereonet3DViewRef import Stereonet3DViewRef
from .Stereonet3DViewRef import Stereonet3DViewRef as Stereonet3DView_RefType
from .ValidatableResultVal import ValidatableResultVal
from .WeightingSettingsVal import WeightingSettingsVal

class ProjStubRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_ProjStub):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__CumulativeChartServicesStubLocal = DipsAPI_pb2_grpc.CumulativeChartServicesStub(channelToConnectOn)
        self.__HistogramServicesStubLocal = DipsAPI_pb2_grpc.HistogramServicesStub(channelToConnectOn)
        self.__JointFrequencyChartServicesStubLocal = DipsAPI_pb2_grpc.JointFrequencyChartServicesStub(channelToConnectOn)
        self.__JointSpacingChartServicesStubLocal = DipsAPI_pb2_grpc.JointSpacingChartServicesStub(channelToConnectOn)
        self.__ProcessedDataManagerStubLocal = DipsAPI_pb2_grpc.ProcessedDataManagerStub(channelToConnectOn)
        self.__ProjStubServiceStubLocal = DipsAPI_pb2_grpc.ProjStubServiceStub(channelToConnectOn)
        self.__QualitativeQuantitativeChartServicesStubLocal = DipsAPI_pb2_grpc.QualitativeQuantitativeChartServicesStub(channelToConnectOn)
        self.__RQDAnalysisChartServicesStubLocal = DipsAPI_pb2_grpc.RQDAnalysisChartServicesStub(channelToConnectOn)
        self.__RosetteServicesStubLocal = DipsAPI_pb2_grpc.RosetteServicesStub(channelToConnectOn)
        self.__ScatterChartServicesStubLocal = DipsAPI_pb2_grpc.ScatterChartServicesStub(channelToConnectOn)
        self.__SetServicesStubLocal = DipsAPI_pb2_grpc.SetServicesStub(channelToConnectOn)
        self.__Stereonet2DServicesStubLocal = DipsAPI_pb2_grpc.Stereonet2DServicesStub(channelToConnectOn)
        self.__Stereonet3DServicesStubLocal = DipsAPI_pb2_grpc.Stereonet3DServicesStub(channelToConnectOn)

    
    def GetValue(self) -> ProjStubVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.ProjStub()
        ret.MergeFromString(bytes.data)
        return ProjStubVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def CreateCumulativeChartView(self,  CumulativeChartView: CumulativeChartViewVal) -> CumulativeChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_CumulativeChartView(This=self.__modelRef,  Input1=(CumulativeChartView.to_proto() if hasattr(CumulativeChartView, 'to_proto') else CumulativeChartView))
        ret = self.__CumulativeChartServicesStubLocal.CreateCumulativeChartView(functionParam)
        
        return CumulativeChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetCumulativeChartViewList(self) -> List[CumulativeChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__CumulativeChartServicesStubLocal.GetCumulativeChartViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( CumulativeChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateHistogramView(self,  HistogramChartView: HistogramChartViewVal) -> HistogramChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_HistogramChartView(This=self.__modelRef,  Input1=(HistogramChartView.to_proto() if hasattr(HistogramChartView, 'to_proto') else HistogramChartView))
        ret = self.__HistogramServicesStubLocal.CreateHistogramView(functionParam)
        
        return HistogramChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetHistogramViewList(self) -> List[HistogramChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__HistogramServicesStubLocal.GetHistogramViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( HistogramChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateJointFrequencyChartView(self,  JointFrequencyChartView: JointFrequencyChartViewVal) -> JointFrequencyChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_JointFrequencyChartView(This=self.__modelRef,  Input1=(JointFrequencyChartView.to_proto() if hasattr(JointFrequencyChartView, 'to_proto') else JointFrequencyChartView))
        ret = self.__JointFrequencyChartServicesStubLocal.CreateJointFrequencyChartView(functionParam)
        
        return JointFrequencyChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetJointFrequencyChartViewList(self) -> List[JointFrequencyChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__JointFrequencyChartServicesStubLocal.GetJointFrequencyChartViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( JointFrequencyChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateJointSpacingChartView(self,  JointSpacingChartView: JointSpacingChartViewVal) -> JointSpacingChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_JointSpacingChartView(This=self.__modelRef,  Input1=(JointSpacingChartView.to_proto() if hasattr(JointSpacingChartView, 'to_proto') else JointSpacingChartView))
        ret = self.__JointSpacingChartServicesStubLocal.CreateJointSpacingChartView(functionParam)
        
        return JointSpacingChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetJointSpacingChartViewList(self) -> List[JointSpacingChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__JointSpacingChartServicesStubLocal.GetJointSpacingChartViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( JointSpacingChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def NumericRequest(self,  DataDescriptor: DataDescriptorVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_DataDescriptor(This=self.__modelRef,  Input1=(DataDescriptor.to_proto() if hasattr(DataDescriptor, 'to_proto') else DataDescriptor))
        ret = self.__ProcessedDataManagerStubLocal.NumericRequest(functionParam)
        
        return ret
        

    def PlanarRequest(self) -> ProcessedDataVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProcessedDataManagerStubLocal.PlanarRequest(functionParam)
        
        return ProcessedDataVal.from_proto(ret)
        

    def TextRequest(self,  DataDescriptor: DataDescriptorVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_DataDescriptor(This=self.__modelRef,  Input1=(DataDescriptor.to_proto() if hasattr(DataDescriptor, 'to_proto') else DataDescriptor))
        ret = self.__ProcessedDataManagerStubLocal.TextRequest(functionParam)
        
        return ret
        

    def AddFold(self,  FoldEntityInfo: FoldEntityInfoVal) -> FoldEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_FoldEntityInfo(This=self.__modelRef,  Input1=(FoldEntityInfo.to_proto() if hasattr(FoldEntityInfo, 'to_proto') else FoldEntityInfo))
        ret = self.__ProjStubServiceStubLocal.AddFold(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return FoldEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddTraverse(self,  OrientationDataSet: OrientationDataSetVal) -> OrientationDataSet_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_OrientationDataSet(This=self.__modelRef,  Input1=(OrientationDataSet.to_proto() if hasattr(OrientationDataSet, 'to_proto') else OrientationDataSet))
        ret = self.__ProjStubServiceStubLocal.AddTraverse(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return OrientationDataSet_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddUserPlane(self,  PlaneEntityInfo: PlaneEntityInfoVal) -> PlaneEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_PlaneEntityInfo(This=self.__modelRef,  Input1=(PlaneEntityInfo.to_proto() if hasattr(PlaneEntityInfo, 'to_proto') else PlaneEntityInfo))
        ret = self.__ProjStubServiceStubLocal.AddUserPlane(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PlaneEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def Get2DStereonets(self) -> List[Stereonet2DViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.Get2DStereonets(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( Stereonet2DViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def Get3DStereonets(self) -> List[Stereonet3DViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.Get3DStereonets(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( Stereonet3DViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetDataFilters(self) -> List[DataFilterRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.GetDataFilters(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( DataFilterRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetReportingConvention(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.GetReportingConvention(functionParam)
        
        return ret
        

    def GetRosettes(self) -> List[RosetteViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.GetRosettes(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( RosetteViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetTraverses(self) -> List[OrientationDataSetRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.GetTraverses(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( OrientationDataSetRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetUnitSystem(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.GetUnitSystem(functionParam)
        
        return ret
        

    def GetWeightingOptions(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ProjStubServiceStubLocal.GetWeightingOptions(functionParam)
        
        return ret
        

    def RemoveTraverse(self,  OrientationDataSet: OrientationDataSet_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_ProtoReference_OrientationDataSet(This=self.__modelRef,  Input1=OrientationDataSet.get_model_ref())
        ret = self.__ProjStubServiceStubLocal.RemoveTraverse(functionParam)
        

    def SaveProject(self,  String: str) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_String(This=self.__modelRef,  Input1=(DipsAPI_pb2.String(Value=String) if hasattr(DipsAPI_pb2, 'String') else String))
        ret = self.__ProjStubServiceStubLocal.SaveProject(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetReportingConvention(self,  eOrientationConvention: DipsAPI_pb2.eOrientationConvention):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_eOrientationConvention(This=self.__modelRef,  Input1=eOrientationConvention)
        ret = self.__ProjStubServiceStubLocal.SetReportingConvention(functionParam)
        

    def SetUnitSystem(self,  eUnitSystem: DipsAPI_pb2.eUnitSystem):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_eUnitSystem(This=self.__modelRef,  Input1=eUnitSystem)
        ret = self.__ProjStubServiceStubLocal.SetUnitSystem(functionParam)
        

    def SetWeightingOptions(self,  WeightingSettings: WeightingSettingsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_WeightingSettings(This=self.__modelRef,  Input1=(WeightingSettings.to_proto() if hasattr(WeightingSettings, 'to_proto') else WeightingSettings))
        ret = self.__ProjStubServiceStubLocal.SetWeightingOptions(functionParam)
        

    def CreateQualitativeQuantitativeChartView(self,  QualitativeQuantitativeChartView: QualitativeQuantitativeChartViewVal) -> QualitativeQuantitativeChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_QualitativeQuantitativeChartView(This=self.__modelRef,  Input1=(QualitativeQuantitativeChartView.to_proto() if hasattr(QualitativeQuantitativeChartView, 'to_proto') else QualitativeQuantitativeChartView))
        ret = self.__QualitativeQuantitativeChartServicesStubLocal.CreateQualitativeQuantitativeChartView(functionParam)
        
        return QualitativeQuantitativeChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetQualitativeQuantitativeChartViewList(self) -> List[QualitativeQuantitativeChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__QualitativeQuantitativeChartServicesStubLocal.GetQualitativeQuantitativeChartViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( QualitativeQuantitativeChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateRQDAnalysisChartView(self,  RQDAnalysisChartView: RQDAnalysisChartViewVal) -> RQDAnalysisChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_RQDAnalysisChartView(This=self.__modelRef,  Input1=(RQDAnalysisChartView.to_proto() if hasattr(RQDAnalysisChartView, 'to_proto') else RQDAnalysisChartView))
        ret = self.__RQDAnalysisChartServicesStubLocal.CreateRQDAnalysisChartView(functionParam)
        
        return RQDAnalysisChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetRQDAnalysisChartViewList(self) -> List[RQDAnalysisChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__RQDAnalysisChartServicesStubLocal.GetRQDAnalysisChartViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( RQDAnalysisChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateRosetteView(self) -> RosetteView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.CreateRosetteView(functionParam)
        
        return RosetteView_RefType(self.__channelToConnectOn, ret)
        

    def CreateScatterChartView(self,  ScatterChartView: ScatterChartViewVal) -> ScatterChartView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_ScatterChartView(This=self.__modelRef,  Input1=(ScatterChartView.to_proto() if hasattr(ScatterChartView, 'to_proto') else ScatterChartView))
        ret = self.__ScatterChartServicesStubLocal.CreateScatterChartView(functionParam)
        
        return ScatterChartView_RefType(self.__channelToConnectOn, ret)
        

    def GetScatterChartViewList(self) -> List[ScatterChartViewRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__ScatterChartServicesStubLocal.GetScatterChartViewList(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( ScatterChartViewRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateSetWindow(self,  SetEntityInfo: SetEntityInfoVal) -> SetEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_SetEntityInfo(This=self.__modelRef,  Input1=(SetEntityInfo.to_proto() if hasattr(SetEntityInfo, 'to_proto') else SetEntityInfo))
        ret = self.__SetServicesStubLocal.CreateSetWindow(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return SetEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def DeleteSet(self,  SetEntityInfo: SetEntityInfo_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub_ProtoReference_SetEntityInfo(This=self.__modelRef,  Input1=SetEntityInfo.get_model_ref())
        ret = self.__SetServicesStubLocal.DeleteSet(functionParam)
        

    def GetAllSets(self) -> List[SetEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__SetServicesStubLocal.GetAllSets(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( SetEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def CreateStereonet2DView(self) -> Stereonet2DView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.CreateStereonet2DView(functionParam)
        
        return Stereonet2DView_RefType(self.__channelToConnectOn, ret)
        

    def CreateStereonet3DView(self) -> Stereonet3DView_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_ProjStub(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.CreateStereonet3DView(functionParam)
        
        return Stereonet3DView_RefType(self.__channelToConnectOn, ret)
        

 