from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge import service, options
from selenium.common.exceptions import NoSuchElementException 

import time, json

def waiting_counter(s: int) -> None:
    for i in range(s):
        print(f'waiting {s-i} seconds....')
        time.sleep(1)

class Scraper:
    def __init__(self, login_data: dict, job_title: str, filename: str, hidden: bool = False, logs: bool = False, default_sleep: int = 3) -> None:
        '''
            Parameters
            login_data (dictionary): dictionary of username and password of linkedin account.
            
            job_title (string): the job title your're searching for.

            filename (string): the name of the file to save data (without extension).

            hidden (bool): show or hide the browser window while working (default is False).

            logs (bool): display the logs and info of the scrapping process (default is False).

            default_sleep (int): time in seconds of waiting time between jobs.
        '''
        self.login_data =  login_data
        self.job_title = job_title

        self.hidden = hidden
        self.logs = logs

        self.filename = filename
        self.save_path = './data/'

        self.sleep = default_sleep

        self.driver = self.setup_driver()

    def setup_driver(self) -> webdriver.Edge:
        edge_service = service.Service(executable_path='./driver/msedgedriver.exe')
        edge_options = options.Options()
        if self.hidden:
            edge_options.add_argument("--headless")
            edge_options.add_argument("--disable-gpu")

        if not self.logs:
            edge_options.add_argument("--log-level=3")
        
        self.logger('setup the driver successfully!')

        return webdriver.Edge(service=edge_service, options=edge_options)


    def login(self) -> None:
        self.driver.get('https://www.linkedin.com/login')

        self.driver.find_element(By.ID, 'username').send_keys(self.login_data['username'])
        self.driver.find_element(By.ID, 'password').send_keys(self.login_data['password'])

        self.driver.find_element(By.CSS_SELECTOR, 'button.btn__primary--large.from__button--floating').click()

        self.logger('logged in successfully!')
        waiting_counter(self.sleep)

    def get_jobs(self) -> list:
        self.driver.get(f'https://www.linkedin.com/jobs/search/?keywords={self.job_title}')
        self.logger('got the jobs page.')
        waiting_counter(self.sleep)

        job_descriptions = []
        jobs = self.driver.find_elements(By.CSS_SELECTOR, 'ul.scaffold-layout__list-container > li')
        
        job_counter = 1
        for job in jobs:
            job.click()
            try:
                title = job.find_element(By.CSS_SELECTOR, 'a strong').text
            except NoSuchElementException:
                break
                # if there is no title so showd jobs are end

            description = self.driver.find_element(By.CSS_SELECTOR, 'article.jobs-description__container').text
            if description != '':
                job_descriptions.append({
                    "title": title,
                    "description": description
                })

                self.logger(f'got job #{job_counter}')
                job_counter += 1

                continue
            
            self.logger(f'failed to get job #{job_counter}')
            job_counter += 1
        
        if len(job_descriptions) == 0:
            self.logger('there is no jobs with this title.')

            return []

        self.logger(f'{len(job_descriptions)} jobs were found!')
        return job_descriptions
    
    def save_data(self, data: list) -> None:
        self.filename += '.json'
        
        try:
            with open(self.save_path + self.filename, 'w') as file:
                json.dump(data, file)
            
            self.logger(f'data was saved succesfully in {self.filename}')
        except:
            self.logger('an error has occurred.')
    
    def logger(self, msg: str) -> None:
        print(msg)

    def run(self) -> None:
        self.login()
        jobs = self.get_jobs()
        
        self.save_data(jobs)