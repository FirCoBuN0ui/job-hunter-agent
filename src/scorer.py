from .models import Job


def score_job(job: Job, keywords: list[str]) -> int:
    text = f"{job.title} {job.description}".lower()
    score = 0

    for kw in keywords:
        kw = kw.strip().lower()
        if kw and kw in text:
            score += 20

    if "remote" in text or "远程" in text:
        score += 10

    if "python" in text:
        score += 15

    return min(score, 100)