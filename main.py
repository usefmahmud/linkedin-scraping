import os
from dotenv import load_dotenv

from utils import Scraper


load_dotenv()

login = {
    'username': os.getenv('EMAIL'),
    'password': os.getenv('PASSWORD')
}

title = 'FrontEnd Developer'

scraper = Scraper(login, title, filename='exported_data', hidden=False, logs=False)
scraper.run()