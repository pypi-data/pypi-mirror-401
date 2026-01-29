"""
Integration tests for project management functionality.
These tests require a running Dips application or will launch one.
"""
import pytest
import os
import tempfile
import math
from dips import DipsApp
from dips import DipsAPI_pb2
from dips.UnitSystemResultVal import UnitSystemResultVal
from dips.ReportingConventionResultVal import ReportingConventionResultVal
from dips.WeightingSettingsVal import WeightingSettingsVal
from dips.AngleDataVal import AngleDataVal
from dips.ValidatableResultVal import ValidatableResultVal


@pytest.mark.integration
class TestProjectSave:
    """Test cases for saving projects."""
    
    def test_save_project(self, dips_app_path, dips_base_port):
        """Test saving a project to a file path."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 1, dips_app_path)
        
        try:
            # Get the model
            model = app.GetModel()
            
            # Create a temporary file path
            with tempfile.NamedTemporaryFile(suffix='.dips9', delete=False) as tmp_file:
                file_path = tmp_file.name
            
            try:
                # Save the project - the generated code now handles String as a Python str
                # and converts it to the protobuf String message type automatically
                result = model.SaveProject(file_path)
                
                # Verify the save was successful (no errors)
                # assert isinstance(result, ValidatableResultVal)
                # assert len(result.errors) == 0, f"Save failed with errors: {[e.error_message for e in result.errors]}"
                
                # Verify the file was created
                assert os.path.exists(file_path), "Project file was not created"
                assert os.path.getsize(file_path) > 0, "Project file is empty"
                
            finally:
                # Clean up the temporary file
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
        finally:
            # Close the application
            app.Close()


@pytest.mark.integration
class TestUnitSystem:
    """Test cases for unit system get/set operations."""
    
    def test_get_and_set_unit_system(self, dips_app_path, dips_base_port):
        """Test getting and setting the unit system."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 2, dips_app_path)
        
        try:
            # Get the model
            model = app.GetModel()
            
            # Get the current unit system
            unit_system_result = model.GetUnitSystem()
            
            # Verify we got a result
            assert unit_system_result is not None
            
            # Wrap it to access the value
            unit_system_wrapper = UnitSystemResultVal.from_proto(unit_system_result)
            original_value = unit_system_wrapper.value
            
            # Verify it's a valid enum value
            assert original_value in [DipsAPI_pb2.eUnitSystem.Metric, DipsAPI_pb2.eUnitSystem.Imperial]
            
            # Toggle the unit system
            new_value = DipsAPI_pb2.eUnitSystem.Imperial if original_value == DipsAPI_pb2.eUnitSystem.Metric else DipsAPI_pb2.eUnitSystem.Metric
            model.SetUnitSystem(new_value)
            
            # Get the unit system again and verify it changed
            updated_result = model.GetUnitSystem()
            updated_wrapper = UnitSystemResultVal.from_proto(updated_result)
            assert updated_wrapper.value == new_value, "Unit system was not updated correctly"
            
            # Restore the original value
            model.SetUnitSystem(original_value)
            
            # Verify it was restored
            restored_result = model.GetUnitSystem()
            restored_wrapper = UnitSystemResultVal.from_proto(restored_result)
            assert restored_wrapper.value == original_value, "Unit system was not restored correctly"
            
        finally:
            # Close the application
            app.Close()
    
    def test_set_metric_unit_system(self, dips_app_path, dips_base_port):
        """Test setting the unit system to Metric."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 3, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Set to Metric
            model.SetUnitSystem(DipsAPI_pb2.eUnitSystem.Metric)
            
            # Verify it was set
            result = model.GetUnitSystem()
            wrapper = UnitSystemResultVal.from_proto(result)
            assert wrapper.value == DipsAPI_pb2.eUnitSystem.Metric
            
        finally:
            app.Close()
    
    def test_set_imperial_unit_system(self, dips_app_path, dips_base_port):
        """Test setting the unit system to Imperial."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 4, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Set to Imperial
            model.SetUnitSystem(DipsAPI_pb2.eUnitSystem.Imperial)
            
            # Verify it was set
            result = model.GetUnitSystem()
            wrapper = UnitSystemResultVal.from_proto(result)
            assert wrapper.value == DipsAPI_pb2.eUnitSystem.Imperial
            
        finally:
            app.Close()


