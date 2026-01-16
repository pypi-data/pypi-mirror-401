import pytest
import casased


def test_list_assets():
    assets = casased.notation()
    assert isinstance(assets, list)
    assert 'Addoha' in assets
    assert 'BCP' in assets
    assert 'MASI' in assets
    assert 'MSI20' in assets


def test_get_isin_by_name():
    isin = casased.get_isin_by_name('Addoha')
    assert isin.startswith('MA')
    assert isin == 'MA0000011512'
    with pytest.raises(KeyError):
        casased.get_isin_by_name('UNKNOWN_ASSET')


def test_get_isin_by_name_case_insensitive():
    # Test case insensitivity
    assert casased.get_isin_by_name('BCP') == casased.get_isin_by_name('bcp')
    assert casased.get_isin_by_name('Addoha') == casased.get_isin_by_name('ADDOHA')


def test_notation_code():
    codes = casased.notation_code()
    assert isinstance(codes, list)
    assert len(codes) > 0
    # Check structure
    for entry in codes:
        assert 'name' in entry
        assert 'ISIN' in entry


def test_notation_value():
    values = casased.notation_value()
    assert isinstance(values, dict)
    assert 'BCP' in values
    assert 'Addoha' in values


def test_aliases_in_notation_code():
    """Test that common aliases are included in notation_code."""
    codes = casased.notation_code()
    names = [c['name'] for c in codes]
    
    # Test common aliases
    assert 'CFG' in names, "CFG alias for CFG Bank should be in notation_code"
    assert 'CMG' in names, "CMG alias for CMGP Group should be in notation_code"
    assert 'IAM' in names, "IAM alias for Maroc Telecom should be in notation_code"
    assert 'MDP' in names, "MDP alias for Med Paper should be in notation_code"
    assert 'SAM' in names, "SAM alias for Sanlam Maroc should be in notation_code"


def test_aliases_in_notation_value():
    """Test that common aliases are included in notation_value."""
    values = casased.notation_value()
    
    # Test common aliases
    assert 'CFG' in values, "CFG alias should be in notation_value"
    assert 'CMG' in values, "CMG alias should be in notation_value"
    assert 'IAM' in values, "IAM alias should be in notation_value"
    assert 'MDP' in values, "MDP alias should be in notation_value"
    assert 'SAM' in values, "SAM alias should be in notation_value"
    
    # Test that aliases map to same values as full names
    assert values['CFG'] == values['CFG Bank']
    assert values['CMG'] == values['CMGP Group']
    assert values['IAM'] == values['Maroc Telecom']
    assert values['MDP'] == values['Med Paper']
    assert values['SAM'] == values['Sanlam Maroc']


def test_get_isin_by_alias():
    """Test that ISIN lookup works with aliases."""
    # Test aliases resolve to correct ISINs
    assert casased.get_isin_by_name('CFG') == casased.get_isin_by_name('CFG Bank')
    assert casased.get_isin_by_name('CMG') == casased.get_isin_by_name('CMGP Group')
    assert casased.get_isin_by_name('IAM') == casased.get_isin_by_name('Maroc Telecom')
    assert casased.get_isin_by_name('MDP') == casased.get_isin_by_name('Med Paper')
    assert casased.get_isin_by_name('SAM') == casased.get_isin_by_name('Sanlam Maroc')
