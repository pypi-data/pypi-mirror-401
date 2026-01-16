import pytest
import warnings
import casased


def test_getPond():
    """Test getPond returns dictionary with expected keys."""
    result = casased.getPond()
    assert isinstance(result, dict)
    # getPond should return weight data with these keys
    expected_keys = ['Code Isin', 'Instrument', 'Nombre de titres', 'Cours', 
                     'Facteur flottant', 'Facteur plafonnement', 
                     'Capitalisation flottante', 'Poids']
    for key in expected_keys:
        assert key in result, f"Expected key '{key}' in getPond result"


def test_deprecated_getCours():
    """Test that getCours shows deprecation warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = casased.getCours('BCP')
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert 'temporarily unavailable' in str(w[0].message).lower()
        assert result == {}


def test_deprecated_getKeyIndicators():
    """Test that getKeyIndicators shows deprecation warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = casased.getKeyIndicators('BCP')
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert result == {}


def test_deprecated_getDividend():
    """Test that getDividend shows deprecation warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = casased.getDividend('BCP')
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert result == {}


def test_deprecated_getIndex():
    """Test that getIndex shows deprecation warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = casased.getIndex()
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert result == {}


def test_deprecated_getIndexRecap():
    """Test that getIndexRecap shows deprecation warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = casased.getIndexRecap()
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert result == {}
