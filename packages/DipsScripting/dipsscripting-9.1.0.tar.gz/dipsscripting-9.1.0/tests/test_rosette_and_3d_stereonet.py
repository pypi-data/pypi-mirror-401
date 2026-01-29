"""
Integration tests for Rosette and 3D Stereonet view functionality.
These tests require a running Dips application or will launch one.
"""
import pytest
import math
from dips import DipsApp
from dips import DipsAPI_pb2
from dips.StereonetProjectionModeVal import StereonetProjectionModeVal
from dips.RosetteSettingsVal import RosetteSettingsVal
from dips.TrendPlungeVal import TrendPlungeVal
from dips.AngleDataVal import AngleDataVal
from dips.ValidatableResultVal import ValidatableResultVal


@pytest.mark.integration
class TestRosetteViews:
    """Test cases for Rosette view operations."""
    
    def test_get_rosettes(self, dips_app_path, dips_base_port):
        """Test getting the list of Rosette views."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 20, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Get the list of Rosette views
            rosettes = model.GetRosettes()
            
            # Verify we got a list
            assert rosettes is not None
            assert isinstance(rosettes, list)
            
        finally:
            app.Close()
    
    def test_create_rosette_view(self, dips_app_path, dips_base_port):
        """Test creating a new Rosette view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 21, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new Rosette view
            rosette_view = model.CreateRosetteView()
            
            # Verify the view was created
            assert rosette_view is not None
            
            # Get the view value to check its properties
            view_value = rosette_view.GetValue()
            assert view_value is not None
            assert hasattr(view_value, 'view_name')
            
            # Verify the view appears in the list
            rosettes = model.GetRosettes()
            assert len(rosettes) > 0
            assert any(r.GetValue().view_name == view_value.view_name for r in rosettes)
            
        finally:
            app.Close()
    
    def test_close_rosette_view(self, dips_app_path, dips_base_port):
        """Test closing a Rosette view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 22, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            rosette_view = model.CreateRosetteView()
            view_value = rosette_view.GetValue()
            view_name = view_value.view_name
            
            # Close the view
            rosette_view.CloseRosetteView()
            
            # Verify the view is no longer in the list
            rosettes = model.GetRosettes()
            assert not any(r.GetValue().view_name == view_name for r in rosettes)
            
        finally:
            app.Close()
    
    def test_set_rosette_settings(self, dips_app_path, dips_base_port):
        """Test setting Rosette settings."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 23, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            rosette_view = model.CreateRosetteView()
            
            # Create and set Rosette settings with all required fields for validation
            settings = RosetteSettingsVal()
            settings.is_weighted = True
            
            # Set sight line orientation (trend: 90 degrees, plunge: 45 degrees)
            sight_line = TrendPlungeVal()
            sight_line.trend = AngleDataVal()
            sight_line.trend.angle_radians = math.radians(90.0)
            sight_line.plunge = AngleDataVal()
            sight_line.plunge.angle_radians = math.radians(45.0)
            settings.sight_line_orientation = sight_line
            
            # Set min angle (10 degrees - lower hemisphere plunge, 0-90)
            min_angle = AngleDataVal()
            min_angle.angle_radians = math.radians(10.0)
            settings.min_angle = min_angle
            
            # Set max angle (80 degrees - must be > min_angle, lower hemisphere plunge, 0-90)
            max_angle = AngleDataVal()
            max_angle.angle_radians = math.radians(80.0)
            settings.max_angle = max_angle
            
            # Set start bin strike (0 degrees - compass trend, 0-360)
            start_bin = AngleDataVal()
            start_bin.angle_radians = math.radians(0.0)
            settings.start_bin_strike = start_bin
            
            # Set num bins (36 - must be between 1 and 360)
            settings.num_bins = 36
            
            # Set num planes per circle increment (1 - must be >= 1)
            settings.num_planes_per_circle_increment = 1
            
            # Set the settings and check for validation errors
            result = rosette_view.SetRosetteSettings(settings)
            
            # Verify no validation errors
            assert result is not None
            assert len(result.errors) == 0, f"Validation failed with errors: {[e.error_message for e in result.errors]}"
            
            # Verify the setting was applied (by checking the view value)
            view_value = rosette_view.GetValue()
            assert view_value.rosette_settings is not None
            assert view_value.rosette_settings.is_weighted == True
            assert view_value.rosette_settings.num_bins == 36
            
        finally:
            app.Close()
    
    def test_set_projection_mode(self, dips_app_path, dips_base_port):
        """Test setting projection mode for Rosette view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 24, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            rosette_view = model.CreateRosetteView()
            
            # Set projection mode
            projection_mode = StereonetProjectionModeVal()
            projection_mode.hemisphere_draw_option = DipsAPI_pb2.eHemisphereDrawOption.Lower
            projection_mode.projection_method_draw_option = DipsAPI_pb2.eProjectionMethodDrawOption.EqualArea
            rosette_view.SetProjectionMode(projection_mode)
            
            # Verify the setting was applied
            view_value = rosette_view.GetValue()
            assert view_value.projection_mode is not None
            assert view_value.projection_mode.hemisphere_draw_option == DipsAPI_pb2.eHemisphereDrawOption.Lower
            assert view_value.projection_mode.projection_method_draw_option == DipsAPI_pb2.eProjectionMethodDrawOption.EqualArea
            
        finally:
            app.Close()
    
    def test_set_user_plane_entity_group_visibility(self, dips_app_path, dips_base_port):
        """Test setting user plane entity group visibility."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 25, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            rosette_view = model.CreateRosetteView()
            
            # Set visibility
            rosette_view.SetUserPlaneEntityGroupVisibility(True)
            
            # Toggle it
            rosette_view.SetUserPlaneEntityGroupVisibility(False)
            rosette_view.SetUserPlaneEntityGroupVisibility(True)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_set_tools_entity_group_visibility(self, dips_app_path, dips_base_port):
        """Test setting tools entity group visibility."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 26, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            rosette_view = model.CreateRosetteView()
            
            # Set visibility
            rosette_view.SetToolsEntityGroupVisibility(True)
            rosette_view.SetToolsEntityGroupVisibility(False)
            rosette_view.SetToolsEntityGroupVisibility(True)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_get_user_plane_entity_visibilities(self, dips_app_path, dips_base_port):
        """Test getting user plane entity visibilities."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 27, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            rosette_view = model.CreateRosetteView()
            
            # Get user plane entity visibilities
            entities = rosette_view.GetUserPlaneEntityVisibilities()
            
            # Verify we got a list
            assert entities is not None
            assert isinstance(entities, list)
            
        finally:
            app.Close()


