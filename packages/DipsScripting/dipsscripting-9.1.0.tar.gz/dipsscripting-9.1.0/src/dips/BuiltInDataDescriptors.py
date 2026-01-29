from .DataDescriptorVal import DataDescriptorVal
from .DataIdentifierVal import DataIdentifierVal

# Orientation descriptors (Angle type = 8)
TrendDescriptor = DataDescriptorVal()
TrendDescriptor.data_type = 8  # eDataType.Angle
TrendDescriptor.data_name = DataIdentifierVal()
TrendDescriptor.data_name.data_name = "Trend"

PlungeDescriptor = DataDescriptorVal()
PlungeDescriptor.data_type = 8  # eDataType.Angle
PlungeDescriptor.data_name = DataIdentifierVal()
PlungeDescriptor.data_name.data_name = "Plunge"

DipDescriptor = DataDescriptorVal()
DipDescriptor.data_type = 8  # eDataType.Angle
DipDescriptor.data_name = DataIdentifierVal()
DipDescriptor.data_name.data_name = "Dip"

DipDirectionDescriptor = DataDescriptorVal()
DipDirectionDescriptor.data_type = 8  # eDataType.Angle
DipDirectionDescriptor.data_name = DataIdentifierVal()
DipDirectionDescriptor.data_name.data_name = "Dip Direction"

StrikeLeftDescriptor = DataDescriptorVal()
StrikeLeftDescriptor.data_type = 8  # eDataType.Angle
StrikeLeftDescriptor.data_name = DataIdentifierVal()
StrikeLeftDescriptor.data_name.data_name = "Strike (left)"

StrikeRightDescriptor = DataDescriptorVal()
StrikeRightDescriptor.data_type = 8  # eDataType.Angle
StrikeRightDescriptor.data_name = DataIdentifierVal()
StrikeRightDescriptor.data_name.data_name = "Strike (right)"

# Numeric descriptors (UnitlessNumeric type = 1)
QuantityDescriptor = DataDescriptorVal()
QuantityDescriptor.data_type = 1  # eDataType.UnitlessNumeric
QuantityDescriptor.data_name = DataIdentifierVal()
QuantityDescriptor.data_name.data_name = "Quantity"

TraverseDescriptor = DataDescriptorVal()
TraverseDescriptor.data_type = 1  # eDataType.UnitlessNumeric
TraverseDescriptor.data_name = DataIdentifierVal()
TraverseDescriptor.data_name.data_name = "Traverse"

WeightingDescriptor = DataDescriptorVal()
WeightingDescriptor.data_type = 1  # eDataType.UnitlessNumeric
WeightingDescriptor.data_name = DataIdentifierVal()
WeightingDescriptor.data_name.data_name = "Weighting"

# Length descriptors (Length type = 3)
DistanceDescriptor = DataDescriptorVal()
DistanceDescriptor.data_type = 3  # eDataType.Length
DistanceDescriptor.data_name = DataIdentifierVal()
DistanceDescriptor.data_name.data_name = "Distance"

XDescriptor = DataDescriptorVal()
XDescriptor.data_type = 3  # eDataType.Length
XDescriptor.data_name = DataIdentifierVal()
XDescriptor.data_name.data_name = "X"

YDescriptor = DataDescriptorVal()
YDescriptor.data_type = 3  # eDataType.Length
YDescriptor.data_name = DataIdentifierVal()
YDescriptor.data_name.data_name = "Y"

ElevationDescriptor = DataDescriptorVal()
ElevationDescriptor.data_type = 3  # eDataType.Length
ElevationDescriptor.data_name = DataIdentifierVal()
ElevationDescriptor.data_name.data_name = "Elevation"

PersistenceDescriptor = DataDescriptorVal()
PersistenceDescriptor.data_type = 3  # eDataType.Length
PersistenceDescriptor.data_name = DataIdentifierVal()
PersistenceDescriptor.data_name.data_name = "Persistence"

# Text descriptor (Text type = 0)
SetDescriptor = DataDescriptorVal()
SetDescriptor.data_type = 0  # eDataType.Text
SetDescriptor.data_name = DataIdentifierVal()
SetDescriptor.data_name.data_name = "Set"