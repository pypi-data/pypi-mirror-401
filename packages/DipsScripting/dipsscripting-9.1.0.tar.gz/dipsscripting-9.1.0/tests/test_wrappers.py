"""
Unit tests for the Dips Python API wrapper classes.
These tests verify that the wrapper classes function correctly without requiring
a running Dips application.
"""

import pytest
import math
from dips import DipsAPI_pb2
from dips.AngleDataVal import AngleDataVal
from dips.ColorSurrogateVal import ColorSurrogateVal
from dips.TrendPlungeVal import TrendPlungeVal
from dips.SetEntityInfoVal import SetEntityInfoVal
from dips.SetWindowEntityInfoVal import SetWindowEntityInfoVal
from dips.SetStatisticsSettingsVal import SetStatisticsSettingsVal
from dips.CircularWindowVal import CircularWindowVal


class TestAngleDataVal:
    """Test cases for AngleDataVal."""
    
    def test_angle_radians_setter_getter(self):
        """Test setting and getting angle in radians."""
        angle = AngleDataVal()
        angle.angle_radians = math.pi / 4
        
        assert angle.angle_radians == math.pi / 4
    
    def test_angle_conversion_degrees_radians(self):
        """Test converting between degrees and radians."""
        angle = AngleDataVal()
        angle.angle_radians = math.radians(45)
        
        assert abs(angle.angle_radians - math.pi / 4) < 1e-10
    
    def test_to_proto(self):
        """Test converting to protobuf."""
        angle = AngleDataVal()
        angle.angle_radians = 1.5
        
        proto = angle.to_proto()
        assert proto.AngleRadians == 1.5


class TestColorSurrogateVal:
    """Test cases for ColorSurrogateVal."""
    
    def test_rgb_colors(self):
        """Test setting RGB color values."""
        color = ColorSurrogateVal()
        color.r = 255
        color.g = 128
        color.b = 64
        color.a = 255
        
        assert color.r == 255
        assert color.g == 128
        assert color.b == 64
        assert color.a == 255
    
    def test_alpha_transparency(self):
        """Test alpha transparency setting."""
        color = ColorSurrogateVal()
        color.a = 128  # 50% transparency
        
        assert color.a == 128


class TestTrendPlungeVal:
    """Test cases for TrendPlungeVal."""
    
    def test_trend_plunge_creation(self):
        """Test creating trend and plunge values."""
        tp = TrendPlungeVal()
        tp.trend.angle_radians = math.radians(45)
        tp.plunge.angle_radians = math.radians(30)
        
        assert abs(tp.trend.angle_radians - math.pi / 4) < 1e-10
        assert abs(tp.plunge.angle_radians - math.pi / 6) < 1e-10
    
    def test_to_proto(self):
        """Test converting to protobuf."""
        tp = TrendPlungeVal()
        tp.trend.angle_radians = 1.0
        tp.plunge.angle_radians = 0.5
        
        proto = tp.to_proto()
        assert proto.Trend.AngleRadians == 1.0
        assert proto.Plunge.AngleRadians == 0.5


class TestSetStatisticsSettingsVal:
    """Test cases for SetStatisticsSettingsVal."""
    
    def test_std_dev_flags(self):
        """Test standard deviation flags."""
        stats = SetStatisticsSettingsVal()
        stats.one_std_dev = True
        stats.two_std_dev = True
        stats.three_std_dev = False
        
        assert stats.one_std_dev == True
        assert stats.two_std_dev == True
        assert stats.three_std_dev == False
    
    def test_custom_interval(self):
        """Test custom interval settings."""
        stats = SetStatisticsSettingsVal()
        stats.use_custom_interval = True
        stats.custom_interval = 15.5
        
        assert stats.use_custom_interval == True
        assert stats.custom_interval == 15.5


class TestSetEntityInfoVal:
    """Test cases for SetEntityInfoVal."""
    
    def test_set_id_and_color(self):
        """Test setting set ID and color."""
        set_info = SetEntityInfoVal()
        set_info.id = "TestSet1"
        
        color = ColorSurrogateVal()
        color.r = 255
        color.g = 0
        color.b = 0
        color.a = 255
        set_info.color = color
        
        assert set_info.id == "TestSet1"
        assert set_info.color.r == 255
    
    def test_set_window_type(self):
        """Test setting window type for different set types."""
        set_info = SetEntityInfoVal()
        
        # Test circular set window
        window_info = SetWindowEntityInfoVal()
        window_info.set_window_type = DipsAPI_pb2.eSetWindowType.Circular
        set_info.set_window_entity_info = window_info
        
        assert set_info.set_window_entity_info.set_window_type == DipsAPI_pb2.eSetWindowType.Circular
    
    def test_circular_window_setup(self):
        """Test setting up a circular window."""
        set_info = SetEntityInfoVal()
        set_info.id = "CircularSet1"
        
        window_info = SetWindowEntityInfoVal()
        window_info.set_window_type = DipsAPI_pb2.eSetWindowType.Circular
        
        circular_window = CircularWindowVal()
        circular_window.id = "CircularSet1"
        
        center = TrendPlungeVal()
        center.trend.angle_radians = math.radians(90)
        center.plunge.angle_radians = math.radians(45)
        circular_window.center = center
        
        cone_angle = AngleDataVal()
        cone_angle.angle_radians = math.radians(20)
        circular_window.cone_angle = cone_angle
        
        window_info.circular_set_window = circular_window
        set_info.set_window_entity_info = window_info
        
        assert set_info.id == "CircularSet1"
        assert set_info.set_window_entity_info.circular_set_window.center.trend.angle_radians == math.radians(90)


if __name__ == "__main__":
    pytest.main([__file__])