@pytest.mark.integration
class TestStereonet3DViews:
    """Test cases for 3D Stereonet view operations."""
    
    def test_get_3d_stereonets(self, dips_app_path, dips_base_port):
        """Test getting the list of 3D Stereonet views."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 30, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Get the list of 3D Stereonet views
            stereonets_3d = model.Get3DStereonets()
            
            # Verify we got a list
            assert stereonets_3d is not None
            assert isinstance(stereonets_3d, list)
            
        finally:
            app.Close()
    
    def test_create_3d_stereonet_view(self, dips_app_path, dips_base_port):
        """Test creating a new 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 31, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new 3D Stereonet view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Verify the view was created
            assert stereonet_3d_view is not None
            
            # Get the view value to check its properties
            view_value = stereonet_3d_view.GetValue()
            assert view_value is not None
            assert hasattr(view_value, 'view_name')
            
            # Verify the view appears in the list
            stereonets_3d = model.Get3DStereonets()
            assert len(stereonets_3d) > 0
            assert any(s.GetValue().view_name == view_value.view_name for s in stereonets_3d)
            
        finally:
            app.Close()
    
    def test_close_3d_stereonet_view(self, dips_app_path, dips_base_port):
        """Test closing a 3D Stereonet view."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 32, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            view_value = stereonet_3d_view.GetValue()
            view_name = view_value.view_name
            
            # Close the view
            stereonet_3d_view.CloseStereonet3DView()
            
            # Verify the view is no longer in the list
            stereonets_3d = model.Get3DStereonets()
            assert not any(s.GetValue().view_name == view_name for s in stereonets_3d)
            
        finally:
            app.Close()
    
    def test_set_pole_entity_visibility(self, dips_app_path, dips_base_port):
        """Test setting pole entity visibility for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 33, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set visibility
            stereonet_3d_view.SetPoleEntityVisibility(True)
            stereonet_3d_view.SetPoleEntityVisibility(False)
            stereonet_3d_view.SetPoleEntityVisibility(True)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_set_intersection_entity_visibility(self, dips_app_path, dips_base_port):
        """Test setting intersection entity visibility for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 34, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set visibility
            stereonet_3d_view.SetIntersectionEntityVisibility(True)
            stereonet_3d_view.SetIntersectionEntityVisibility(False)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_set_contour_entity_visibility(self, dips_app_path, dips_base_port):
        """Test setting contour entity visibility for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 35, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set visibility
            stereonet_3d_view.SetContourEntityVisibility(True)
            stereonet_3d_view.SetContourEntityVisibility(False)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_set_is_weighted(self, dips_app_path, dips_base_port):
        """Test setting is weighted for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 36, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set is weighted
            stereonet_3d_view.SetIsWeighted(True)
            
            # Verify the setting was applied
            view_value = stereonet_3d_view.GetValue()
            assert view_value.is_weighted == True
            
            # Toggle it
            stereonet_3d_view.SetIsWeighted(False)
            view_value = stereonet_3d_view.GetValue()
            assert view_value.is_weighted == False
            
        finally:
            app.Close()
    
    def test_set_vector_mode(self, dips_app_path, dips_base_port):
        """Test setting vector mode for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 37, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set vector mode
            stereonet_3d_view.SetVectorMode(DipsAPI_pb2.eVectorMode.Pole)
            
            # Verify the setting was applied
            view_value = stereonet_3d_view.GetValue()
            assert view_value.vector_mode == DipsAPI_pb2.eVectorMode.Pole
            
            # Change to another mode
            stereonet_3d_view.SetVectorMode(DipsAPI_pb2.eVectorMode.Dip)
            view_value = stereonet_3d_view.GetValue()
            assert view_value.vector_mode == DipsAPI_pb2.eVectorMode.Dip
            
        finally:
            app.Close()
    
    def test_set_user_plane_entity_group_visibility(self, dips_app_path, dips_base_port):
        """Test setting user plane entity group visibility for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 38, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set visibility
            stereonet_3d_view.SetUserPlaneEntityGroupVisibility(True)
            stereonet_3d_view.SetUserPlaneEntityGroupVisibility(False)
            stereonet_3d_view.SetUserPlaneEntityGroupVisibility(True)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_set_set_window_entity_group_visibility(self, dips_app_path, dips_base_port):
        """Test setting set window entity group visibility for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 39, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Set visibility
            stereonet_3d_view.SetSetWindowEntityGroupVisibility(True)
            stereonet_3d_view.SetSetWindowEntityGroupVisibility(False)
            
            # If no exception, the operation succeeded
            assert True
            
        finally:
            app.Close()
    
    def test_get_user_plane_entity_visibilities(self, dips_app_path, dips_base_port):
        """Test getting user plane entity visibilities for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 40, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Get user plane entity visibilities
            entities = stereonet_3d_view.GetUserPlaneEntityVisibilities()
            
            # Verify we got a list
            assert entities is not None
            assert isinstance(entities, list)
            
        finally:
            app.Close()
    
    def test_get_set_window_entity_visibilities(self, dips_app_path, dips_base_port):
        """Test getting set window entity visibilities for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 41, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Get set window entity visibilities
            entities = stereonet_3d_view.GetSetWindowEntityVisibilities()
            
            # Verify we got a list
            assert entities is not None
            assert isinstance(entities, list)
            
        finally:
            app.Close()
    
    def test_get_active_data_filter(self, dips_app_path, dips_base_port):
        """Test getting active data filter for 3D Stereonet."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 42, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create a new view
            stereonet_3d_view = model.CreateStereonet3DView()
            
            # Get active data filter (may be None)
            active_filter = stereonet_3d_view.GetActiveDataFilter()
            
            # Verify we got a result (even if None)
            # The method should not raise an exception
            assert True
            
        finally:
            app.Close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