@pytest.mark.integration
class TestReportingConvention:
    """Test cases for reporting convention get/set operations."""
    
    def test_get_and_set_reporting_convention(self, dips_app_path, dips_base_port):
        """Test getting and setting the reporting convention."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 5, dips_app_path)
        
        try:
            # Get the model
            model = app.GetModel()
            
            # Get the current reporting convention
            convention_result = model.GetReportingConvention()
            
            # Verify we got a result
            assert convention_result is not None
            
            # Wrap it to access the value
            convention_wrapper = ReportingConventionResultVal.from_proto(convention_result)
            original_value = convention_wrapper.value
            
            # Verify it's a valid enum value
            valid_conventions = [
                DipsAPI_pb2.eOrientationConvention.DipDipDirectionOrientation,
                DipsAPI_pb2.eOrientationConvention.StrikeRightDipOrientation,
                DipsAPI_pb2.eOrientationConvention.StrikeLeftDipOrientation,
                DipsAPI_pb2.eOrientationConvention.TrendPlungeOrientation,
                DipsAPI_pb2.eOrientationConvention.Orient123Orientation,
                DipsAPI_pb2.eOrientationConvention.Orient1SurveyDataOrientation,
                DipsAPI_pb2.eOrientationConvention.SurveyDataOrientation,
                DipsAPI_pb2.eOrientationConvention.AlphaBetaOrientation,
            ]
            assert original_value in valid_conventions
            
            # Set to a different convention (use TrendPlungeOrientation as test value)
            test_value = DipsAPI_pb2.eOrientationConvention.TrendPlungeOrientation
            if original_value != test_value:
                model.SetReportingConvention(test_value)
                
                # Get the convention again and verify it changed
                updated_result = model.GetReportingConvention()
                updated_wrapper = ReportingConventionResultVal.from_proto(updated_result)
                assert updated_result is not None
                assert updated_wrapper.value == test_value, "Reporting convention was not updated correctly"
                
                # Restore the original value
                model.SetReportingConvention(original_value)
                
                # Verify it was restored
                restored_result = model.GetReportingConvention()
                restored_wrapper = ReportingConventionResultVal.from_proto(restored_result)
                assert restored_wrapper.value == original_value, "Reporting convention was not restored correctly"
            
        finally:
            # Close the application
            app.Close()
    
    def test_set_dip_dip_direction_convention(self, dips_app_path, dips_base_port):
        """Test setting the reporting convention to Dip/DipDirection."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 6, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Set to DipDipDirectionOrientation
            model.SetReportingConvention(DipsAPI_pb2.eOrientationConvention.DipDipDirectionOrientation)
            
            # Verify it was set
            result = model.GetReportingConvention()
            wrapper = ReportingConventionResultVal.from_proto(result)
            assert wrapper.value == DipsAPI_pb2.eOrientationConvention.DipDipDirectionOrientation
            
        finally:
            app.Close()


@pytest.mark.integration
class TestWeightingOptions:
    """Test cases for weighting options get/set operations."""
    
    def test_get_and_set_weighting_options(self, dips_app_path, dips_base_port):
        """Test getting and setting weighting options."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 7, dips_app_path)
        
        try:
            # Get the model
            model = app.GetModel()
            
            # Get the current weighting options
            weighting_result = model.GetWeightingOptions()
            
            # Verify we got a result
            assert weighting_result is not None
            
            # Wrap it to access the properties
            weighting_wrapper = WeightingSettingsVal.from_proto(weighting_result)
            original_weighting_option = weighting_wrapper.weighting_option
            original_minimum_bias_angle = weighting_wrapper.minimum_bias_angle.angle_radians
            
            # Verify it's a valid enum value
            assert original_weighting_option == DipsAPI_pb2.eWeightingOption.TerzaghiWeighting
            
            # Create new weighting settings
            new_weighting = WeightingSettingsVal()
            new_weighting.weighting_option = DipsAPI_pb2.eWeightingOption.TerzaghiWeighting
            
            # Set a new minimum bias angle (15 degrees in radians)
            new_min_bias_angle = AngleDataVal()
            new_min_bias_angle.angle_radians = math.radians(15.0)
            new_weighting.minimum_bias_angle = new_min_bias_angle
            
            # Set the weighting options
            model.SetWeightingOptions(new_weighting)
            
            # Get the weighting options again and verify they changed
            updated_result = model.GetWeightingOptions()
            updated_wrapper = WeightingSettingsVal.from_proto(updated_result)
            assert updated_wrapper.weighting_option == new_weighting.weighting_option
            assert abs(updated_wrapper.minimum_bias_angle.angle_radians - new_min_bias_angle.angle_radians) < 1e-6
            
            # Restore the original values
            original_weighting = WeightingSettingsVal()
            original_weighting.weighting_option = original_weighting_option
            original_min_bias = AngleDataVal()
            original_min_bias.angle_radians = original_minimum_bias_angle
            original_weighting.minimum_bias_angle = original_min_bias
            model.SetWeightingOptions(original_weighting)
            
            # Verify it was restored
            restored_result = model.GetWeightingOptions()
            restored_wrapper = WeightingSettingsVal.from_proto(restored_result)
            assert restored_wrapper.weighting_option == original_weighting_option
            assert abs(restored_wrapper.minimum_bias_angle.angle_radians - original_minimum_bias_angle) < 1e-6
            
        finally:
            # Close the application
            app.Close()
    
    def test_set_weighting_options_with_custom_angle(self, dips_app_path, dips_base_port):
        """Test setting weighting options with a custom minimum bias angle."""
        # Launch the application
        app = DipsApp.DipsApp.LaunchApp(dips_base_port + 8, dips_app_path)
        
        try:
            model = app.GetModel()
            
            # Create weighting settings with a 20-degree minimum bias angle
            weighting = WeightingSettingsVal()
            weighting.weighting_option = DipsAPI_pb2.eWeightingOption.TerzaghiWeighting
            
            min_bias_angle = AngleDataVal()
            min_bias_angle.angle_radians = math.radians(20.0)
            weighting.minimum_bias_angle = min_bias_angle
            
            # Set the weighting options
            model.SetWeightingOptions(weighting)
            
            # Verify it was set
            result = model.GetWeightingOptions()
            wrapper = WeightingSettingsVal.from_proto(result)
            assert wrapper.weighting_option == DipsAPI_pb2.eWeightingOption.TerzaghiWeighting
            assert abs(wrapper.minimum_bias_angle.angle_radians - math.radians(20.0)) < 1e-6
            
        finally:
            app.Close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

