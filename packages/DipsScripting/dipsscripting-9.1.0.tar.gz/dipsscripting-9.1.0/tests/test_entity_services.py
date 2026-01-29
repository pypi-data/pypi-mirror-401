"""
Integration tests for consolidated Entity Services functionality.
These tests require a running Dips application or will launch one.
Tests entity operations across different view types (2D Stereonet, 3D Stereonet, Rosette).
"""
import pytest
from dips import DipsApp
from dips import DipsAPI_pb2
from dips.PlaneEntityVisibilityVal import PlaneEntityVisibilityVal
from dips.SetEntityVisibilityVal import SetEntityVisibilityVal
from dips.SetWindowEntityVisibilityVal import SetWindowEntityVisibilityVal
from dips.TraverseEntityVisibilityVal import TraverseEntityVisibilityVal
from dips.FoldEntityVisibilityVal import FoldEntityVisibilityVal
from dips.FoldWindowEntityVisibilityVal import FoldWindowEntityVisibilityVal
from dips.TextToolEntityInfoVal import TextToolEntityInfoVal
from dips.ArrowToolEntityInfoVal import ArrowToolEntityInfoVal
from dips.LineToolEntityInfoVal import LineToolEntityInfoVal
import dips.AnchorPointVal
import dips.TrendPlungeVal
import dips.AngleDataVal
import dips.Vector2DVal
import dips.ColorSurrogateVal
import dips.LineFormatVal
import dips.FillFormatVal
import dips.TextFormatVal
import dips.OrientationDataSetVal
import dips.DiscontinuityDataVal
import dips.SetEntityInfoVal
import dips.SetWindowEntityInfoVal
import dips.CircularWindowVal
import dips.SetStatisticsSettingsVal
import dips.PlaneEntityInfoVal
import dips.PlaneVal
import dips.FoldEntityInfoVal
import dips.FoldWindowEntityInfoVal
import dips.WrappedFreehandWindowVal
import dips.FreehandWindowVal
from dips import BuiltInDataFormatters
import math


# Helper functions to create entities for testing
def create_sample_traverse(name: str = "Test Traverse") -> dips.OrientationDataSetVal.OrientationDataSetVal:
    """Create a sample traverse for testing."""
    ods = dips.OrientationDataSetVal.OrientationDataSetVal()
    ods.name = name
    ods.orientation_convention = DipsAPI_pb2.eOrientationConvention.TrendPlungeOrientation
    ods.orientation_data_type = DipsAPI_pb2.eOrientationDataType.SpotMapping
    ods.discontinuity_orientation_convention = DipsAPI_pb2.eOrientationConvention.TrendPlungeOrientation
    
    # Use built-in unit formatters
    ods.traverse_elevation_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    ods.traverse_xyz_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    ods.traverse_depth_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    ods.survey_distance_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    ods.discontinuity_distance_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    ods.discontinuity_xyz_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    ods.discontinuity_persistence_unit = BuiltInDataFormatters.LengthMeterDataFormmatter
    
    # Add a few sample discontinuities
    for i in range(5):
        discontinuity = dips.DiscontinuityDataVal.DiscontinuityDataVal()
        discontinuity.orientation1.angle_radians = math.radians(45 + i * 10)
        discontinuity.orientation2.angle_radians = math.radians(30 + i * 5)
        discontinuity.quantity = 1.0 + i * 0.1
        ods.discontinuity_list.append(discontinuity)
    
    return ods


def create_sample_set(set_id: str = "Test Set") -> dips.SetEntityInfoVal.SetEntityInfoVal:
    """Create a sample circular set for testing."""
    # Create the set window entity info
    set_window_info = dips.SetWindowEntityInfoVal.SetWindowEntityInfoVal()
    set_window_info.set_window_type = DipsAPI_pb2.eSetWindowType.Circular
    
    # Set the color
    window_color = create_color(255, 0, 0)
    set_window_info.color = window_color
    
    # Configure statistics settings
    stats_settings = dips.SetStatisticsSettingsVal.SetStatisticsSettingsVal()
    stats_settings.one_std_dev = True
    stats_settings.two_std_dev = True
    stats_settings.three_std_dev = False
    stats_settings.use_custom_interval = False
    stats_settings.custom_interval = 10.0
    set_window_info.statistics_settings = stats_settings
    
    # Create circular window
    circular_window = dips.CircularWindowVal.CircularWindowVal()
    circular_window.id = set_id
    
    # Create center point (TrendPlunge)
    center = create_trend_plunge(90.0, 45.0)
    circular_window.center = center
    
    # Create cone angle
    cone_angle = dips.AngleDataVal.AngleDataVal()
    cone_angle.angle_radians = math.radians(30.0)
    circular_window.cone_angle = cone_angle
    
    set_window_info.circular_set_window = circular_window
    
    # Create the set entity info
    set_info = dips.SetEntityInfoVal.SetEntityInfoVal()
    set_info.id = set_id
    set_info.color = window_color
    set_info.set_window_entity_info = set_window_info
    
    return set_info


