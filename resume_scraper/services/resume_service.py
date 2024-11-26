from typing import List
from pydantic import ValidationError

from resume_scraper.schemas.schemas import Resume


class ResumeService:
    def __init__(self, scraper, parser, scorer):
        self.scraper = scraper
        self.parser = parser
        self.scorer = scorer

    def fetch_and_process_resumes(self, endpoint: str) -> List[dict]:
        html_content = self.scraper.fetch_page(endpoint)
        raw_resumes = self.parser.parse_page(html_content)
        validated_resumes = []
        for raw_resume in raw_resumes:
            try:
                validated_resumes.append(Resume(**raw_resume))
            except ValidationError as e:
                print(f"Validation error: {e}")
        return self.scorer.sort_candidates([r.model_dump() for r in validated_resumes])