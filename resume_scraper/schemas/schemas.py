from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime, timedelta
import re


class Resume(BaseModel):
    job_title: str
    resume_link: str
    name: Optional[str]
    age: Optional[int]
    location: Optional[str]
    education_job_type: Optional[str]
    salary: Optional[int]
    work_experience: Optional[str]
    posted_time: str

    # Normalizing age to an integer
    @field_validator("age", mode="before")
    def normalize_age(cls, value):
        if value:
            match = re.search(r"\d+", value)
            return int(match.group()) if match else None
        return None

    # Normalizing salary to an integer
    @field_validator("salary", mode="before")
    def normalize_salary(cls, value):
        if value:
            numeric_value = re.sub(r"[^\d]", "", value)
            return int(numeric_value) if numeric_value else None
        return None

    # Clean work experience to remove non-breaking spaces
    @field_validator("work_experience", mode="before")
    def clean_work_experience(cls, value):
        if value:
            return value.replace("\xa0", " ")
        return value

    # Convert posted time to ISO format
    @field_validator("posted_time", mode="before")
    def normalize_posted_time(cls, value):
        now = datetime.now()
        if value == "вчора":
            return (now - timedelta(days=1)).isoformat()
        elif "хвилин" in value or "годин" in value:
            match = re.search(r"(\d+)", value)
            if match:
                number = int(match.group())
                delta = timedelta(minutes=number) if "хвилин" in value else timedelta(hours=number)
                return (now - delta).isoformat()
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            return datetime.strptime(value, "%Y-%m-%d").isoformat()
        return value

    # Convert HttpUrl to string
    @field_validator("resume_link", mode="before")
    def convert_httpurl_to_string(cls, value):
        return str(value)