def create_sample_user_plane(plane_id: str = "Test Plane", trend_deg: float = 90.0, plunge_deg: float = 45.0) -> dips.PlaneEntityInfoVal.PlaneEntityInfoVal:
    """Create a sample user plane for testing."""
    plane_info = dips.PlaneEntityInfoVal.PlaneEntityInfoVal()
    plane_info.color = create_color(0, 255, 0)
    
    # Create the plane
    plane = dips.PlaneVal.PlaneVal()
    plane.id = plane_id
    plane.pole = create_trend_plunge(trend_deg, plunge_deg)
    plane.quantity = 1.0
    plane.weight = 1.0
    plane_info.plane = plane
    
    return plane_info


def create_sample_fold(fold_id: str = "Test Fold") -> dips.FoldEntityInfoVal.FoldEntityInfoVal:
    """Create a sample fold for testing."""
    fold_info = dips.FoldEntityInfoVal.FoldEntityInfoVal()
    fold_info.id = fold_id
    fold_info.color = create_color(255, 0, 255)
    
    # Create fold window entity info
    fold_window_info = dips.FoldWindowEntityInfoVal.FoldWindowEntityInfoVal()
    fold_window_info.color = create_color(255, 0, 255)
    
    # Create wrapped freehand window
    wrapped_window = dips.WrappedFreehandWindowVal.WrappedFreehandWindowVal()
    wrapped_window.id = fold_id
    
    # Create primary window with a simple polygon (at least 3 points)
    primary_window = dips.FreehandWindowVal.FreehandWindowVal()
    primary_window.polygon.append( create_trend_plunge(0.0, 0.0))
    primary_window.polygon.append( create_trend_plunge(90.0, 0.0))
    primary_window.polygon.append( create_trend_plunge(180.0, 0.0))
        
    primary_window.is_wrapped = False
    wrapped_window.primary_window = primary_window
    
    # Create secondary window
    secondary_window = dips.FreehandWindowVal.FreehandWindowVal()
    #secondary_window.polygon = []
    secondary_window.is_wrapped = False
    wrapped_window.secondary_window = secondary_window
    
    fold_window_info.wrapped_freehand_fold_window = wrapped_window
    fold_info.fold_window_entity_info = fold_window_info
    
    return fold_info


# Helper functions to create valid tool data
def create_color(r: int, g: int, b: int) -> dips.ColorSurrogateVal.ColorSurrogateVal:
    """Create a ColorSurrogate."""
    color = dips.ColorSurrogateVal.ColorSurrogateVal()
    color.r = r
    color.g = g
    color.b = b
    color.a = 255
    return color


def create_trend_plunge(trend_deg: float, plunge_deg: float) -> dips.TrendPlungeVal.TrendPlungeVal:
    """Create a TrendPlunge."""
    tp = dips.TrendPlungeVal.TrendPlungeVal()
    tp.trend = dips.AngleDataVal.AngleDataVal()
    tp.trend.angle_radians = math.radians(trend_deg)
    tp.plunge = dips.AngleDataVal.AngleDataVal()
    tp.plunge.angle_radians = math.radians(plunge_deg)
    return tp


def create_anchor_point_spherical(trend_deg: float, plunge_deg: float) -> dips.AnchorPointVal.AnchorPointVal:
    """Create an AnchorPoint with spherical coordinates."""
    anchor = dips.AnchorPointVal.AnchorPointVal()
    anchor.coordinate_option = DipsAPI_pb2.eAnchorCoordinateOption.Spherical
    anchor.spherical_point = create_trend_plunge(trend_deg, plunge_deg)
    return anchor


