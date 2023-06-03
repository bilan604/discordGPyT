import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




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
            time.sleep(4)
            

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        anchor_tags = soup.find_all('a')
        anchor_tags = self.filter_by_contains_property(["data-ved", "ping"], anchor_tags)
        links = self.extract_property_values("href", anchor_tags)
        links = [link for link in links if link.find("https://www.") == 0]
        return links


def ask_question(query):
    os.chdir("c:/Users/bill/github/DiscordGPyT/Helpers")
    searcher = Searcher()
    response = searcher.get_query_answers(query)
    return response

def search(query, pages=2):
    os.chdir("c:/Users/bill/github/DiscordGPyT/Helpers")
    searcher = Searcher()
    search_results = searcher.get_search_results(query, pages)
    return search_results


# Usage:
"""
print(ask_question("Why are cats cute?"))

    {'Why are cats cute?': "What the Science Says. Like babies, cats seem to activate our brain's cuteness response. This might be due to cats' physical characteristics, including child-like features like big eyes and small noses. Studies have shown that humans, particularly women, extend the “baby schema effect” to animals as well as babies.", 'Do cats realize that they are cute?': "According to a recent study, cats will blast the cuteness level up to 100 if they think it will get them an early, or more hearty meal. Cats know they're cute, and they know that you love when they're cute, and they use their feline wiles to lure you into forking over some extra yum yums.", 'Why do humans think cats are beautiful?': "It's those oversized heads relative to body size, big eyes, round ears, floppy tails and ears and rounded body shapes that make us grin from ear to ear. Breeds that exhibit several of these features 
    are known to be extra cute.", 'Why are cats so much cuter than dogs?': 'For one, cats tend to retain their kitten like appearance throughout. I mean, they look cute throughout. While dogs grow up to be those humongous beings, at time terrifying, cats remain more in the cuteness zone, even when they grow up.', 'Why are kittens so adorable?': 'Kittens (and puppies) also have large heads and huge eyes, so are considered cuter than the more evenly-proportioned beady-eyed rodents nature provides us with. Younger animals generally provoke this cuteness reflex more, even if the adult version is still relatively 
    small and fluffy.'}
"""

"""
print(search("Why are cats cute?"))

    ["https://www.hillspet.com/pet-care/behavior-appearance/why-are-dogs-and-cats-cute#:~:text=It's%20those%20oversized%20heads%20relative,known%20to%20be%20extra%20cute.", 'https://www.innfinity.in/limitless/why-cats-are-cuter-than-dogs/#:~:text=For%20one%2C%20cats%20tend%20to,even%20when%20they%20grow%20up.', 'https://www.theguardian.com/commentisfree/2018/apr/11/cats-why-are-kittens-so-cute#:~:text=Kittens%20(and%20puppies)%20also%20have,still%20relatively%20small%20and%20fluffy.', 'https://www.rover.com/blog/why-are-cats-so-cute/', 'https://www.trustedhousesitters.com/blog/pets/why-are-cats-so-cute/', 'https://www.quora.com/From-a-psychological-point-of-view-what-makes-cats-so-cute', 'https://www.theguardian.com/commentisfree/2018/apr/11/cats-why-are-kittens-so-cute', 'https://www.hillspet.com/pet-care/behavior-appearance/why-are-dogs-and-cats-cute', 'https://www.travelingwithyourcat.com/why-are-cats-so-cute/', 'https://www.sheknows.com/living/articles/959467/cute-cats/', 'https://www.treehugger.com/the-science-behind-your-cats-most-adorable-features-4863944', 'https://www.reddit.com/r/AskReddit/comments/orfpj/why_do_humans_find_cats_cute_even_though_they/', 'https://www.youtube.com/watch?v=bgnSD8ieGDg', 'https://www.youtube.com/watch?v=bgnSD8ieGDg&amp;t=3', 'https://www.youtube.com/watch?v=bgnSD8ieGDg&amp;t=62', 'https://www.youtube.com/watch?v=bgnSD8ieGDg&amp;t=156', 'https://www.youtube.com/watch?v=bgnSD8ieGDg', 'https://www.youtube.com/watch?v=bgnSD8ieGDg&amp;t=3', 'https://www.youtube.com/watch?v=bgnSD8ieGDg&amp;t=62', 'https://www.youtube.com/watch?v=bgnSD8ieGDg&amp;t=156', 'https://www.motherjones.com/environment/2016/10/cat-invasive-species-inquiring-minds/', 'https://www.rd.com/list/cutest-cat-breeds/', 
    'https://www.petfinder.com/cats-and-kittens/breeds/cutest-cat-breeds/', 'https://www.pinterest.com/pin/771734086139661516/', 'https://www.thesprucepets.com/cute-cat-breeds-5176271', 'https://www.womansday.com/life/g32979681/cute-cat-photos/', 'https://www.facebook.com/mycutecats.official/', 'https://www.dailypaws.com/cats-kittens/cat-names/cute-cat-names', 'https://www.innfinity.in/limitless/why-cats-are-cuter-than-dogs/', 'https://www.amazon.com/Baby-Cats-Cute-Christina-Leaf/dp/1648344674', 'https://www.catify.co/blogs/news/why-are-cats-so-cute-definitive-reasons-why-right-here', 'https://www.nbcnews.com/think/opinion/cats-cute-furry-cuddly-invasive-alien-species-rcna41768', 'https://www.nytimes.com/2021/12/01/technology/misinformation-cute-cats-online.html', 'https://www.travelandleisure.com/animals/most-popular-cute-cat-names', 'https://www.instagram.com/cutecatskittens/?hl=en', 'https://www.pexels.com/search/cute%20cat/', 'https://www.shutterfly.com/ideas/cat-quotes/', 'https://www.cbsnews.com/news/spider-cats-cute-kittens-bouncing-off-the-walls-literally/', 'https://www.countryliving.com/life/kids-pets/a28448103/cat-instagram-captions/', 'https://www.buzzfeed.com/shelbyheinrich/every-part-cats-cute', 'https://www.dreamstime.com/photos-images/cats-cute.html', 'https://www.goodhousekeeping.com/life/pets/a43276342/cat-instagram-captions/']
"""