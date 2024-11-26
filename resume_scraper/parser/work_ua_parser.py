from bs4 import BeautifulSoup
from typing import Dict, Optional

from resume_scraper.exceptions.Exceptions import ParserException

class ResumeParser:
    def parse_card(self, card: BeautifulSoup) -> Optional[Dict]:
        try:
            job_title_tag = card.find('h2', class_='mt-0')
            job_title = job_title_tag.text.strip()
            resume_link = f"https://www.work.ua{job_title_tag.find('a')['href']}"

            personal_info_tag = card.find('p', class_='mt-xs mb-0')
            name, age, location = None, None, None
            if personal_info_tag:
                personal_info = personal_info_tag.text.strip()
                parts = [part.strip() for part in personal_info.split(',')]
                if len(parts) == 3:
                    name, age, location = parts

            education_job_type_tag = card.find('p',
                                               class_='mb-0 mt-xs text-default-7')
            education_job_type = education_job_type_tag.text.strip() if education_job_type_tag else None

            salary_tag = card.find('p',
                                   class_='h5 strong-600 mt-xs mb-0 nowrap')
            salary = salary_tag.text.strip() if salary_tag else None

            experience_tag = card.find('ul', class_='mt-lg mb-0')
            work_experience = None
            if experience_tag:
                experience_item = experience_tag.find('li')
                work_experience = experience_item.text.strip() if experience_item else None

            posted_time_tag = card.find('time', class_='text-default-7 mt-lg')
            posted_time = posted_time_tag.text.strip() if posted_time_tag else None

            return {
                "job_title": job_title,
                "resume_link": resume_link,
                "name": name,
                "age": age,
                "location": location,
                "education_job_type": education_job_type,
                "salary": salary,
                "work_experience": work_experience,
                "posted_time": posted_time,
            }
        except Exception as e:
            raise ParserException(f"Error parsing card: {e}")

    def parse_page(self, html_content: str) -> list:
        soup = BeautifulSoup(html_content, 'html.parser')
        cards = soup.find_all('div',
                              class_='card card-hover card-search resume-link card-visited wordwrap')
        return [self.parse_card(card) for card in cards if
                self.parse_card(card)]
