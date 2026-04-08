from dataclasses import dataclass


@dataclass
class Job:
    title: str
    company: str
    city: str
    salary: str
    description: str
    url: str