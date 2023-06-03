import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tracemalloc
tracemalloc.start()



class Searcher(object):
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        
    def get_waited(self, xpath):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    def extract_property_values(self, property, tags):
        property_values = []
        for tag in tags:
            if type(tag) != str:
                tag = str(tag)
            lst = tag.split(property+"=")
            if len(lst) == 1:
                continue
            value = lst[1][1:]
            value = value[:value.index("\"")]
            property_values.append(value)
        return property_values

    def filter_tags(self, s):
        inTag = False
        currString = ""
        response = []
        for letter in s:
            if letter == "<":
                inTag = True
                if currString:
                    response.append(currString)
                currString = ""
            elif letter == ">":
                inTag = False
            else:
                if not inTag:
                    currString += letter
        if currString:
            response += currString
        
        return "".join(response)

    def filter_by_contains_property(self, property_names, tags):
        filtered_tags = []
        for tag in tags:
            if type(tag) != str:
                tag = str(tag)
            matching_properties = 0
            property_values = tag.split(" ")
            for property_value in property_values:
                if "=" not in property_value:
                    continue
                if property_value.split("=")[0] in property_names:
                    matching_properties += 1
            if matching_properties == len(property_names):
                filtered_tags.append(tag)
        return filtered_tags        

    def get_similar_questions(self, soup):
        similar_questions = soup.find_all("span", {"class": "CSkcDe"})
        similar_questions = list(map(str, similar_questions))
        similar_questions = list(map(self.filter_tags, similar_questions))
        return similar_questions

    def get_answers(self, soup):
        answers = soup.find_all("span", {"class": "hgKElc"})
        answers = list(map(str, answers))
        answers = list(map(self.filter_tags, answers))
        return answers

    def get_query_answers(self, query):
        self.driver.get("https://www.google.com/")
        search_bar = self.get_waited("//textarea[@type='search']")
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)
        self.get_waited("//span[@class='CSkcDe']")
        self.get_waited("//span[@class='hgKElc']")
        
        
        response = {}
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        questions = [query]
        questions += self.get_similar_questions(soup)
        answers = self.get_answers(soup)
        
        for question, answer in zip(questions, answers):
            response[question] = answer
        return response

    def get_search_results(self, query, pages):
        if type(pages) != int:
            pages = int(pages)
        
        self.driver.get("https://www.google.com/")
        search_bar = self.get_waited("//textarea[@type='search']")
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(4)
        
        for __load_results__ in range(pages):
            # Scroll down to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the page to load and the new search results to appear
            time.sleep(1)
            

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        anchor_tags = soup.find_all('a')
        anchor_tags = self.filter_by_contains_property(["data-ved", "ping"], anchor_tags)
        links = self.extract_property_values("href", anchor_tags)
        links = [link for link in links if link.find("https://www.") == 0]
        return links


def search(query, pages=2):
    searcher = Searcher()
    # result links
    search_results = searcher.get_search_results(query, pages)
    return search_results

def ask_question(query):
    searcher = Searcher()
    response = searcher.get_query_answers(query)
    return response