
# **Resume Scraper with Telegram Bot Interface**

This project is designed to streamline the process of finding relevant resumes from job websites (currently, `work.ua`). It integrates a **resume scraping system** with a **Telegram bot interface**, enabling HR personnel to quickly search, filter, and retrieve the most suitable resumes based on defined criteria.

---

## **What Has Been Implemented**

### 1. **Resume Scraping**
- A **scraper** was built to fetch resumes from `work.ua` using HTTP requests.
- A **parser** extracts relevant fields from the HTML (e.g., job title, experience, location, salary).
- The scraper retries on failures and gracefully handles network issues.

### 2. **Data Validation**
- Scraped data is validated using **Pydantic schemas**.
- Fields like age, salary, and posted time are normalized and cleaned.
- Invalid or incomplete resumes are skipped during processing, ensuring only high-quality data is passed through.

### 3. **Resume Scoring and Ranking**
- A **Candidate Scorer** module ranks resumes based on:
  - **Completeness**: How many fields are filled.
  - **Experience**: Duration of work experience extracted from the resume.
  - **Recency**: How recently the resume was posted.
  - **Keyword Relevance**: Match between user-specified keywords and the resume content.
- Resumes are scored and sorted to prioritize the most relevant candidates.

### 4. **Telegram Bot Interface**
- A Telegram bot enables HR personnel to:
  - Select job categories (e.g., `Python Junior`, `Python Developer`) using inline buttons or manual input.
  - Enter filtering criteria like keywords (e.g., `Python`, `Django`) and budget.
  - Retrieve and display the top 5 resumes based on the scoring system directly in Telegram.

---

## **Logic Flow**

### **Backend Components**
1. **Scraper**:
   - Fetches HTML data from `work.ua`.
   - Implements retries and handles network errors.

2. **Parser**:
   - Extracts structured data (e.g., job title, experience, salary) from the scraped HTML.
   - Handles invalid or unexpected HTML gracefully.

3. **Validator (Pydantic)**:
   - Ensures that extracted data conforms to expected formats.
   - Normalizes fields (e.g., converts salary to integers, posted time to ISO format).

4. **Scorer**:
   - Scores resumes based on predefined weights and user-defined criteria (keywords, budget).

5. **Resume Service**:
   - Coordinates scraping, parsing, validation, and scoring.
   - Returns a sorted list of resumes ready for display.

---

### **Telegram Bot Workflow**
1. **User Interaction**:
   - The user interacts with the bot via commands and buttons.
   - Options include selecting predefined job categories or entering a category manually.
2. **Data Input**:
   - The user provides filtering criteria (keywords, budget) via text messages.
3. **Resume Retrieval**:
   - The bot fetches, processes, and scores resumes using the backend service.
4. **Results Display**:
   - The top 5 resumes are displayed in Telegram with links to view the full profiles.

---

## **High-Level Workflow**
1. **Scraping**: Fetch resumes from `work.ua`.
2. **Parsing**: Extract structured data from HTML.
3. **Validation**: Clean and normalize data using schemas.
4. **Scoring**: Rank resumes based on relevance and completeness.
5. **Telegram Bot**:
   - Receive user input.
   - Display sorted results.

---

This system ensures a robust and user-friendly way to automate resume filtering and retrieval, tailored for HR needs.
