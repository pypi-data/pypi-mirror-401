from typing import List
from . import DipsAPI_pb2_grpc
from . import DipsAPI_pb2
from .RosetteViewVal import RosetteViewVal
from .ArrowToolEntityInfoRef import ArrowToolEntityInfoRef
from .ArrowToolEntityInfoRef import ArrowToolEntityInfoRef as ArrowToolEntityInfo_RefType
from .ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from .DataFilterRef import DataFilterRef as DataFilter_RefType
from .EllipseToolEntityInfoRef import EllipseToolEntityInfoRef
from .EllipseToolEntityInfoRef import EllipseToolEntityInfoRef as EllipseToolEntityInfo_RefType
from .EllipseToolEntityInfoVal import EllipseToolEntityInfoVal
from .LineToolEntityInfoRef import LineToolEntityInfoRef
from .LineToolEntityInfoRef import LineToolEntityInfoRef as LineToolEntityInfo_RefType
from .LineToolEntityInfoVal import LineToolEntityInfoVal
from .PlaneEntityVisibilityRef import PlaneEntityVisibilityRef
from .PolygonToolEntityInfoRef import PolygonToolEntityInfoRef
from .PolygonToolEntityInfoRef import PolygonToolEntityInfoRef as PolygonToolEntityInfo_RefType
from .PolygonToolEntityInfoVal import PolygonToolEntityInfoVal
from .PolylineToolEntityInfoRef import PolylineToolEntityInfoRef
from .PolylineToolEntityInfoRef import PolylineToolEntityInfoRef as PolylineToolEntityInfo_RefType
from .PolylineToolEntityInfoVal import PolylineToolEntityInfoVal
from .RectangleToolEntityInfoRef import RectangleToolEntityInfoRef
from .RectangleToolEntityInfoRef import RectangleToolEntityInfoRef as RectangleToolEntityInfo_RefType
from .RectangleToolEntityInfoVal import RectangleToolEntityInfoVal
from .RosetteSettingsVal import RosetteSettingsVal
from .StereonetProjectionModeVal import StereonetProjectionModeVal
from .TextToolEntityInfoRef import TextToolEntityInfoRef
from .TextToolEntityInfoRef import TextToolEntityInfoRef as TextToolEntityInfo_RefType
from .TextToolEntityInfoVal import TextToolEntityInfoVal
from .TrendLineToolEntityInfoRef import TrendLineToolEntityInfoRef
from .TrendLineToolEntityInfoRef import TrendLineToolEntityInfoRef as TrendLineToolEntityInfo_RefType
from .TrendLineToolEntityInfoVal import TrendLineToolEntityInfoVal
from .ValidatableResultVal import ValidatableResultVal

