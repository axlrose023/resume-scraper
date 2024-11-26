from resume_scraper.services.resume_service import ResumeService
from resume_scraper.scraper.work_ua_scraper import WorkUaScraper
from resume_scraper.parser.work_ua_parser import ResumeParser
from resume_scraper.scorer.scorer import CandidateScorer

if __name__ == "__main__":
    scraper = WorkUaScraper()
    parser = ResumeParser()
    scorer = CandidateScorer(keywords=["python", "django", "machine learning"],
                             budget=120000)
    service = ResumeService(scraper, parser, scorer)

    endpoint = "/resumes-python-junior/"
    try:
        resumes = service.fetch_and_process_resumes(endpoint)
        for resume in resumes:
            print(resume)
    except Exception as e:
        print(f"Error: {e}")
