from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .Stereonet3DViewVal import Stereonet3DViewVal
from .ArrowToolEntityInfoRef import ArrowToolEntityInfoRef as ArrowToolEntityInfo_RefType
from .ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from .ConeToolEntityInfoRef import ConeToolEntityInfoRef as ConeToolEntityInfo_RefType
from .ConeToolEntityInfoVal import ConeToolEntityInfoVal
from .ContourEntityVisibilityVal import ContourEntityVisibilityVal
from .ContourOptionsVal import ContourOptionsVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType
from .EllipseToolEntityInfoRef import EllipseToolEntityInfoRef as EllipseToolEntityInfo_RefType
from .EllipseToolEntityInfoVal import EllipseToolEntityInfoVal
from .FoldEntityVisibilityRef import FoldEntityVisibilityRef
from .FoldWindowEntityVisibilityRef import FoldWindowEntityVisibilityRef
from .GlobalPlaneEntityVisibilityVal import GlobalPlaneEntityVisibilityVal
from .IntersectionOptionsVal import IntersectionOptionsVal
from .LineIntersectionCalculatorToolEntityInfoRef import LineIntersectionCalculatorToolEntityInfoRef as LineIntersectionCalculatorToolEntityInfo_RefType
from .LineIntersectionCalculatorToolEntityInfoVal import LineIntersectionCalculatorToolEntityInfoVal
from .LineToolEntityInfoRef import LineToolEntityInfoRef as LineToolEntityInfo_RefType
from .LineToolEntityInfoVal import LineToolEntityInfoVal
from .MeasureAngleToolEntityInfoRef import MeasureAngleToolEntityInfoRef as MeasureAngleToolEntityInfo_RefType
from .MeasureAngleToolEntityInfoVal import MeasureAngleToolEntityInfoVal
from .PitchGridToolEntityInfoRef import PitchGridToolEntityInfoRef as PitchGridToolEntityInfo_RefType
from .PitchGridToolEntityInfoVal import PitchGridToolEntityInfoVal
from .PlaneEntityVisibilityRef import PlaneEntityVisibilityRef
from .PlaneIntersectionCalculatorToolEntityInfoRef import PlaneIntersectionCalculatorToolEntityInfoRef as PlaneIntersectionCalculatorToolEntityInfo_RefType
from .PlaneIntersectionCalculatorToolEntityInfoVal import PlaneIntersectionCalculatorToolEntityInfoVal
from .PoleEntityOptionsVal import PoleEntityOptionsVal
from .PolygonToolEntityInfoRef import PolygonToolEntityInfoRef as PolygonToolEntityInfo_RefType
from .PolygonToolEntityInfoVal import PolygonToolEntityInfoVal
from .PolylineToolEntityInfoRef import PolylineToolEntityInfoRef as PolylineToolEntityInfo_RefType
from .PolylineToolEntityInfoVal import PolylineToolEntityInfoVal
from .QuantitativeContourSettingsVal import QuantitativeContourSettingsVal
from .RectangleToolEntityInfoRef import RectangleToolEntityInfoRef as RectangleToolEntityInfo_RefType
from .RectangleToolEntityInfoVal import RectangleToolEntityInfoVal
from .SetEntityVisibilityRef import SetEntityVisibilityRef
from .SetVersusSetVal import SetVersusSetVal
from .SetWindowEntityVisibilityRef import SetWindowEntityVisibilityRef
from .StereonetOverlayEntityVisibilityVal import StereonetOverlayEntityVisibilityVal
from .SymbolicSettingsVal import SymbolicSettingsVal
from .TextToolEntityInfoRef import TextToolEntityInfoRef as TextToolEntityInfo_RefType
from .TextToolEntityInfoVal import TextToolEntityInfoVal
from .TraverseEntityVisibilityRef import TraverseEntityVisibilityRef
from .TrendLineToolEntityInfoRef import TrendLineToolEntityInfoRef as TrendLineToolEntityInfo_RefType
from .TrendLineToolEntityInfoVal import TrendLineToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal
from .VectorDensityContourSettingsVal import VectorDensityContourSettingsVal