def create_anchor_point_logical(x: float, y: float) -> dips.AnchorPointVal.AnchorPointVal:
    """Create an AnchorPoint with logical coordinates."""
    anchor = dips.AnchorPointVal.AnchorPointVal()
    anchor.coordinate_option = DipsAPI_pb2.eAnchorCoordinateOption.Logical
    anchor.logical_point = dips.Vector2DVal.Vector2DVal()
    anchor.logical_point.x = x
    anchor.logical_point.y = y
    return anchor


def create_text_tool(name: str, text: str, trend_deg: float = 90, plunge_deg: float = 45) -> TextToolEntityInfoVal:
    """Create a valid TextToolEntityInfo with all required fields."""
    tool = TextToolEntityInfoVal()
    tool.name = name
    tool.is_visible = True
    tool.text = text
    tool.anchor_point = create_anchor_point_spherical(trend_deg, plunge_deg)
    
    # Set line format (required)
    line_format = dips.LineFormatVal.LineFormatVal()
    line_format.line_color = create_color(0, 0, 0)
    line_format.line_width = 2
    tool.line_format = line_format
    
    # Set fill format (optional but good practice)
    fill_format = dips.FillFormatVal.FillFormatVal()
    fill_format.apply_fill = False
    fill_format.fill_color = create_color(255, 255, 255)
    tool.fill_format = fill_format
    
    # Set text format (required)
    text_format = dips.TextFormatVal.TextFormatVal()
    text_format.text_horizontal_alignment = DipsAPI_pb2.eTextHorizontalAlignment.Center
    text_format.text_color = create_color(0, 0, 0)
    text_format.font_name = "Arial"
    text_format.font_size = 12
    tool.text_format = text_format
    
    return tool


def create_arrow_tool(name: str = "Arrow") -> ArrowToolEntityInfoVal:
    """Create a valid ArrowToolEntityInfo with all required fields."""
    tool = ArrowToolEntityInfoVal()
    tool.name = name
    tool.is_visible = True
    tool.anchor_point = create_anchor_point_logical(0.0, 0.0)
    tool.anchor_point_secondary = create_anchor_point_logical(0.5, 0.5)
    
    # Set line format (required)
    line_format = dips.LineFormatVal.LineFormatVal()
    line_format.line_color = create_color(0, 0, 0)
    line_format.line_width = 2
    tool.line_format = line_format
    
    tool.show_arrow = True
    tool.show_arrow_secondary = False
    
    return tool


def create_line_tool(name: str = "Line") -> LineToolEntityInfoVal:
    """Create a valid LineToolEntityInfo with all required fields."""
    tool = LineToolEntityInfoVal()
    tool.name = name
    tool.is_visible = True
    tool.anchor_point = create_anchor_point_logical(0.0, 0.0)
    tool.anchor_point_secondary = create_anchor_point_logical(0.5, 0.5)
    
    # Set line format (required)
    line_format = dips.LineFormatVal.LineFormatVal()
    line_format.line_color = create_color(0, 0, 0)
    line_format.line_width = 2
    tool.line_format = line_format
    
    return tool