class RosetteViewRef:
    def __init__(self, channelToConnectOn, ref: DipsAPI_pb2.ProtoReference_RosetteView):
        self.__modelRef = ref
        self.__refManagerStub = DipsAPI_pb2_grpc.nSameModuleReferenceAccessorStub(channelToConnectOn)
        self.__channelToConnectOn = channelToConnectOn
        self.__RosetteServicesStubLocal = DipsAPI_pb2_grpc.RosetteServicesStub(channelToConnectOn)

    
    def GetValue(self) -> RosetteViewVal:
        bytes = self.__refManagerStub.GetValue(self.__modelRef.ID)
        ret = DipsAPI_pb2.RosetteView()
        ret.MergeFromString(bytes.data)
        return RosetteViewVal.from_proto(ret)
    
    def get_model_ref(self):
        """Get the underlying model reference for direct protobuf operations."""
        return self.__modelRef
    
    def AddRosetteArrowTool(self,  ArrowToolEntityInfo: ArrowToolEntityInfoVal) -> ArrowToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_ArrowToolEntityInfo(This=self.__modelRef,  Input1=(ArrowToolEntityInfo.to_proto() if hasattr(ArrowToolEntityInfo, 'to_proto') else ArrowToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosetteArrowTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return ArrowToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosetteEllipseTool(self,  EllipseToolEntityInfo: EllipseToolEntityInfoVal) -> EllipseToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_EllipseToolEntityInfo(This=self.__modelRef,  Input1=(EllipseToolEntityInfo.to_proto() if hasattr(EllipseToolEntityInfo, 'to_proto') else EllipseToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosetteEllipseTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return EllipseToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosetteLineTool(self,  LineToolEntityInfo: LineToolEntityInfoVal) -> LineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_LineToolEntityInfo(This=self.__modelRef,  Input1=(LineToolEntityInfo.to_proto() if hasattr(LineToolEntityInfo, 'to_proto') else LineToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosetteLineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return LineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosettePolygonTool(self,  PolygonToolEntityInfo: PolygonToolEntityInfoVal) -> PolygonToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_PolygonToolEntityInfo(This=self.__modelRef,  Input1=(PolygonToolEntityInfo.to_proto() if hasattr(PolygonToolEntityInfo, 'to_proto') else PolygonToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosettePolygonTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PolygonToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosettePolylineTool(self,  PolylineToolEntityInfo: PolylineToolEntityInfoVal) -> PolylineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_PolylineToolEntityInfo(This=self.__modelRef,  Input1=(PolylineToolEntityInfo.to_proto() if hasattr(PolylineToolEntityInfo, 'to_proto') else PolylineToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosettePolylineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return PolylineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosetteRectangleTool(self,  RectangleToolEntityInfo: RectangleToolEntityInfoVal) -> RectangleToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_RectangleToolEntityInfo(This=self.__modelRef,  Input1=(RectangleToolEntityInfo.to_proto() if hasattr(RectangleToolEntityInfo, 'to_proto') else RectangleToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosetteRectangleTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return RectangleToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosetteTextTool(self,  TextToolEntityInfo: TextToolEntityInfoVal) -> TextToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_TextToolEntityInfo(This=self.__modelRef,  Input1=(TextToolEntityInfo.to_proto() if hasattr(TextToolEntityInfo, 'to_proto') else TextToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosetteTextTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return TextToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def AddRosetteTrendLineTool(self,  TrendLineToolEntityInfo: TrendLineToolEntityInfoVal) -> TrendLineToolEntityInfo_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_TrendLineToolEntityInfo(This=self.__modelRef,  Input1=(TrendLineToolEntityInfo.to_proto() if hasattr(TrendLineToolEntityInfo, 'to_proto') else TrendLineToolEntityInfo))
        ret = self.__RosetteServicesStubLocal.AddRosetteTrendLineTool(functionParam)
        
        if len(ret.Errors) > 0:
            raise ValueError(ret.Errors[0].ErrorMessage)
        return TrendLineToolEntityInfo_RefType(self.__channelToConnectOn, ret.Result)
        

    def CloseRosetteView(self):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.CloseRosetteView(functionParam)
        

    def GetActiveDataFilter(self) -> DataFilter_RefType:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetActiveDataFilter(functionParam)
        
        return DataFilter_RefType(self.__channelToConnectOn, ret)
        

    def GetRosetteArrowTools(self) -> List[ArrowToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosetteArrowTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( ArrowToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosetteEllipseTools(self) -> List[EllipseToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosetteEllipseTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( EllipseToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosetteLineTools(self) -> List[LineToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosetteLineTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( LineToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosettePolygonTools(self) -> List[PolygonToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosettePolygonTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PolygonToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosettePolylineTools(self) -> List[PolylineToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosettePolylineTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PolylineToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosetteRectangleTools(self) -> List[RectangleToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosetteRectangleTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( RectangleToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosetteTextTools(self) -> List[TextToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosetteTextTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( TextToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetRosetteTrendLineTools(self) -> List[TrendLineToolEntityInfoRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetRosetteTrendLineTools(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( TrendLineToolEntityInfoRef(self.__channelToConnectOn, item) )
        return retList
        

    def GetUserPlaneEntityVisibilities(self) -> List[PlaneEntityVisibilityRef]:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView(This=self.__modelRef)
        ret = self.__RosetteServicesStubLocal.GetUserPlaneEntityVisibilities(functionParam)
        
        retList=[]
        for item in ret.items:
            retList.append( PlaneEntityVisibilityRef(self.__channelToConnectOn, item) )
        return retList
        

    def SetActiveDataFilter(self,  DataFilter: DataFilter_RefType):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_ProtoReference_DataFilter(This=self.__modelRef,  Input1=DataFilter.get_model_ref())
        ret = self.__RosetteServicesStubLocal.SetActiveDataFilter(functionParam)
        

    def SetArrowToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetArrowToolEntityGroupVisibility(functionParam)
        

    def SetEllipseToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetEllipseToolEntityGroupVisibility(functionParam)
        

    def SetLineToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetLineToolEntityGroupVisibility(functionParam)
        

    def SetPolygonToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetPolygonToolEntityGroupVisibility(functionParam)
        

    def SetPolylineToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetPolylineToolEntityGroupVisibility(functionParam)
        

    def SetProjectionMode(self,  StereonetProjectionMode: StereonetProjectionModeVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_StereonetProjectionMode(This=self.__modelRef,  Input1=(StereonetProjectionMode.to_proto() if hasattr(StereonetProjectionMode, 'to_proto') else StereonetProjectionMode))
        ret = self.__RosetteServicesStubLocal.SetProjectionMode(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetRectangleToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetRectangleToolEntityGroupVisibility(functionParam)
        

    def SetRosetteSettings(self,  RosetteSettings: RosetteSettingsVal) -> ValidatableResultVal:
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_RosetteSettings(This=self.__modelRef,  Input1=(RosetteSettings.to_proto() if hasattr(RosetteSettings, 'to_proto') else RosetteSettings))
        ret = self.__RosetteServicesStubLocal.SetRosetteSettings(functionParam)
        
        return ValidatableResultVal.from_proto(ret)
        

    def SetTextToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetTextToolEntityGroupVisibility(functionParam)
        

    def SetToolsEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetToolsEntityGroupVisibility(functionParam)
        

    def SetTrendLineToolEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetTrendLineToolEntityGroupVisibility(functionParam)
        

    def SetUserPlaneEntityGroupVisibility(self,  Boolean: bool):
        functionParam = DipsAPI_pb2.ProtoMemberFunction_ProtoReference_RosetteView_Boolean(This=self.__modelRef,  Input1=Boolean)
        ret = self.__RosetteServicesStubLocal.SetUserPlaneEntityGroupVisibility(functionParam)
        

 