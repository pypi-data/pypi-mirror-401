"""
Integration tests for the Dips application.
These tests require a running Dips application or will launch one.
"""
import pytest
import math
from dips import DipsApp
from dips import BuiltInDataFormatters
from dips import DipsAPI_pb2
from dips import OrientationDataSetVal
from dips import DiscontinuityDataVal
from dips import AngleDataVal


class TestAppLaunch:
    """Test cases for launching the Dips application."""
    
    def test_launch_application(self, dips_app_path, dips_base_port):
        """Test launching and pinging the application."""
        app = DipsApp.DipsApp.LaunchApp(dips_base_port, dips_app_path) 
        app.Ping()
        app.Close()


class TestTraverseManagement:
    """Test cases for managing traverses in the Dips API."""
    
    def test_add_and_verify_traverse(self, dips_app_path, dips_base_port):
        """Test adding a traverse and verifying it was added."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port, dips_app_path)
        
        try:
            # Get the model
            model = app.GetModel()
            
            # Create a simple traverse
            traverse = self._create_sample_traverse()
            
            # Add the traverse (this will raise ValueError if there are errors)
            traverse_ref = model.AddTraverse(traverse)
            
            # Verify we got a reference back
            assert traverse_ref is not None
            
            # Get all traverses
            traverses = model.GetTraverses()
            
            # Verify the traverse was added
            assert len(traverses) > 0, "No traverses found after adding one"
            
            # Verify the traverse we added is in the list
            found = False
            for trav_ref in traverses:
                traverse_value = trav_ref.GetValue()
                if traverse_value.name == "Test Traverse":
                    found = True
                    break
            
            assert found, "The added traverse was not found in the traverses list"
            
        finally:
            # Close the application
            app.Close()
    
    def _create_sample_traverse(self):
        """Helper method to create a sample traverse for testing."""
        ods = OrientationDataSetVal.OrientationDataSetVal()
        ods.name = "Test Traverse"
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
            discontinuity = DiscontinuityDataVal.DiscontinuityDataVal()
            discontinuity.orientation1.angle_radians = math.radians(45 + i * 10)
            discontinuity.orientation2.angle_radians = math.radians(30 + i * 5)
            discontinuity.quantity = 1.0 + i * 0.1
            ods.discontinuity_list.append(discontinuity)
        
        return ods


if __name__ == "__main__":
    pytest.main([__file__])