import pytest
from src.adapters import supported_sources, load_jobs_by_source


def test_supported_sources_contains_expected():
    s = supported_sources()
    assert "local" in s
    assert "boss" in s
    assert "lagou" in s


def test_unsupported_source_raises():
    with pytest.raises(ValueError) as e:
        load_jobs_by_source("unknown", "data/jobs_mock.csv")
    assert "Unsupported source" in str(e.value)