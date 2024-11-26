import re
from datetime import datetime
from typing import List


class CandidateScorer:

    def __init__(self, keywords: List[str], budget: int = None,
                 weights: dict = None):
        self.keywords = [kw.lower() for kw in keywords]
        self.budget = budget
        self.weights = weights or {
            "completeness": 0.3,
            "experience": 0.3,
            "recency": 0.2,
            "keywords": 0.2,
        }

    def calculate_completeness_score(self, resume: dict) -> float:
        fields = ["name", "age", "location", "education_job_type", "salary",
                  "work_experience"]
        filled_fields = sum(
            1 for field in fields if resume.get(field) is not None)
        return filled_fields / len(fields)

    def calculate_experience_score(self, resume: dict) -> float:
        work_experience = resume.get("work_experience")
        if not work_experience:
            return 0  # No experience mentioned

        match = re.search(r"(\d+)\s*(?:рік|років|роки)", work_experience)
        if match:
            years = int(match.group(1))
            months = 0

            # Extract months if present
            month_match = re.search(r"(\d+)\s*(?:місяць|місяці|місяців)",
                                    work_experience)
            if month_match:
                months = int(month_match.group(1))

            total_years = years + (months / 12)
            return min(total_years / 10, 1)

        return 0

    def calculate_recency_score(self, resume: dict) -> float:
        posted_time = resume.get("posted_time")
        try:
            posted_datetime = datetime.fromisoformat(posted_time)
            days_since_posted = (datetime.now() - posted_datetime).days
            if days_since_posted < 1:
                return 1.0  # Same day
            elif days_since_posted < 7:
                return 0.8  # Within a week
            elif days_since_posted < 30:
                return 0.5  # Within a month
            else:
                return 0.2  # Older resumes
        except Exception:
            return 0

    def calculate_keyword_score(self, resume: dict) -> float:
        job_title = resume.get("job_title", "") or ""
        work_experience = resume.get("work_experience", "") or ""
        combined_text = f"{job_title.lower()} {work_experience.lower()}"
        matches = sum(
            1 for keyword in self.keywords if keyword in combined_text)
        return matches / len(self.keywords) if self.keywords else 0

    def score_resume(self, resume: dict) -> float:
        completeness = self.calculate_completeness_score(resume)
        experience = self.calculate_experience_score(resume)
        recency = self.calculate_recency_score(resume)
        keywords = self.calculate_keyword_score(resume)

        total_score = (
                completeness * self.weights["completeness"]
                + experience * self.weights["experience"]
                + recency * self.weights["recency"]
                + keywords * self.weights["keywords"]
        )
        return total_score

    def sort_candidates(self, resumes: List[dict]) -> List[dict]:
        return sorted(resumes, key=self.score_resume, reverse=True)
