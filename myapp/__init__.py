from flask import Flask

app = Flask(__name__)

from myapp import ai_news, ai_summary, feeds_status, generate_daily_news, jobs, reprocess
