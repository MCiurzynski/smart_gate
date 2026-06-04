from src.detector import LicensePlateValidator
import pytest

@pytest.mark.parametrize('license', [
    'XY12345',
    'XY1234A',
    'XY123AC',
    'XY1A234',
    'XY1AC23'
])
def test_valid_2_char(license):
    validator = LicensePlateValidator()
    assert validator._validate_plate(license)

@pytest.mark.parametrize('license', [
    'XYZA123',
    'XYZ12AC',
    'XYZ1A23',
    'XYZ12A3',
    'XYZ1AC2',
    'XYZAC12',
    'XYZ12345',
    'XYZ1234A',
    'XYZ123AC',
    'XYZA12C',
    'XYZA1CE'
])
def test_valid_3_char(license):
    validator = LicensePlateValidator()
    assert validator._validate_plate(license)

@pytest.mark.parametrize('license', [
    'X123',
    'X12A',
    'X1A2',
    'XA12',
    'X1AC',
    'XAC1',
    'XA1C'
])
def test_valid_1_char(license):
    validator = LicensePlateValidator()
    assert validator._validate_plate(license)

@pytest.mark.parametrize('license', [
    'XY123',
    'XY123456',
    '',
    'A',
    'XY',
    'XYZ',
    '1234567',
    '12345678',
    '1234',
    'ABCD',
    'ABCDE',
    'ABCDEF',
    'ABCDEFG'
])
def test_not_valid(license):
    validator = LicensePlateValidator()
    assert not validator._validate_plate(license)

@pytest.mark.parametrize('licenses, valid_licenses', [
    ({'XY12345', 'XY1234A', 'XY123AC'}, {'XY12345', 'XY1234A', 'XY123AC'}),
    ({'XY123', 'XY1234A', 'XY123AC'}, {'XY1234A', 'XY123AC'}),
    ({'XYZA123', 'XYZ12AC', 'XYZ1A23'}, {'XYZA123', 'XYZ12AC', 'XYZ1A23'}),
    ({'XYZA123', 'XYZ', 'XYZ1A23'}, {'XYZA123', 'XYZ1A23'}),
    ({'X123','X12A', 'X1A2ABCD'}, {'X123','X12A'}),
    ({'X123','X12A', 'X1A2'}, {'X123','X12A', 'X1A2'}),
    ({'XYZA1CE', 'XA1C', 'XY1AC23'}, {'XYZA1CE', 'XA1C', 'XY1AC23'})
])
def test_selecting_valid_licenses(licenses, valid_licenses):
    validator = LicensePlateValidator()
    validated = validator.validate_plates(licenses)
    assert validated == valid_licenses