@pytest.mark.integration
class TestEntityVisibilityOperations:
    """Test cases for entity visibility operations across different views."""
    
    def test_set_user_plane_entity_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting user plane entity visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 50, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a user plane first
            plane_data = create_sample_user_plane("Test Plane for Visibility")
            plane_ref = model.AddUserPlane(plane_data)
            assert plane_ref is not None, "Failed to create user plane"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get user plane entity visibilities
            entities = view_2d.GetUserPlaneEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "User plane entity should be available after creating user plane"
            
            entity = entities[0]
            
            # Set visibility to True (returns void, no ValidatableResult)
            entity.SetUserPlaneEntityVisibility(True)  # Returns void
            
            # Verify the change
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
            
            # Toggle to False (returns void, no ValidatableResult)
            entity.SetUserPlaneEntityVisibility(False)  # Returns void
            
            entity_value = entity.GetValue()
            assert entity_value.is_visible == False
                
        finally:
            app.Close()
    
    def test_set_user_plane_entity_visibility_3d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting user plane entity visibility in 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 51, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a user plane first
            plane_data = create_sample_user_plane("Test Plane for 3D Visibility")
            plane_ref = model.AddUserPlane(plane_data)
            assert plane_ref is not None, "Failed to create user plane"
            
            
            # Create a 3D Stereonet view
            view_3d = model.CreateStereonet3DView()
            
            # Get user plane entity visibilities
            entities = view_3d.GetUserPlaneEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "User plane entity should be available after creating user plane"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetUserPlaneEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_user_plane_entity_visibility_rosette(self, dips_app_path, dips_base_port):
        """Test setting user plane entity visibility in Rosette view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 52, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a user plane first
            plane_data = create_sample_user_plane("Test Plane for Rosette Visibility")
            plane_ref = model.AddUserPlane(plane_data)
            assert plane_ref is not None, "Failed to create user plane"

            # Create a Rosette view
            rosette_view = model.CreateRosetteView()
            
            # Get user plane entity visibilities
            entities = rosette_view.GetUserPlaneEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "User plane entity should be available after creating user plane"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetUserPlaneEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_mean_set_plane_entity_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting mean set plane entity visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 53, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a set first (mean set planes are derived from sets)
            set_data = create_sample_set("Test Set for Mean Plane")
            set_ref = model.CreateSetWindow(set_data)
            assert set_ref is not None, "Failed to create set"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get mean set plane entity visibilities
            entities = view_2d.GetMeanSetPlaneEntityVisibilities()
            
            # Should have at least one entity now (mean set plane is derived from the set)
            assert len(entities) > 0, "Mean set plane entity should be available after creating set"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetMeanSetPlaneEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_mean_set_plane_entity_visibility_3d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting mean set plane entity visibility in 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 54, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a set first (mean set planes are derived from sets)
            set_data = create_sample_set("Test Set for 3D Mean Plane")
            set_ref = model.CreateSetWindow(set_data)
            assert set_ref is not None, "Failed to create set"
            
            # Create a 3D Stereonet view
            view_3d = model.CreateStereonet3DView()
            
            # Get mean set plane entity visibilities
            entities = view_3d.GetMeanSetPlaneEntityVisibilities()
            
            # Should have at least one entity now (mean set plane is derived from the set)
            assert len(entities) > 0, "Mean set plane entity should be available after creating set"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetMeanSetPlaneEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_set_window_entity_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting set window entity visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 55, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a set first
            set_data = create_sample_set("Test Set for Visibility")
            set_ref = model.CreateSetWindow(set_data)
            assert set_ref is not None, "Failed to create set"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get set window entity visibilities
            entities = view_2d.GetSetWindowEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Set window entity should be available after creating set"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetSetWindowEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_set_window_entity_visibility_3d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting set window entity visibility in 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 56, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a set first
            set_data = create_sample_set("Test Set for 3D Visibility")
            set_ref = model.CreateSetWindow(set_data)
            assert set_ref is not None, "Failed to create set"
            
            # Create a 3D Stereonet view
            view_3d = model.CreateStereonet3DView()
            
            # Get set window entity visibilities
            entities = view_3d.GetSetWindowEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Set window entity should be available after creating set"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetSetWindowEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_traverse_entity_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting traverse entity visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 57, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a traverse first
            traverse_data = create_sample_traverse("Test Traverse for Visibility")
            traverse_ref = model.AddTraverse(traverse_data)
            assert traverse_ref is not None, "Failed to create traverse"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get traverse entity visibilities
            entities = view_2d.GetTraverseEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Traverse entity should be available after creating traverse"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetTraverseEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_traverse_entity_visibility_3d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting traverse entity visibility in 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 58, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a traverse first
            traverse_data = create_sample_traverse("Test Traverse for 3D Visibility")
            traverse_ref = model.AddTraverse(traverse_data)
            assert traverse_ref is not None, "Failed to create traverse"
            
            # Create a 3D Stereonet view
            view_3d = model.CreateStereonet3DView()
            
            # Get traverse entity visibilities
            entities = view_3d.GetTraverseEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Traverse entity should be available after creating traverse"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetTraverseEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_fold_entity_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting fold entity visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 59, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a fold first
            fold_data = create_sample_fold("Test Fold for Visibility")
            fold_ref = model.AddFold(fold_data)
            assert fold_ref is not None, "Failed to create fold"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get fold entity visibilities
            entities = view_2d.GetFoldEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Fold entity should be available after creating fold"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetFoldEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_fold_window_entity_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting fold window entity visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 60, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a fold first (fold windows are part of folds)
            fold_data = create_sample_fold("Test Fold for Window Visibility")
            fold_ref = model.AddFold(fold_data)
            assert fold_ref is not None, "Failed to create fold"

            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get fold window entity visibilities
            entities = view_2d.GetFoldWindowEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Fold window entity should be available after creating fold"
            
            entity = entities[0]
            
            # Set visibility (returns void, no ValidatableResult)
            entity.SetFoldWindowEntityVisibility(True)  # Returns void
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()


@pytest.mark.integration
class TestEntityOptionsOperations:
    """Test cases for entity options operations across different views."""
    
    def test_set_user_plane_entity_options_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting user plane entity options in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 70, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a user plane first
            plane_data = create_sample_user_plane("Test Plane for Options")
            plane_ref = model.AddUserPlane(plane_data)
            assert plane_ref is not None, "Failed to create user plane"
   
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get user plane entity visibilities
            entities = view_2d.GetUserPlaneEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "User plane entity should be available after creating user plane"
            
            entity = entities[0]
            
            # Get current value
            current_value = entity.GetValue()
            
            # Create updated options (clone the current value)
            updated_options = PlaneEntityVisibilityVal.from_proto(current_value.to_proto())
            updated_options.is_visible = True
            
            # Set options
            result = entity.SetUserPlaneEntityOptions(updated_options)
            assert len(result.errors) == 0, f"Set options failed: {[e.error_message for e in result.errors]}"
            
            # Verify the change
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_user_plane_entity_options_rosette(self, dips_app_path, dips_base_port):
        """Test setting user plane entity options in Rosette view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 71, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a user plane first
            plane_data = create_sample_user_plane("Test Plane for Rosette Options")
            plane_ref = model.AddUserPlane(plane_data)
            assert plane_ref is not None, "Failed to create user plane"
            
            # Create a Rosette view
            rosette_view = model.CreateRosetteView()
            
            # Get user plane entity visibilities
            entities = rosette_view.GetUserPlaneEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "User plane entity should be available after creating user plane"
            
            entity = entities[0]
            
            # Get current value
            current_value = entity.GetValue()
            
            # Create updated options
            updated_options = PlaneEntityVisibilityVal.from_proto(current_value.to_proto())
            updated_options.is_visible = False
            
            # Set options
            result = entity.SetUserPlaneEntityOptions(updated_options)
            assert len(result.errors) == 0
            
            # Verify
            entity_value2 = entity.GetValue()
            assert entity_value2.is_visible == False
                
        finally:
            app.Close()
    
    def test_set_mean_set_plane_entity_options_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting mean set plane entity options in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 72, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a set first (mean set planes are derived from sets)
            set_data = create_sample_set("Test Set for Mean Plane Options")
            set_ref = model.CreateSetWindow(set_data)
            assert set_ref is not None, "Failed to create set"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get mean set plane entity visibilities
            entities = view_2d.GetMeanSetPlaneEntityVisibilities()
            
            # Should have at least one entity now (mean set plane is derived from the set)
            assert len(entities) > 0, "Mean set plane entity should be available after creating set"
            
            entity = entities[0]
            
            # Get current value
            current_value = entity.GetValue()
            
            # Create updated options
            updated_options = SetEntityVisibilityVal.from_proto(current_value.to_proto())
            updated_options.is_visible = True
            
            # Set options
            result = entity.SetMeanSetPlaneEntityOptions(updated_options)
            assert len(result.errors) == 0
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_mean_set_plane_entity_options_3d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting mean set plane entity options in 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 73, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a set first (mean set planes are derived from sets)
            set_data = create_sample_set("Test Set for 3D Mean Plane Options")
            set_ref = model.CreateSetWindow(set_data)
            assert set_ref is not None, "Failed to create set"
            
            # Create a 3D Stereonet view
            view_3d = model.CreateStereonet3DView()
            
            # Get mean set plane entity visibilities
            entities = view_3d.GetMeanSetPlaneEntityVisibilities()
            
            # Should have at least one entity now (mean set plane is derived from the set)
            assert len(entities) > 0, "Mean set plane entity should be available after creating set"
            
            entity = entities[0]
            
            # Get current value
            current_value = entity.GetValue()
            
            # Create updated options
            updated_options = SetEntityVisibilityVal.from_proto(current_value.to_proto())
            updated_options.is_visible = False
            
            # Set options
            result = entity.SetMeanSetPlaneEntityOptions(updated_options)
            assert len(result.errors) == 0
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == False
                
        finally:
            app.Close()
    
    def test_set_traverse_entity_options_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting traverse entity options in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 74, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a traverse first
            traverse_data = create_sample_traverse("Test Traverse for Options")
            traverse_ref = model.AddTraverse(traverse_data)
            assert traverse_ref is not None, "Failed to create traverse"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get traverse entity visibilities
            entities = view_2d.GetTraverseEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Traverse entity should be available after creating traverse"
            
            entity = entities[0]
            
            # Get current value
            current_value = entity.GetValue()
            
            # Create updated options
            updated_options = TraverseEntityVisibilityVal.from_proto(current_value.to_proto())
            updated_options.is_visible = True
            
            # Set options
            result = entity.SetTraverseEntityOptions(updated_options)
            assert len(result.errors) == 0
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()
    
    def test_set_fold_entity_options_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting fold entity options in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 75, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a fold first
            fold_data = create_sample_fold("Test Fold for Options")
            fold_ref = model.AddFold(fold_data)
            assert fold_ref is not None, "Failed to create fold"
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Get fold entity visibilities
            entities = view_2d.GetFoldEntityVisibilities()
            
            # Should have at least one entity now
            assert len(entities) > 0, "Fold entity should be available after creating fold"
            
            entity = entities[0]
            
            # Get current value
            current_value = entity.GetValue()
            
            # Create updated options
            updated_options = FoldEntityVisibilityVal.from_proto(current_value.to_proto())
            updated_options.is_visible = True
            
            # Set options
            result = entity.SetFoldEntityOptions(updated_options)
            assert len(result.errors) == 0
            
            # Verify
            entity_value = entity.GetValue()
            assert entity_value.is_visible == True
                
        finally:
            app.Close()


