from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

class Scraper:
    def __init__(self, login_data: dict, job_title: str, filename: str, hidden: bool = False, logs: bool = False) -> None:
        self.login_data =  login_data
        self.job_title = job_title

        self.hidden = hidden
        self.logs = logs

        self.filename = filename

        self.driver = self.setup_driver()

    def setup_driver(self) -> webdriver.Edge:
        edge_service = Service(executable_path='./driver/msedgedriver.exe')
        edge_options = Options()
        if self.hidden:
            edge_options.add_argument("--headless")
            edge_options.add_argument("--disable-gpu")

        if not self.logs:
            edge_options.add_argument("--log-level=3")
        
        print('setup the driver successfully!')

        return webdriver.Edge(service=edge_service, options=edge_options)


    def login(self) -> None:
        self.driver.get('https://www.linkedin.com/login')

        self.driver.find_element(By.ID, 'username').send_keys(self.login_data['username'])
        self.driver.find_element(By.ID, 'password').send_keys(self.login_data['password'])

        self.driver.find_element(By.CSS_SELECTOR, 'button.btn__primary--large.from__button--floating').click()

        print('logged in successfully!')

    def get_titles(self) -> list:

        return []
    

    def run(self) -> None:
        self.login()
