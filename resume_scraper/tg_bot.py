from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command

from resume_scraper.services.resume_service import ResumeService
from resume_scraper.scraper.work_ua_scraper import WorkUaScraper
from resume_scraper.parser.work_ua_parser import ResumeParser
from resume_scraper.scorer.scorer import CandidateScorer

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user_state = {}


async def fetch_top_resumes(keywords, budget, endpoint):
    scraper = WorkUaScraper()
    parser = ResumeParser()
    scorer = CandidateScorer(keywords=keywords, budget=budget)
    service = ResumeService(scraper, parser, scorer)
    try:
        resumes = service.fetch_and_process_resumes(endpoint)
        return resumes[:5]
    except Exception as e:
        print(f"Помилка під час отримання резюме: {e}")
        return None


@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    user_state[message.from_user.id] = {}
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Python Junior", callback_data="endpoint:/resumes-python-junior/"),
        InlineKeyboardButton("Python Developer", callback_data="endpoint:/resumes-python/"),
        InlineKeyboardButton("QA Engineer", callback_data="endpoint:/resumes-qa/"),
    )
    await message.reply(
        "Оберіть категорію вакансій за допомогою кнопок нижче або введіть її вручну (наприклад, Python Senior):",
        reply_markup=keyboard,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("endpoint:"))
async def set_endpoint_callback(callback_query: types.CallbackQuery):
    endpoint = callback_query.data.split(":")[1]
    user_state[callback_query.from_user.id]["endpoint"] = endpoint
    await callback_query.answer(f"Обрано категорію: {endpoint}")
    await bot.send_message(callback_query.from_user.id, "Введіть ключові слова для пошуку (наприклад, Python, Django):")


@dp.message_handler(lambda msg: "endpoint" not in user_state.get(msg.from_user.id, {}))
async def set_endpoint_manual(message: types.Message):
    user_input = message.text.strip()
    endpoint = f"/resumes-{user_input.replace(' ', '-').lower()}/"
    user_state[message.from_user.id]["endpoint"] = endpoint
    await message.reply(f"Обрано категорію: {user_input}. Введіть ключові слова для пошуку (наприклад, Python, Django):")


@dp.message_handler(lambda msg: msg.from_user.id in user_state and "keywords" not in user_state[msg.from_user.id])
async def capture_keywords(message: types.Message):
    keywords = message.text.split(",")
    user_state[message.from_user.id]["keywords"] = keywords
    await message.reply("Ключові слова збережено. Тепер введіть ваш бюджет (наприклад, 100000):")


@dp.message_handler(lambda msg: msg.from_user.id in user_state and "budget" not in user_state[msg.from_user.id])
async def capture_budget(message: types.Message):
    try:
        budget = int(message.text)
        user_state[message.from_user.id]["budget"] = budget
        await message.reply("Бюджет збережено! Натисніть /find, щоб розпочати пошук.")
    except ValueError:
        await message.reply("Будь ласка, введіть коректний числовий бюджет.")


@dp.message_handler(Command("find"))
async def find_resumes(message: types.Message):
    user_data = user_state.get(message.from_user.id, {})
    if not all(k in user_data for k in ("endpoint", "keywords", "budget")):
        await message.reply("Будь ласка, задайте всі критерії пошуку за допомогою /start.")
        return

    endpoint = user_data["endpoint"]
    keywords = user_data["keywords"]
    budget = user_data["budget"]

    await message.reply("Шукаю резюме... Зачекайте!")

    resumes = await fetch_top_resumes(keywords, budget, endpoint)
    if not resumes:
        await message.reply("Резюме не знайдено або сталася помилка під час пошуку.")
        return

    for resume in resumes:
        resume_text = (
            f"<b>{resume['job_title']}</b>\n"
            f"🔗 <a href='{resume['resume_link']}'>Переглянути резюме</a>\n"
            f"📍 Місцезнаходження: {resume.get('location', 'Не вказано')}\n"
            f"📅 Дата публікації: {resume['posted_time']}\n"
            f"💼 Досвід: {resume.get('work_experience', 'Не вказано')}\n"
            f"💰 Зарплата: {resume.get('salary', 'Не вказано')}\n"
        )
        await message.reply(resume_text, parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)