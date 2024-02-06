from bot import bot


if __name__ == "__main__":
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"Ошибка: {e}")
