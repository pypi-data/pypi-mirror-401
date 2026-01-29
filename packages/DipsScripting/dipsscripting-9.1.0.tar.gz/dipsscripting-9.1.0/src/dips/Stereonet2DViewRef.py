from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .Stereonet2DViewVal import Stereonet2DViewVal
from .ArrowToolEntityInfoRef import ArrowToolEntityInfoRef
from .ArrowToolEntityInfoRef import ArrowToolEntityInfoRef as ArrowToolEntityInfo_RefType
from .ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from .ConeToolEntityInfoRef import ConeToolEntityInfoRef
from .ConeToolEntityInfoRef import ConeToolEntityInfoRef as ConeToolEntityInfo_RefType
from .ConeToolEntityInfoVal import ConeToolEntityInfoVal
from .ContourEntityVisibilityVal import ContourEntityVisibilityVal
from .ContourOptionsVal import ContourOptionsVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType
from .EllipseToolEntityInfoRef import EllipseToolEntityInfoRef
from .EllipseToolEntityInfoRef import EllipseToolEntityInfoRef as EllipseToolEntityInfo_RefType
from .EllipseToolEntityInfoVal import EllipseToolEntityInfoVal
from .FoldEntityVisibilityRef import FoldEntityVisibilityRef
from .FoldWindowEntityVisibilityRef import FoldWindowEntityVisibilityRef
from .GlobalPlaneEntityVisibilityVal import GlobalPlaneEntityVisibilityVal
from .IntersectionOptionsVal import IntersectionOptionsVal
from .LineIntersectionCalculatorToolEntityInfoRef import LineIntersectionCalculatorToolEntityInfoRef
from .LineIntersectionCalculatorToolEntityInfoRef import LineIntersectionCalculatorToolEntityInfoRef as LineIntersectionCalculatorToolEntityInfo_RefType
from .LineIntersectionCalculatorToolEntityInfoVal import LineIntersectionCalculatorToolEntityInfoVal
from .LineToolEntityInfoRef import LineToolEntityInfoRef
from .LineToolEntityInfoRef import LineToolEntityInfoRef as LineToolEntityInfo_RefType
from .LineToolEntityInfoVal import LineToolEntityInfoVal
from .MeasureAngleToolEntityInfoRef import MeasureAngleToolEntityInfoRef
from .MeasureAngleToolEntityInfoRef import MeasureAngleToolEntityInfoRef as MeasureAngleToolEntityInfo_RefType
from .MeasureAngleToolEntityInfoVal import MeasureAngleToolEntityInfoVal
from .PitchGridToolEntityInfoRef import PitchGridToolEntityInfoRef
from .PitchGridToolEntityInfoRef import PitchGridToolEntityInfoRef as PitchGridToolEntityInfo_RefType
from .PitchGridToolEntityInfoVal import PitchGridToolEntityInfoVal
from .PlaneEntityVisibilityRef import PlaneEntityVisibilityRef
from .PlaneIntersectionCalculatorToolEntityInfoRef import PlaneIntersectionCalculatorToolEntityInfoRef
from .PlaneIntersectionCalculatorToolEntityInfoRef import PlaneIntersectionCalculatorToolEntityInfoRef as PlaneIntersectionCalculatorToolEntityInfo_RefType
from .PlaneIntersectionCalculatorToolEntityInfoVal import PlaneIntersectionCalculatorToolEntityInfoVal
from .PoleEntityOptionsVal import PoleEntityOptionsVal
from .PolygonToolEntityInfoRef import PolygonToolEntityInfoRef
from .PolygonToolEntityInfoRef import PolygonToolEntityInfoRef as PolygonToolEntityInfo_RefType
from .PolygonToolEntityInfoVal import PolygonToolEntityInfoVal
from .PolylineToolEntityInfoRef import PolylineToolEntityInfoRef
from .PolylineToolEntityInfoRef import PolylineToolEntityInfoRef as PolylineToolEntityInfo_RefType
from .PolylineToolEntityInfoVal import PolylineToolEntityInfoVal
from .QuantitativeContourSettingsVal import QuantitativeContourSettingsVal
from .RectangleToolEntityInfoRef import RectangleToolEntityInfoRef
from .RectangleToolEntityInfoRef import RectangleToolEntityInfoRef as RectangleToolEntityInfo_RefType
from .RectangleToolEntityInfoVal import RectangleToolEntityInfoVal
from .SetEntityVisibilityRef import SetEntityVisibilityRef
from .SetWindowEntityVisibilityRef import SetWindowEntityVisibilityRef
from .StereonetOverlayEntityVisibilityVal import StereonetOverlayEntityVisibilityVal
from .StereonetProjectionModeVal import StereonetProjectionModeVal
from .TextToolEntityInfoRef import TextToolEntityInfoRef
from .TextToolEntityInfoRef import TextToolEntityInfoRef as TextToolEntityInfo_RefType
from .TextToolEntityInfoVal import TextToolEntityInfoVal
from .TraverseEntityVisibilityRef import TraverseEntityVisibilityRef
from .TrendLineToolEntityInfoRef import TrendLineToolEntityInfoRef
from .TrendLineToolEntityInfoRef import TrendLineToolEntityInfoRef as TrendLineToolEntityInfo_RefType
from .TrendLineToolEntityInfoVal import TrendLineToolEntityInfoVal