@pytest.mark.integration
class TestToolOperations:
    """Test cases for tool operations across different views."""
    
    def test_add_and_remove_text_tool_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test adding and removing text tool in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 80, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Create a valid text tool with all required fields
            text_tool = create_text_tool("Test Text Tool", "Test Text Tool")
            
            # Add the tool (returns reference directly, raises exception on error)
            tool_ref = view_2d.AddStereonet2DTextTool(text_tool)
            assert tool_ref is not None, "Tool reference should be returned"
            
            # Verify the tool appears in the list
            tools = view_2d.GetStereonet2DTextTools()
            assert len(tools) > 0
            assert any(t.get_model_ref().ID == tool_ref.get_model_ref().ID for t in tools)
            
            # Remove the tool (returns void, no ValidatableResult)
            tool_entity = tools[0]  # Get the first tool
            tool_entity.RemoveTextTool()  # Returns void
            
            # Verify the tool is removed
            tools_after = view_2d.GetStereonet2DTextTools()
            assert len(tools_after) < len(tools)
            
        finally:
            app.Close()
    
    def test_add_and_remove_text_tool_rosette(self, dips_app_path, dips_base_port):
        """Test adding and removing text tool in Rosette view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 81, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a Rosette view
            rosette_view = model.CreateRosetteView()
            
            # Create a valid text tool with all required fields
            text_tool = create_text_tool("Rosette Text Tool", "Rosette Text Tool")
            
            # Add the tool (returns reference directly)
            tool_ref = rosette_view.AddRosetteTextTool(text_tool)
            assert tool_ref is not None
            
            # Verify the tool appears in the list
            tools = rosette_view.GetRosetteTextTools()
            assert len(tools) > 0
            assert any(t.get_model_ref().ID == tool_ref.get_model_ref().ID for t in tools)
            
            # Remove the tool (returns void, no ValidatableResult)
            tool_entity = tools[0]
            tool_entity.RemoveTextTool()  # Returns void
            
        finally:
            app.Close()
    
    def test_update_text_tool_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test updating text tool in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 82, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Create and add a valid text tool with all required fields
            text_tool = create_text_tool("Original Text", "Original Text")
            
            tool_ref = view_2d.AddStereonet2DTextTool(text_tool)
            assert tool_ref is not None
            
            # Get the tool
            tools = view_2d.GetStereonet2DTextTools()
            assert len(tools) > 0
            tool_entity = tools[0]
            
            # Get current value
            current_value = tool_entity.GetValue()
            
            # Create updated tool (clone preserves all required fields)
            updated_tool = TextToolEntityInfoVal.from_proto(current_value.to_proto())
            updated_tool.text = "Updated Text"
            # Ensure name is set (required by validator)
            if not updated_tool.name or updated_tool.name == "":
                updated_tool.name = "Updated Text Tool"
            
            # Update the tool
            update_result = tool_entity.UpdateTextTool(updated_tool)
            assert len(update_result.errors) == 0
            
            # Verify the update
            updated_value = tool_entity.GetValue()
            assert updated_value.text == "Updated Text"
            
        finally:
            app.Close()
    
    def test_set_text_tool_visibility_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test setting text tool visibility in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 83, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Create and add a valid text tool with all required fields
            text_tool = create_text_tool("Test Tool", "Test Tool")
            
            tool_ref = view_2d.AddStereonet2DTextTool(text_tool)
            assert tool_ref is not None
            
            # Get the tool
            tools = view_2d.GetStereonet2DTextTools()
            assert len(tools) > 0
            tool_entity = tools[0]
            
            # Set visibility to False (returns void, no ValidatableResult)
            tool_entity.SetTextToolVisibility(False)  # Returns void
            
            # Verify
            tool_value = tool_entity.GetValue()
            assert tool_value.is_visible == False
            
            # Toggle back to True (returns void, no ValidatableResult)
            tool_entity.SetTextToolVisibility(True)  # Returns void
            
            tool_value = tool_entity.GetValue()
            assert tool_value.is_visible == True
            
        finally:
            app.Close()
    
    def test_add_and_remove_arrow_tool_2d_stereonet(self, dips_app_path, dips_base_port):
        """Test adding and removing arrow tool in 2D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 84, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a 2D Stereonet view
            view_2d = model.CreateStereonet2DView()
            
            # Create a valid arrow tool with all required fields
            arrow_tool = create_arrow_tool("Test Arrow")
            
            # Add the tool (returns reference directly)
            tool_ref = view_2d.AddStereonet2DArrowTool(arrow_tool)
            assert tool_ref is not None
            
            # Verify the tool appears in the list
            tools = view_2d.GetStereonet2DArrowTools()
            assert len(tools) > 0
            
            # Remove the tool (returns void, no ValidatableResult)
            tool_entity = tools[0]
            tool_entity.RemoveArrowTool()  # Returns void
            
        finally:
            app.Close()
    
    def test_add_and_remove_line_tool_rosette(self, dips_app_path, dips_base_port):
        """Test adding and removing line tool in Rosette view."""
        #app = DipsApp.DipsApp.LaunchApp(dips_base_port + 85, dips_app_path)
        app = DipsApp.DipsApp.AttachToExisting(dips_base_port )

        try:
            model = app.GetModel()
            
            # Create a Rosette view
            rosette_view = model.CreateRosetteView()
            
            # Create a valid line tool with all required fields
            line_tool = create_line_tool("Test Line")
            
            # Add the tool (returns reference directly)
            tool_ref = rosette_view.AddRosetteLineTool(line_tool)
            assert tool_ref is not None
            
            # Verify the tool appears in the list
            tools = rosette_view.GetRosetteLineTools()
            assert len(tools) > 0
            
            # Remove the tool (returns void, no ValidatableResult)
            tool_entity = tools[0]
            tool_entity.RemoveLineTool()  # Returns void
            
        finally:
            app.Close()
    
    def test_cross_view_entity_operations(self, dips_app_path, dips_base_port):
        """Test that entity operations work correctly across different views."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 90, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create multiple views
            view_2d = model.CreateStereonet2DView()
            view_3d = model.CreateStereonet3DView()
            rosette_view = model.CreateRosetteView()
            
            # Test that we can get entities from each view
            entities_2d = view_2d.GetUserPlaneEntityVisibilities()
            entities_3d = view_3d.GetUserPlaneEntityVisibilities()
            entities_rosette = rosette_view.GetUserPlaneEntityVisibilities()
            
            # All should return lists (even if empty)
            assert isinstance(entities_2d, list)
            assert isinstance(entities_3d, list)
            assert isinstance(entities_rosette, list)
            
            # If entities exist, test operations on them (returns void, no ValidatableResult)
            if len(entities_2d) > 0:
                entities_2d[0].SetUserPlaneEntityVisibility(True)  # Returns void
            
            if len(entities_3d) > 0:
                entities_3d[0].SetUserPlaneEntityVisibility(True)  # Returns void
            
            if len(entities_rosette) > 0:
                entities_rosette[0].SetUserPlaneEntityVisibility(True)  # Returns void
            
        finally:
            app.Close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

