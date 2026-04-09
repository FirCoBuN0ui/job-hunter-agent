from src.adapters import load_jobs_by_source


def test_load_boss_adapter():
    jobs = load_jobs_by_source("boss", "data/boss_mock.json")
    assert len(jobs) == 2
    assert jobs[0].title == "Python Backend Engineer"
    assert jobs[0].company == "A Tech"


def test_load_lagou_adapter():
    jobs = load_jobs_by_source("lagou", "data/lagou_mock.json")
    assert len(jobs) == 2
    assert jobs[0].title == "Data Engineer"
    assert jobs[0].city == "Beijing"