class Stereonet2DViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_Stereonet2DView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__Stereonet2DServicesStubLocal = DipsAPI_pb2_grpc.Stereonet2DServicesStub(channelToConnectOn)

    
    def GetValue(self) -> Stereonet2DViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.Stereonet2DView()
        ret.MergeFromString(bytes.data)
        return Stereonet2DViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def AddStereonet2DArrowTool(self,  ArrowToolEntityInfo: ArrowToolEntityInfoVal) -> ArrowToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ArrowToolEntityInfo(This=self.__modelRef,  Input1=(ArrowToolEntityInfo.to_proto() if hasattr(ArrowToolEntityInfo, 'to_proto') else ArrowToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DArrowTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return ArrowToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DConeTool(self,  ConeToolEntityInfo: ConeToolEntityInfoVal) -> ConeToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ConeToolEntityInfo(This=self.__modelRef,  Input1=(ConeToolEntityInfo.to_proto() if hasattr(ConeToolEntityInfo, 'to_proto') else ConeToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DConeTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return ConeToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DEllipseTool(self,  EllipseToolEntityInfo: EllipseToolEntityInfoVal) -> EllipseToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_EllipseToolEntityInfo(This=self.__modelRef,  Input1=(EllipseToolEntityInfo.to_proto() if hasattr(EllipseToolEntityInfo, 'to_proto') else EllipseToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DEllipseTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return EllipseToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DLineIntersectionCalculatorTool(self,  LineIntersectionCalculatorToolEntityInfo: LineIntersectionCalculatorToolEntityInfoVal) -> LineIntersectionCalculatorToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_LineIntersectionCalculatorToolEntityInfo(This=self.__modelRef,  Input1=(LineIntersectionCalculatorToolEntityInfo.to_proto() if hasattr(LineIntersectionCalculatorToolEntityInfo, 'to_proto') else LineIntersectionCalculatorToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DLineIntersectionCalculatorTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return LineIntersectionCalculatorToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DLineTool(self,  LineToolEntityInfo: LineToolEntityInfoVal) -> LineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_LineToolEntityInfo(This=self.__modelRef,  Input1=(LineToolEntityInfo.to_proto() if hasattr(LineToolEntityInfo, 'to_proto') else LineToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DLineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return LineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DMeasureAngleTool(self,  MeasureAngleToolEntityInfo: MeasureAngleToolEntityInfoVal) -> MeasureAngleToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_MeasureAngleToolEntityInfo(This=self.__modelRef,  Input1=(MeasureAngleToolEntityInfo.to_proto() if hasattr(MeasureAngleToolEntityInfo, 'to_proto') else MeasureAngleToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DMeasureAngleTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return MeasureAngleToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DPitchGridTool(self,  PitchGridToolEntityInfo: PitchGridToolEntityInfoVal) -> PitchGridToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_PitchGridToolEntityInfo(This=self.__modelRef,  Input1=(PitchGridToolEntityInfo.to_proto() if hasattr(PitchGridToolEntityInfo, 'to_proto') else PitchGridToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DPitchGridTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PitchGridToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DPlaneIntersectionCalculatorTool(self,  PlaneIntersectionCalculatorToolEntityInfo: PlaneIntersectionCalculatorToolEntityInfoVal) -> PlaneIntersectionCalculatorToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_PlaneIntersectionCalculatorToolEntityInfo(This=self.__modelRef,  Input1=(PlaneIntersectionCalculatorToolEntityInfo.to_proto() if hasattr(PlaneIntersectionCalculatorToolEntityInfo, 'to_proto') else PlaneIntersectionCalculatorToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DPlaneIntersectionCalculatorTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PlaneIntersectionCalculatorToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DPolygonTool(self,  PolygonToolEntityInfo: PolygonToolEntityInfoVal) -> PolygonToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_PolygonToolEntityInfo(This=self.__modelRef,  Input1=(PolygonToolEntityInfo.to_proto() if hasattr(PolygonToolEntityInfo, 'to_proto') else PolygonToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DPolygonTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PolygonToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DPolylineTool(self,  PolylineToolEntityInfo: PolylineToolEntityInfoVal) -> PolylineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_PolylineToolEntityInfo(This=self.__modelRef,  Input1=(PolylineToolEntityInfo.to_proto() if hasattr(PolylineToolEntityInfo, 'to_proto') else PolylineToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DPolylineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PolylineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DRectangleTool(self,  RectangleToolEntityInfo: RectangleToolEntityInfoVal) -> RectangleToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_RectangleToolEntityInfo(This=self.__modelRef,  Input1=(RectangleToolEntityInfo.to_proto() if hasattr(RectangleToolEntityInfo, 'to_proto') else RectangleToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DRectangleTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return RectangleToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DTextTool(self,  TextToolEntityInfo: TextToolEntityInfoVal) -> TextToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_TextToolEntityInfo(This=self.__modelRef,  Input1=(TextToolEntityInfo.to_proto() if hasattr(TextToolEntityInfo, 'to_proto') else TextToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DTextTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return TextToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddStereonet2DTrendLineTool(self,  TrendLineToolEntityInfo: TrendLineToolEntityInfoVal) -> TrendLineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_TrendLineToolEntityInfo(This=self.__modelRef,  Input1=(TrendLineToolEntityInfo.to_proto() if hasattr(TrendLineToolEntityInfo, 'to_proto') else TrendLineToolEntityInfo))
        ret = self.__Stereonet2DServicesStubLocal.AddStereonet2DTrendLineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return TrendLineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def CloseStereonet2DView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.CloseStereonet2DView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def GetFoldEntityVisibilities(self) -> List[FoldEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetFoldEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( FoldEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetFoldWindowEntityVisibilities(self) -> List[FoldWindowEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetFoldWindowEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( FoldWindowEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetMeanSetPlaneEntityVisibilities(self) -> List[SetEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetMeanSetPlaneEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( SetEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetSetWindowEntityVisibilities(self) -> List[SetWindowEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetSetWindowEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( SetWindowEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DArrowTools(self) -> List[ArrowToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DArrowTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( ArrowToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DConeTools(self) -> List[ConeToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DConeTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( ConeToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DEllipseTools(self) -> List[EllipseToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DEllipseTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( EllipseToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DLineIntersectionCalculatorTools(self) -> List[LineIntersectionCalculatorToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DLineIntersectionCalculatorTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( LineIntersectionCalculatorToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DLineTools(self) -> List[LineToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DLineTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( LineToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DMeasureAngleTools(self) -> List[MeasureAngleToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DMeasureAngleTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( MeasureAngleToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DPitchGridTools(self) -> List[PitchGridToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DPitchGridTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PitchGridToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DPlaneIntersectionCalculatorTools(self) -> List[PlaneIntersectionCalculatorToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DPlaneIntersectionCalculatorTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PlaneIntersectionCalculatorToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DPolygonTools(self) -> List[PolygonToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DPolygonTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PolygonToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DPolylineTools(self) -> List[PolylineToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DPolylineTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PolylineToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DRectangleTools(self) -> List[RectangleToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DRectangleTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( RectangleToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DTextTools(self) -> List[TextToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DTextTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( TextToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetStereonet2DTrendLineTools(self) -> List[TrendLineToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetStereonet2DTrendLineTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( TrendLineToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetTraverseEntityVisibilities(self) -> List[TraverseEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetTraverseEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( TraverseEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetUserPlaneEntityVisibilities(self) -> List[PlaneEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView(This=self.__modelRef)
        ret = self.__Stereonet2DServicesStubLocal.GetUserPlaneEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PlaneEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__Stereonet2DServicesStubLocal.SetActiveDataFilter(functionParam)
        

    def SetArrowToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetArrowToolEntityGroupVisibility(functionParam)
        

    def SetConeToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetConeToolEntityGroupVisibility(functionParam)
        

    def SetContourEntityOptions(self,  ContourEntityVisibility: ContourEntityVisibilityVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ContourEntityVisibility(This=self.__modelRef,  Input1=(ContourEntityVisibility.to_proto() if hasattr(ContourEntityVisibility, 'to_proto') else ContourEntityVisibility))
        ret = self.__Stereonet2DServicesStubLocal.SetContourEntityOptions(functionParam)
        

    def SetContourEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetContourEntityVisibility(functionParam)
        

    def SetContourType(self,  eContourType: DipsAPI_pb2.eContourType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_eContourType(This=self.__modelRef,  Input1=eContourType)
        ret = self.__Stereonet2DServicesStubLocal.SetContourType(functionParam)
        

    def SetContourVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetContourVisibility(functionParam)
        

    def SetEllipseToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetEllipseToolEntityGroupVisibility(functionParam)
        

    def SetFoldEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetFoldEntityGroupVisibility(functionParam)
        

    def SetFoldWindowEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetFoldWindowEntityGroupVisibility(functionParam)
        

    def SetGlobalBestFitPlaneEntityOptions(self,  GlobalPlaneEntityVisibility: GlobalPlaneEntityVisibilityVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_GlobalPlaneEntityVisibility(This=self.__modelRef,  Input1=(GlobalPlaneEntityVisibility.to_proto() if hasattr(GlobalPlaneEntityVisibility, 'to_proto') else GlobalPlaneEntityVisibility))
        ret = self.__Stereonet2DServicesStubLocal.SetGlobalBestFitPlaneEntityOptions(functionParam)
        

    def SetGlobalBestFitPlaneEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetGlobalBestFitPlaneEntityVisibility(functionParam)
        

    def SetGlobalMeanPlaneEntityOptions(self,  GlobalPlaneEntityVisibility: GlobalPlaneEntityVisibilityVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_GlobalPlaneEntityVisibility(This=self.__modelRef,  Input1=(GlobalPlaneEntityVisibility.to_proto() if hasattr(GlobalPlaneEntityVisibility, 'to_proto') else GlobalPlaneEntityVisibility))
        ret = self.__Stereonet2DServicesStubLocal.SetGlobalMeanPlaneEntityOptions(functionParam)
        

    def SetGlobalMeanPlaneEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetGlobalMeanPlaneEntityVisibility(functionParam)
        

    def SetIntersectionEntityOptions(self,  IntersectionOptions: IntersectionOptionsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_IntersectionOptions(This=self.__modelRef,  Input1=(IntersectionOptions.to_proto() if hasattr(IntersectionOptions, 'to_proto') else IntersectionOptions))
        ret = self.__Stereonet2DServicesStubLocal.SetIntersectionEntityOptions(functionParam)
        

    def SetIntersectionEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetIntersectionEntityVisibility(functionParam)
        

    def SetIntersectionVectorContourOptions(self,  ContourOptions: ContourOptionsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ContourOptions(This=self.__modelRef,  Input1=(ContourOptions.to_proto() if hasattr(ContourOptions, 'to_proto') else ContourOptions))
        ret = self.__Stereonet2DServicesStubLocal.SetIntersectionVectorContourOptions(functionParam)
        

    def SetIsWeighted(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetIsWeighted(functionParam)
        

    def SetLegendVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetLegendVisibility(functionParam)
        

    def SetLineIntersectionCalculatorToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetLineIntersectionCalculatorToolEntityGroupVisibility(functionParam)
        

    def SetLineToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetLineToolEntityGroupVisibility(functionParam)
        

    def SetMeanSetPlaneEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetMeanSetPlaneEntityGroupVisibility(functionParam)
        

    def SetMeasureAngleToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetMeasureAngleToolEntityGroupVisibility(functionParam)
        

    def SetPitchGridToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetPitchGridToolEntityGroupVisibility(functionParam)
        

    def SetPlaneIntersectionCalculatorToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetPlaneIntersectionCalculatorToolEntityGroupVisibility(functionParam)
        

    def SetPoleEntityOptions(self,  PoleEntityOptions: PoleEntityOptionsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_PoleEntityOptions(This=self.__modelRef,  Input1=(PoleEntityOptions.to_proto() if hasattr(PoleEntityOptions, 'to_proto') else PoleEntityOptions))
        ret = self.__Stereonet2DServicesStubLocal.SetPoleEntityOptions(functionParam)
        

    def SetPoleEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetPoleEntityVisibility(functionParam)
        

    def SetPoleEntVisiblity(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetPoleEntVisiblity(functionParam)
        

    def SetPoleVectorContourOptions(self,  ContourOptions: ContourOptionsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ContourOptions(This=self.__modelRef,  Input1=(ContourOptions.to_proto() if hasattr(ContourOptions, 'to_proto') else ContourOptions))
        ret = self.__Stereonet2DServicesStubLocal.SetPoleVectorContourOptions(functionParam)
        

    def SetPolygonToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetPolygonToolEntityGroupVisibility(functionParam)
        

    def SetPolylineToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetPolylineToolEntityGroupVisibility(functionParam)
        

    def SetProjectionMode(self,  StereonetProjectionMode: StereonetProjectionModeVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_StereonetProjectionMode(This=self.__modelRef,  Input1=(StereonetProjectionMode.to_proto() if hasattr(StereonetProjectionMode, 'to_proto') else StereonetProjectionMode))
        ret = self.__Stereonet2DServicesStubLocal.SetProjectionMode(functionParam)
        

    def SetQuantitativeContourOptions(self,  ContourOptions: ContourOptionsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_ContourOptions(This=self.__modelRef,  Input1=(ContourOptions.to_proto() if hasattr(ContourOptions, 'to_proto') else ContourOptions))
        ret = self.__Stereonet2DServicesStubLocal.SetQuantitativeContourOptions(functionParam)
        

    def SetQuantitativeContourSettings(self,  QuantitativeContourSettings: QuantitativeContourSettingsVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_QuantitativeContourSettings(This=self.__modelRef,  Input1=(QuantitativeContourSettings.to_proto() if hasattr(QuantitativeContourSettings, 'to_proto') else QuantitativeContourSettings))
        ret = self.__Stereonet2DServicesStubLocal.SetQuantitativeContourSettings(functionParam)
        

    def SetRectangleToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetRectangleToolEntityGroupVisibility(functionParam)
        

    def SetSetWindowEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetSetWindowEntityGroupVisibility(functionParam)
        

    def SetStereonetOverlayEntityOptions(self,  StereonetOverlayEntityVisibility: StereonetOverlayEntityVisibilityVal):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_StereonetOverlayEntityVisibility(This=self.__modelRef,  Input1=(StereonetOverlayEntityVisibility.to_proto() if hasattr(StereonetOverlayEntityVisibility, 'to_proto') else StereonetOverlayEntityVisibility))
        ret = self.__Stereonet2DServicesStubLocal.SetStereonetOverlayEntityOptions(functionParam)
        

    def SetStereonetOverlayEntityVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetStereonetOverlayEntityVisibility(functionParam)
        

    def SetTextToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetTextToolEntityGroupVisibility(functionParam)
        

    def SetTraverseEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetTraverseEntityGroupVisibility(functionParam)
        

    def SetTrendLineToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetTrendLineToolEntityGroupVisibility(functionParam)
        

    def SetUserPlaneEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__Stereonet2DServicesStubLocal.SetUserPlaneEntityGroupVisibility(functionParam)
        

    def SetVectorMode(self,  eVectorMode: DipsAPI_pb2.eVectorMode):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_Stereonet2DView_eVectorMode(This=self.__modelRef,  Input1=eVectorMode)
        ret = self.__Stereonet2DServicesStubLocal.SetVectorMode(functionParam)
        

 