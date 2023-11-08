from flask import Flask
import schedule
from wilscraper import job
import time

app = Flask(__name__)

if __name__ == '__main__':
    posts_data = job()
    print(posts_data)  # Add this line to print the output
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    app.run(debug=True)