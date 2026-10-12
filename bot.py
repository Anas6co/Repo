import html
import logging
import math
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

from fonts import STYLES

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

PER_PAGE = 10
MAX_LEN = 64
PAGES = math.ceil(len(STYLES) / PER_PAGE)


def render(text: str, page: int) -> str:
    start = page * PER_PAGE
    lines = []
    for i, (_, fn) in enumerate(STYLES[start:start + PER_PAGE], start=start + 1):
        lines.append(f"{i}. <code>{html.escape(fn(text))}</code>")
    return f"<b>Page {page + 1}/{PAGES}</b> · tap any style to copy\n\n" + "\n\n".join(lines)


def keyboard(page: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(f"•{n + 1}•" if n == page else str(n + 1), callback_data=f"p:{n}")
        for n in range(PAGES)
    ]
    rows = [buttons[i:i + 5] for i in range(0, len(buttons), 5)]
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Send me any text and I'll reply with {len(STYLES)} font styles.\n"
        f"Tap a style to copy it. Max {MAX_LEN} characters."
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    if len(text) > MAX_LEN:
        await update.message.reply_text(f"Too long. Please send {MAX_LEN} characters or fewer.")
        return
    context.user_data["text"] = text
    await update.message.reply_text(
        render(text, 0), parse_mode=ParseMode.HTML, reply_markup=keyboard(0)
    )


async def on_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    text = context.user_data.get("text")
    if not text:
        await query.answer("Send me some text first.", show_alert=True)
        return
    page = int(query.data.split(":")[1])
    await query.answer()
    try:
        await query.edit_message_text(
            render(text, page), parse_mode=ParseMode.HTML, reply_markup=keyboard(page)
        )
    except BadRequest as e:
        if "not modified" not in str(e).lower():
            raise


def main() -> None:
    token = "7346396333:AAETgK_1ZGix3OSzB83mldgzTLxybV66C-s"
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(CallbackQueryHandler(on_page, pattern=r"^p:\d+$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling()


if __name__ == "__main__":
    main()
