"""Generated wrapper for OrientationDataSet protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal
from .CustomColumnCollectionVal import CustomColumnCollectionVal
from .DataFormatterVal import DataFormatterVal
from .DiscontinuityDataVal import DiscontinuityDataVal
from .LatLongVal import LatLongVal
from .SurveyDataVal import SurveyDataVal
from .Vector3Val import Vector3Val

class OrientationDataSetVal:
    """Simple wrapper for OrientationDataSet with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.OrientationDataSet


    def __init__(self, global_position: Optional[LatLongVal] = None, local_position: Optional[Vector3Val] = None, orient1: Optional[AngleDataVal] = None, orient2: Optional[AngleDataVal] = None, orient3: Optional[AngleDataVal] = None, declination: Optional[AngleDataVal] = None, traverse_elevation_unit: Optional[DataFormatterVal] = None, traverse_xyz_unit: Optional[DataFormatterVal] = None, traverse_depth_unit: Optional[DataFormatterVal] = None, survey_distance_unit: Optional[DataFormatterVal] = None, discontinuity_distance_unit: Optional[DataFormatterVal] = None, discontinuity_xyz_unit: Optional[DataFormatterVal] = None, discontinuity_persistence_unit: Optional[DataFormatterVal] = None, discontinuity_extra_columns: Optional[CustomColumnCollectionVal] = None, survey_extra_columns: Optional[CustomColumnCollectionVal] = None, proto_message: Optional[Any] = None):
        """Initialize the OrientationDataSet wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if global_position is not None:
            self._proto_message.GlobalPosition.CopyFrom(global_position.to_proto())
            self._global_position_wrapper = global_position
        if local_position is not None:
            self._proto_message.LocalPosition.CopyFrom(local_position.to_proto())
            self._local_position_wrapper = local_position
        if orient1 is not None:
            self._proto_message.Orient1.CopyFrom(orient1.to_proto())
            self._orient1_wrapper = orient1
        if orient2 is not None:
            self._proto_message.Orient2.CopyFrom(orient2.to_proto())
            self._orient2_wrapper = orient2
        if orient3 is not None:
            self._proto_message.Orient3.CopyFrom(orient3.to_proto())
            self._orient3_wrapper = orient3
        if declination is not None:
            self._proto_message.Declination.CopyFrom(declination.to_proto())
            self._declination_wrapper = declination
        if traverse_elevation_unit is not None:
            self._proto_message.TraverseElevationUnit.CopyFrom(traverse_elevation_unit.to_proto())
            self._traverse_elevation_unit_wrapper = traverse_elevation_unit
        if traverse_xyz_unit is not None:
            self._proto_message.TraverseXYZUnit.CopyFrom(traverse_xyz_unit.to_proto())
            self._traverse_xyz_unit_wrapper = traverse_xyz_unit
        if traverse_depth_unit is not None:
            self._proto_message.TraverseDepthUnit.CopyFrom(traverse_depth_unit.to_proto())
            self._traverse_depth_unit_wrapper = traverse_depth_unit
        if survey_distance_unit is not None:
            self._proto_message.SurveyDistanceUnit.CopyFrom(survey_distance_unit.to_proto())
            self._survey_distance_unit_wrapper = survey_distance_unit
        if discontinuity_distance_unit is not None:
            self._proto_message.DiscontinuityDistanceUnit.CopyFrom(discontinuity_distance_unit.to_proto())
            self._discontinuity_distance_unit_wrapper = discontinuity_distance_unit
        if discontinuity_xyz_unit is not None:
            self._proto_message.DiscontinuityXYZUnit.CopyFrom(discontinuity_xyz_unit.to_proto())
            self._discontinuity_xyz_unit_wrapper = discontinuity_xyz_unit
        if discontinuity_persistence_unit is not None:
            self._proto_message.DiscontinuityPersistenceUnit.CopyFrom(discontinuity_persistence_unit.to_proto())
            self._discontinuity_persistence_unit_wrapper = discontinuity_persistence_unit
        if discontinuity_extra_columns is not None:
            self._proto_message.DiscontinuityExtraColumns.CopyFrom(discontinuity_extra_columns.to_proto())
            self._discontinuity_extra_columns_wrapper = discontinuity_extra_columns
        if survey_extra_columns is not None:
            self._proto_message.SurveyExtraColumns.CopyFrom(survey_extra_columns.to_proto())
            self._survey_extra_columns_wrapper = survey_extra_columns


    # Properties

    @property
    def name(self) -> str:
        """Get the Name field value."""
        return self._proto_message.Name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the Name field value."""
        self._proto_message.Name = value


    @property
    def orientation_data_type(self) -> Any:
        """Get the OrientationDataType field value."""
        return self._proto_message.OrientationDataType
    
    @orientation_data_type.setter
    def orientation_data_type(self, value: Any) -> None:
        """Set the OrientationDataType field value."""
        self._proto_message.OrientationDataType = value


    @property
    def orientation_convention(self) -> Any:
        """Get the OrientationConvention field value."""
        return self._proto_message.OrientationConvention
    
    @orientation_convention.setter
    def orientation_convention(self, value: Any) -> None:
        """Set the OrientationConvention field value."""
        self._proto_message.OrientationConvention = value


    @property
    def discontinuity_orientation_convention(self) -> Any:
        """Get the DiscontinuityOrientationConvention field value."""
        return self._proto_message.DiscontinuityOrientationConvention
    
    @discontinuity_orientation_convention.setter
    def discontinuity_orientation_convention(self, value: Any) -> None:
        """Set the DiscontinuityOrientationConvention field value."""
        self._proto_message.DiscontinuityOrientationConvention = value


    @property
    def global_position(self) -> LatLongVal:
        """Get the GlobalPosition field as a wrapper."""
        if not hasattr(self, '_global_position_wrapper'):
            self._global_position_wrapper = LatLongVal(proto_message=self._proto_message.GlobalPosition)
        return self._global_position_wrapper
    
    @global_position.setter
    def global_position(self, value: LatLongVal) -> None:
        """Set the GlobalPosition field to a wrapper."""
        self._proto_message.GlobalPosition.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_global_position_wrapper'):
            self._global_position_wrapper._proto_message.CopyFrom(self._proto_message.GlobalPosition)


    @property
    def local_position(self) -> Vector3Val:
        """Get the LocalPosition field as a wrapper."""
        if not hasattr(self, '_local_position_wrapper'):
            self._local_position_wrapper = Vector3Val(proto_message=self._proto_message.LocalPosition)
        return self._local_position_wrapper
    
    @local_position.setter
    def local_position(self, value: Vector3Val) -> None:
        """Set the LocalPosition field to a wrapper."""
        self._proto_message.LocalPosition.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_local_position_wrapper'):
            self._local_position_wrapper._proto_message.CopyFrom(self._proto_message.LocalPosition)


    @property
    def orient1(self) -> AngleDataVal:
        """Get the Orient1 field as a wrapper."""
        if not hasattr(self, '_orient1_wrapper'):
            self._orient1_wrapper = AngleDataVal(proto_message=self._proto_message.Orient1)
        return self._orient1_wrapper
    
    @orient1.setter
    def orient1(self, value: AngleDataVal) -> None:
        """Set the Orient1 field to a wrapper."""
        self._proto_message.Orient1.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_orient1_wrapper'):
            self._orient1_wrapper._proto_message.CopyFrom(self._proto_message.Orient1)


    @property
    def orient2(self) -> AngleDataVal:
        """Get the Orient2 field as a wrapper."""
        if not hasattr(self, '_orient2_wrapper'):
            self._orient2_wrapper = AngleDataVal(proto_message=self._proto_message.Orient2)
        return self._orient2_wrapper
    
    @orient2.setter
    def orient2(self, value: AngleDataVal) -> None:
        """Set the Orient2 field to a wrapper."""
        self._proto_message.Orient2.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_orient2_wrapper'):
            self._orient2_wrapper._proto_message.CopyFrom(self._proto_message.Orient2)


    @property
    def orient3(self) -> AngleDataVal:
        """Get the Orient3 field as a wrapper."""
        if not hasattr(self, '_orient3_wrapper'):
            self._orient3_wrapper = AngleDataVal(proto_message=self._proto_message.Orient3)
        return self._orient3_wrapper
    
    @orient3.setter
    def orient3(self, value: AngleDataVal) -> None:
        """Set the Orient3 field to a wrapper."""
        self._proto_message.Orient3.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_orient3_wrapper'):
            self._orient3_wrapper._proto_message.CopyFrom(self._proto_message.Orient3)


    @property
    def declination(self) -> AngleDataVal:
        """Get the Declination field as a wrapper."""
        if not hasattr(self, '_declination_wrapper'):
            self._declination_wrapper = AngleDataVal(proto_message=self._proto_message.Declination)
        return self._declination_wrapper
    
    @declination.setter
    def declination(self, value: AngleDataVal) -> None:
        """Set the Declination field to a wrapper."""
        self._proto_message.Declination.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_declination_wrapper'):
            self._declination_wrapper._proto_message.CopyFrom(self._proto_message.Declination)


    @property
    def de_survey_option(self) -> Any:
        """Get the DeSurveyOption field value."""
        return self._proto_message.DeSurveyOption
    
    @de_survey_option.setter
    def de_survey_option(self, value: Any) -> None:
        """Set the DeSurveyOption field value."""
        self._proto_message.DeSurveyOption = value


    @property
    def traverse_elevation_unit(self) -> DataFormatterVal:
        """Get the TraverseElevationUnit field as a wrapper."""
        if not hasattr(self, '_traverse_elevation_unit_wrapper'):
            self._traverse_elevation_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.TraverseElevationUnit)
        return self._traverse_elevation_unit_wrapper
    
    @traverse_elevation_unit.setter
    def traverse_elevation_unit(self, value: DataFormatterVal) -> None:
        """Set the TraverseElevationUnit field to a wrapper."""
        self._proto_message.TraverseElevationUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_traverse_elevation_unit_wrapper'):
            self._traverse_elevation_unit_wrapper._proto_message.CopyFrom(self._proto_message.TraverseElevationUnit)


    @property
    def traverse_xyz_unit(self) -> DataFormatterVal:
        """Get the TraverseXYZUnit field as a wrapper."""
        if not hasattr(self, '_traverse_xyz_unit_wrapper'):
            self._traverse_xyz_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.TraverseXYZUnit)
        return self._traverse_xyz_unit_wrapper
    
    @traverse_xyz_unit.setter
    def traverse_xyz_unit(self, value: DataFormatterVal) -> None:
        """Set the TraverseXYZUnit field to a wrapper."""
        self._proto_message.TraverseXYZUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_traverse_xyz_unit_wrapper'):
            self._traverse_xyz_unit_wrapper._proto_message.CopyFrom(self._proto_message.TraverseXYZUnit)


    @property
    def traverse_depth_unit(self) -> DataFormatterVal:
        """Get the TraverseDepthUnit field as a wrapper."""
        if not hasattr(self, '_traverse_depth_unit_wrapper'):
            self._traverse_depth_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.TraverseDepthUnit)
        return self._traverse_depth_unit_wrapper
    
    @traverse_depth_unit.setter
    def traverse_depth_unit(self, value: DataFormatterVal) -> None:
        """Set the TraverseDepthUnit field to a wrapper."""
        self._proto_message.TraverseDepthUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_traverse_depth_unit_wrapper'):
            self._traverse_depth_unit_wrapper._proto_message.CopyFrom(self._proto_message.TraverseDepthUnit)


    @property
    def survey_distance_unit(self) -> DataFormatterVal:
        """Get the SurveyDistanceUnit field as a wrapper."""
        if not hasattr(self, '_survey_distance_unit_wrapper'):
            self._survey_distance_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.SurveyDistanceUnit)
        return self._survey_distance_unit_wrapper
    
    @survey_distance_unit.setter
    def survey_distance_unit(self, value: DataFormatterVal) -> None:
        """Set the SurveyDistanceUnit field to a wrapper."""
        self._proto_message.SurveyDistanceUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_survey_distance_unit_wrapper'):
            self._survey_distance_unit_wrapper._proto_message.CopyFrom(self._proto_message.SurveyDistanceUnit)


    @property
    def discontinuity_distance_unit(self) -> DataFormatterVal:
        """Get the DiscontinuityDistanceUnit field as a wrapper."""
        if not hasattr(self, '_discontinuity_distance_unit_wrapper'):
            self._discontinuity_distance_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.DiscontinuityDistanceUnit)
        return self._discontinuity_distance_unit_wrapper
    
    @discontinuity_distance_unit.setter
    def discontinuity_distance_unit(self, value: DataFormatterVal) -> None:
        """Set the DiscontinuityDistanceUnit field to a wrapper."""
        self._proto_message.DiscontinuityDistanceUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_discontinuity_distance_unit_wrapper'):
            self._discontinuity_distance_unit_wrapper._proto_message.CopyFrom(self._proto_message.DiscontinuityDistanceUnit)


    @property
    def discontinuity_xyz_unit(self) -> DataFormatterVal:
        """Get the DiscontinuityXYZUnit field as a wrapper."""
        if not hasattr(self, '_discontinuity_xyz_unit_wrapper'):
            self._discontinuity_xyz_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.DiscontinuityXYZUnit)
        return self._discontinuity_xyz_unit_wrapper
    
    @discontinuity_xyz_unit.setter
    def discontinuity_xyz_unit(self, value: DataFormatterVal) -> None:
        """Set the DiscontinuityXYZUnit field to a wrapper."""
        self._proto_message.DiscontinuityXYZUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_discontinuity_xyz_unit_wrapper'):
            self._discontinuity_xyz_unit_wrapper._proto_message.CopyFrom(self._proto_message.DiscontinuityXYZUnit)


    @property
    def discontinuity_persistence_unit(self) -> DataFormatterVal:
        """Get the DiscontinuityPersistenceUnit field as a wrapper."""
        if not hasattr(self, '_discontinuity_persistence_unit_wrapper'):
            self._discontinuity_persistence_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.DiscontinuityPersistenceUnit)
        return self._discontinuity_persistence_unit_wrapper
    
    @discontinuity_persistence_unit.setter
    def discontinuity_persistence_unit(self, value: DataFormatterVal) -> None:
        """Set the DiscontinuityPersistenceUnit field to a wrapper."""
        self._proto_message.DiscontinuityPersistenceUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_discontinuity_persistence_unit_wrapper'):
            self._discontinuity_persistence_unit_wrapper._proto_message.CopyFrom(self._proto_message.DiscontinuityPersistenceUnit)


    @property
    def discontinuity_extra_columns(self) -> CustomColumnCollectionVal:
        """Get the DiscontinuityExtraColumns field as a wrapper."""
        if not hasattr(self, '_discontinuity_extra_columns_wrapper'):
            self._discontinuity_extra_columns_wrapper = CustomColumnCollectionVal(proto_message=self._proto_message.DiscontinuityExtraColumns)
        return self._discontinuity_extra_columns_wrapper
    
    @discontinuity_extra_columns.setter
    def discontinuity_extra_columns(self, value: CustomColumnCollectionVal) -> None:
        """Set the DiscontinuityExtraColumns field to a wrapper."""
        self._proto_message.DiscontinuityExtraColumns.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_discontinuity_extra_columns_wrapper'):
            self._discontinuity_extra_columns_wrapper._proto_message.CopyFrom(self._proto_message.DiscontinuityExtraColumns)


    @property
    def discontinuity_list(self) -> List[DiscontinuityDataVal]:
        """Get the DiscontinuityList field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.DiscontinuityList, DiscontinuityDataVal)
    
    @discontinuity_list.setter
    def discontinuity_list(self, value: List[DiscontinuityDataVal]) -> None:
        """Set the DiscontinuityList field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.DiscontinuityList[:] = []
        for item in value:
            self._proto_message.DiscontinuityList.append(item.to_proto())


    @property
    def survey_extra_columns(self) -> CustomColumnCollectionVal:
        """Get the SurveyExtraColumns field as a wrapper."""
        if not hasattr(self, '_survey_extra_columns_wrapper'):
            self._survey_extra_columns_wrapper = CustomColumnCollectionVal(proto_message=self._proto_message.SurveyExtraColumns)
        return self._survey_extra_columns_wrapper
    
    @survey_extra_columns.setter
    def survey_extra_columns(self, value: CustomColumnCollectionVal) -> None:
        """Set the SurveyExtraColumns field to a wrapper."""
        self._proto_message.SurveyExtraColumns.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_survey_extra_columns_wrapper'):
            self._survey_extra_columns_wrapper._proto_message.CopyFrom(self._proto_message.SurveyExtraColumns)


    @property
    def survey_list(self) -> List[SurveyDataVal]:
        """Get the SurveyList field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.SurveyList, SurveyDataVal)
    
    @survey_list.setter
    def survey_list(self, value: List[SurveyDataVal]) -> None:
        """Set the SurveyList field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.SurveyList[:] = []
        for item in value:
            self._proto_message.SurveyList.append(item.to_proto())


    @property
    def depth(self) -> float:
        """Get the Depth field value."""
        return self._proto_message.Depth
    
    @depth.setter
    def depth(self, value: float) -> None:
        """Set the Depth field value."""
        self._proto_message.Depth = value


    @property
    def comments(self) -> str:
        """Get the Comments field value."""
        return self._proto_message.Comments
    
    @comments.setter
    def comments(self, value: str) -> None:
        """Set the Comments field value."""
        self._proto_message.Comments = value


    # Utility methods

    def to_proto(self):
        """Get the underlying protobuf message."""
        return self._proto_message
    
    @classmethod
    def from_proto(cls, proto_message):
        """Create wrapper from existing protobuf message."""
        wrapper = cls()
        wrapper._proto_message.CopyFrom(proto_message)
        return wrapper
    
    def copy(self):
        """Create a copy of this wrapper."""
        new_wrapper = self.__class__()
        new_wrapper._proto_message.CopyFrom(self._proto_message)
        return new_wrapper
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}({self._proto_message})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"{self.__class__.__name__}({self._proto_message})"
