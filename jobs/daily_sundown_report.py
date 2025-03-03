from third_party.discord import client as discord
from third_party.stock_news import client as stock_news

from bots import finance_bot
from scheduler import instance
from scheduler import jobs


def _format_report(report: dict) -> str:
    return f"headline: {report['headline']}\ncontent: {report['text']}"


@instance.DefaultBackgroundScheduler.scheduled_job(jobs.TriggerType.CRON, day_of_week="tue-sat", hour=9, minute=0)
def main():
    report = stock_news.get_latest_sundown_report()
    openai_bot = finance_bot.load_finance_bot()

    response = openai_bot.invoke(_format_report(report))
    discord.send_to_finance(f"{response.content}\n-# Translation by AI")