class Stereonet3DViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_Stereonet3DView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__Stereonet3DServicesStubLocal = DipsAPI_pb2_grpc.Stereonet3DServicesStub(channelToConnectOn)

    
    def GetValue(self) -> Stereonet3DViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.Stereonet3DView()
        ret.MergeFromString(bytes.data)
        return Stereonet3DViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def AddStereonet3DArrowTool(self,  ArrowToolEntityInfo: ArrowToolEntityInfoVal) -> ArrowToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ArrowToolEntityInfo(This=self.__modelRef,  Input1=(ArrowToolEntityInfo.to_proto() if hasattr(ArrowToolEntityInfo, 'to_proto') else ArrowToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DArrowTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return ArrowToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DConeTool(self,  ConeToolEntityInfo: ConeToolEntityInfoVal) -> ConeToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ConeToolEntityInfo(This=self.__modelRef,  Input1=(ConeToolEntityInfo.to_proto() if hasattr(ConeToolEntityInfo, 'to_proto') else ConeToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DConeTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return ConeToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DEllipseTool(self,  EllipseToolEntityInfo: EllipseToolEntityInfoVal) -> EllipseToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_EllipseToolEntityInfo(This=self.__modelRef,  Input1=(EllipseToolEntityInfo.to_proto() if hasattr(EllipseToolEntityInfo, 'to_proto') else EllipseToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DEllipseTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return EllipseToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DLineIntersectionCalculatorTool(self,  LineIntersectionCalculatorToolEntityInfo: LineIntersectionCalculatorToolEntityInfoVal) -> LineIntersectionCalculatorToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_LineIntersectionCalculatorToolEntityInfo(This=self.__modelRef,  Input1=(LineIntersectionCalculatorToolEntityInfo.to_proto() if hasattr(LineIntersectionCalculatorToolEntityInfo, 'to_proto') else LineIntersectionCalculatorToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DLineIntersectionCalculatorTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return LineIntersectionCalculatorToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DLineTool(self,  LineToolEntityInfo: LineToolEntityInfoVal) -> LineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_LineToolEntityInfo(This=self.__modelRef,  Input1=(LineToolEntityInfo.to_proto() if hasattr(LineToolEntityInfo, 'to_proto') else LineToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DLineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return LineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DMeasureAngleTool(self,  MeasureAngleToolEntityInfo: MeasureAngleToolEntityInfoVal) -> MeasureAngleToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_MeasureAngleToolEntityInfo(This=self.__modelRef,  Input1=(MeasureAngleToolEntityInfo.to_proto() if hasattr(MeasureAngleToolEntityInfo, 'to_proto') else MeasureAngleToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DMeasureAngleTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return MeasureAngleToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DPitchGridTool(self,  PitchGridToolEntityInfo: PitchGridToolEntityInfoVal) -> PitchGridToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_PitchGridToolEntityInfo(This=self.__modelRef,  Input1=(PitchGridToolEntityInfo.to_proto() if hasattr(PitchGridToolEntityInfo, 'to_proto') else PitchGridToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DPitchGridTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PitchGridToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DPlaneIntersectionCalculatorTool(self,  PlaneIntersectionCalculatorToolEntityInfo: PlaneIntersectionCalculatorToolEntityInfoVal) -> PlaneIntersectionCalculatorToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_PlaneIntersectionCalculatorToolEntityInfo(This=self.__modelRef,  Input1=(PlaneIntersectionCalculatorToolEntityInfo.to_proto() if hasattr(PlaneIntersectionCalculatorToolEntityInfo, 'to_proto') else PlaneIntersectionCalculatorToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DPlaneIntersectionCalculatorTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PlaneIntersectionCalculatorToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DPolygonTool(self,  PolygonToolEntityInfo: PolygonToolEntityInfoVal) -> PolygonToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_PolygonToolEntityInfo(This=self.__modelRef,  Input1=(PolygonToolEntityInfo.to_proto() if hasattr(PolygonToolEntityInfo, 'to_proto') else PolygonToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DPolygonTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PolygonToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DPolylineTool(self,  PolylineToolEntityInfo: PolylineToolEntityInfoVal) -> PolylineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_PolylineToolEntityInfo(This=self.__modelRef,  Input1=(PolylineToolEntityInfo.to_proto() if hasattr(PolylineToolEntityInfo, 'to_proto') else PolylineToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DPolylineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PolylineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DRectangleTool(self,  RectangleToolEntityInfo: RectangleToolEntityInfoVal) -> RectangleToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_RectangleToolEntityInfo(This=self.__modelRef,  Input1=(RectangleToolEntityInfo.to_proto() if hasattr(RectangleToolEntityInfo, 'to_proto') else RectangleToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DRectangleTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return RectangleToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DTextTool(self,  TextToolEntityInfo: TextToolEntityInfoVal) -> TextToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_TextToolEntityInfo(This=self.__modelRef,  Input1=(TextToolEntityInfo.to_proto() if hasattr(TextToolEntityInfo, 'to_proto') else TextToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DTextTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return TextToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet3DTrendLineTool(self,  TrendLineToolEntityInfo: TrendLineToolEntityInfoVal) -> TrendLineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_TrendLineToolEntityInfo(This=self.__modelRef,  Input1=(TrendLineToolEntityInfo.to_proto() if hasattr(TrendLineToolEntityInfo, 'to_proto') else TrendLineToolEntityInfo))
        ret = self.__Stereonet3DServicesStubLocal.AddStereonet3DTrendLineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return TrendLineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def CloseStereonet3DView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.CloseStereonet3DView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def GetFoldEntityVisibilities(self) -> List[FoldEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetFoldEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( FoldEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetFoldWindowEntityVisibilities(self) -> List[FoldWindowEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetFoldWindowEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( FoldWindowEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetMeanSetPlaneEntityVisibilities(self) -> List[SetEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetMeanSetPlaneEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( SetEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetSetWindowEntityVisibilities(self) -> List[SetWindowEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetSetWindowEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( SetWindowEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetTraverseEntityVisibilities(self) -> List[TraverseEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetTraverseEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( TraverseEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetUserPlaneEntityVisibilities(self) -> List[PlaneEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView(This=self.__modelRef)
        ret = self.__Stereonet3DServicesStubLocal.GetUserPlaneEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PlaneEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__Stereonet3DServicesStubLocal.SetActiveDataFilter(functionParam)
        

    def SetContourEntityOptions(self,  ContourEntityVisibility: ContourEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ContourEntityVisibility(This=self.__modelRef,  Input1=(ContourEntityVisibility.to_proto() if hasattr(ContourEntityVisibility, 'to_proto') else ContourEntityVisibility))
        ret = self.__Stereonet3DServicesStubLocal.SetContourEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetContourEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetContourEntityVisibility(functionParam)
        

    def SetContourType(self,  eContourType: DipsAPI_pb2.eContourType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_eContourType(This=self.__modelRef,  Input1=eContourType)
        ret = self.__Stereonet3DServicesStubLocal.SetContourType(functionParam)
        

    def SetFoldEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetFoldEntityGroupVisibility(functionParam)
        

    def SetFoldWindowEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetFoldWindowEntityGroupVisibility(functionParam)
        

    def SetGlobalBestFitPlaneEntityOptions(self,  GlobalPlaneEntityVisibility: GlobalPlaneEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_GlobalPlaneEntityVisibility(This=self.__modelRef,  Input1=(GlobalPlaneEntityVisibility.to_proto() if hasattr(GlobalPlaneEntityVisibility, 'to_proto') else GlobalPlaneEntityVisibility))
        ret = self.__Stereonet3DServicesStubLocal.SetGlobalBestFitPlaneEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetGlobalBestFitPlaneEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetGlobalBestFitPlaneEntityVisibility(functionParam)
        

    def SetGlobalMeanPlaneEntityOptions(self,  GlobalPlaneEntityVisibility: GlobalPlaneEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_GlobalPlaneEntityVisibility(This=self.__modelRef,  Input1=(GlobalPlaneEntityVisibility.to_proto() if hasattr(GlobalPlaneEntityVisibility, 'to_proto') else GlobalPlaneEntityVisibility))
        ret = self.__Stereonet3DServicesStubLocal.SetGlobalMeanPlaneEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetGlobalMeanPlaneEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetGlobalMeanPlaneEntityVisibility(functionParam)
        

    def SetIntersectionEntityOptions(self,  IntersectionOptions: IntersectionOptionsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_IntersectionOptions(This=self.__modelRef,  Input1=(IntersectionOptions.to_proto() if hasattr(IntersectionOptions, 'to_proto') else IntersectionOptions))
        ret = self.__Stereonet3DServicesStubLocal.SetIntersectionEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetIntersectionEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetIntersectionEntityVisibility(functionParam)
        

    def SetIntersectionType(self,  eIntersectionType: DipsAPI_pb2.eIntersectionType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_eIntersectionType(This=self.__modelRef,  Input1=eIntersectionType)
        ret = self.__Stereonet3DServicesStubLocal.SetIntersectionType(functionParam)
        

    def SetIntersectionVectorContourOptions(self,  ContourOptions: ContourOptionsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ContourOptions(This=self.__modelRef,  Input1=(ContourOptions.to_proto() if hasattr(ContourOptions, 'to_proto') else ContourOptions))
        ret = self.__Stereonet3DServicesStubLocal.SetIntersectionVectorContourOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetIntersectionVectorDensityContourSettings(self,  VectorDensityContourSettings: VectorDensityContourSettingsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_VectorDensityContourSettings(This=self.__modelRef,  Input1=(VectorDensityContourSettings.to_proto() if hasattr(VectorDensityContourSettings, 'to_proto') else VectorDensityContourSettings))
        ret = self.__Stereonet3DServicesStubLocal.SetIntersectionVectorDensityContourSettings(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetIsWeighted(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetIsWeighted(functionParam)
        

    def SetMeanSetPlaneEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetMeanSetPlaneEntityGroupVisibility(functionParam)
        

    def SetPoleEntityOptions(self,  PoleEntityOptions: PoleEntityOptionsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_PoleEntityOptions(This=self.__modelRef,  Input1=(PoleEntityOptions.to_proto() if hasattr(PoleEntityOptions, 'to_proto') else PoleEntityOptions))
        ret = self.__Stereonet3DServicesStubLocal.SetPoleEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetPoleEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetPoleEntityVisibility(functionParam)
        

    def SetPoleVectorContourOptions(self,  ContourOptions: ContourOptionsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ContourOptions(This=self.__modelRef,  Input1=(ContourOptions.to_proto() if hasattr(ContourOptions, 'to_proto') else ContourOptions))
        ret = self.__Stereonet3DServicesStubLocal.SetPoleVectorContourOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetPoleVectorDensityContourSettings(self,  VectorDensityContourSettings: VectorDensityContourSettingsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_VectorDensityContourSettings(This=self.__modelRef,  Input1=(VectorDensityContourSettings.to_proto() if hasattr(VectorDensityContourSettings, 'to_proto') else VectorDensityContourSettings))
        ret = self.__Stereonet3DServicesStubLocal.SetPoleVectorDensityContourSettings(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetQuantitativeContourOptions(self,  ContourOptions: ContourOptionsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_ContourOptions(This=self.__modelRef,  Input1=(ContourOptions.to_proto() if hasattr(ContourOptions, 'to_proto') else ContourOptions))
        ret = self.__Stereonet3DServicesStubLocal.SetQuantitativeContourOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetQuantitativeContourSettings(self,  QuantitativeContourSettings: QuantitativeContourSettingsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_QuantitativeContourSettings(This=self.__modelRef,  Input1=(QuantitativeContourSettings.to_proto() if hasattr(QuantitativeContourSettings, 'to_proto') else QuantitativeContourSettings))
        ret = self.__Stereonet3DServicesStubLocal.SetQuantitativeContourSettings(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetSetVersusSet(self,  SetVersusSet: SetVersusSetVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_SetVersusSet(This=self.__modelRef,  Input1=(SetVersusSet.to_proto() if hasattr(SetVersusSet, 'to_proto') else SetVersusSet))
        ret = self.__Stereonet3DServicesStubLocal.SetSetVersusSet(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetSetWindowEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetSetWindowEntityGroupVisibility(functionParam)
        

    def SetStereonetOverlayEntityOptions(self,  StereonetOverlayEntityVisibility: StereonetOverlayEntityVisibilityVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_StereonetOverlayEntityVisibility(This=self.__modelRef,  Input1=(StereonetOverlayEntityVisibility.to_proto() if hasattr(StereonetOverlayEntityVisibility, 'to_proto') else StereonetOverlayEntityVisibility))
        ret = self.__Stereonet3DServicesStubLocal.SetStereonetOverlayEntityOptions(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetStereonetOverlayEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetStereonetOverlayEntityVisibility(functionParam)
        

    def SetSymbolicSettings(self,  SymbolicSettings: SymbolicSettingsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_SymbolicSettings(This=self.__modelRef,  Input1=(SymbolicSettings.to_proto() if hasattr(SymbolicSettings, 'to_proto') else SymbolicSettings))
        ret = self.__Stereonet3DServicesStubLocal.SetSymbolicSettings(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetTraverseEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetTraverseEntityGroupVisibility(functionParam)
        

    def SetUserPlaneEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet3DServicesStubLocal.SetUserPlaneEntityGroupVisibility(functionParam)
        

    def SetVectorMode(self,  eVectorMode: DipsAPI_pb2.eVectorMode):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet3DView_eVectorMode(This=self.__modelRef,  Input1=eVectorMode)
        ret = self.__Stereonet3DServicesStubLocal.SetVectorMode(functionParam)
        

 