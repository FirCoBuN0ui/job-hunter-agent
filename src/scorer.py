import re
from .models import Job


def _extract_salary_high_k(salary: str) -> int | None:
    """
    从薪资字符串中提取区间上限（单位 k）
    支持示例: 20k-45k, 20K-32K, 15-30k
    无法解析返回 None
    """
    if not salary:
        return None

    s = salary.lower().replace(" ", "")
    # 取所有数字，通常区间会有两个数字
    nums = re.findall(r"\d+", s)
    if not nums:
        return None

    # 取最大值作为上限，兼容 "20k-45k" / "15-30k" / "30k以上"
    high = max(int(n) for n in nums)
    return high


def score_job(job: Job, keywords: list[str]) -> int:
    text = f"{job.title} {job.description}".lower()
    score = 0

    # 关键词命中
    for kw in keywords:
        if kw.lower() in text:
            score += 20

    # remote/远程加分（v1先保留子串匹配）
    if "remote" in text or "远程" in text:
        score += 10

    # python加分
    if "python" in text:
        score += 15

    # 薪资加分（新增）
    high_k = _extract_salary_high_k(job.salary)
    if high_k is not None:
        if high_k >= 40:
            score += 10
        elif high_k >= 30:
            score += 5

    return min(score, 100)