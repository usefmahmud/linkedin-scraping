from utils import Scraper

login = {
    'username': 'email',
    'password': 'password'
}

title = 'FrontEnd Developer'

scraper = Scraper(login, title, hidden=False, logs=False)

scraper.run()