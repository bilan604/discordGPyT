import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tracemalloc
tracemalloc.start()
import openai
import asyncio

openai.api_key = "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"

async def askOpenAI003(query):
  message = "[Empty Message]"
  try:
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=query,
                                        temperature=0.35,
                                        max_tokens=1000)
    message = response.choices[0].text
    time.sleep(2)
  except Exception as e:
    print(e)

  return message



class Node(object):
    def __init__(self, s="", parent=None, children=[]):
        self.tag = None
        self.s = s
        self.parent = parent
        self.children = children


def nest_tags(curr, tagList, tagMap):
    idx = tagList.index(curr)
    if idx == len(tagList) - 1:
        tagMap[curr]

    count = 0
    subarr = []
    for i in range(idx+1, len(tagList)):
        if tagList[i][0] == "/":
            count -= 1
            if not count:
                
                for child in subarr:
                    if child[0] != "/":
                        tagMap[curr].children[child] = tagMap[child]
                        tagMap[child] = nest_tags(child, subarr, tagMap)
                return tagMap[curr]
            else:
                subarr.append(tagList[i])
        else:
            subarr.append(tagList[i])
            count += 1
    return tagMap[curr]


class JobAppBot:

    def __init__(self, username, password, driver_path):
        self.username = username
        self.password = password
        self.driver_path = driver_path
        self.node = None

        self.driver = None
        self.initialize()


    def get_redir(self, label):
        # Figure out something for multiple words
        label = label.upper()
        tags = self.get_tags()
        links = []
        for i, tag in enumerate(tags):
            if "href" in tag:
                stack = []
                for j in range(i, len(tags)):
                    if tags[j][0] == "/":
                        if stack:
                            stack.pop()
                            if not stack:
                                if label in "".join(tags[i:j]).upper():
                                    links.append(tags[i])
                    else:
                        stack.append(tags[j])

        # links
        for link in links:
            if label in link.upper():
                return link
        return links[0]
    
    def get_stack(self, i, tags):
        stack = []
        container = []
        for j in range(i, len(tags)):
            if tags[j][0] == "/":
                if stack:
                    container.append(stack.pop())
                    if not stack:
                        return container
            else:
                stack.append(tags[j])
        return container

    def find_label(self, node, label, vis):
        vis[node] = 0        
        for child in node.children:
            if label in child.s:
                return True
            if child not in vis:
                self.find_label(child, label, vis)
        return False


    def label_dfs(self, node, element, label, vis):
        vis[node] = 0
        if not node:
            return ""
        if node.tag.find(element) == 1:
            if self.find_label(node, label, vis.copy()):
                return node.tag
            
        for child in node.children:
            if child not in vis:
                ans = self.label_dfs(child, element, label, vis)
                if ans: return ans
        return ""


    def initialize(self):
        login_link = "https://linkedin.com/uas/login"
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.get(login_link)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    def get_waited(self, xpath):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    # returns the value of a property inside a tag
    def get_property(self, desc, tag):
        if type(tag) == list:
            return [self.get_property(s) for s in tag]
        lst = tag.split(" ")
        for s  in lst:
            if s.find(desc) == 0:
                return s.split("=")[1][1:-1]
        return None
    
    def get_tags(self, s):
        ans = []
        adding = False
        curr = ""
        for letter in s:
            if letter == "<":
                adding = True
            elif letter == ">":
                adding = False
                ans.append(curr)
                curr = ""
            else:
                if adding:
                    curr += letter

        return ans            

    def decompose(self, s):
        ans = []
        c = 0
        currStr = ""
        s = s[s.index("<"):]
        for letter in s:
            if letter in (">", "<"):
                c += 1
                if letter == ">":
                    if currStr[0] != "/":
                        #print("Div start", currStr)
                        ans.append("-"+currStr)
                    else:
                        #print("End", currStr)
                        ans.append(currStr)
                else:
                    #print("Contents", currStr)
                    ans.append(currStr)
                currStr = ""
            else:
                currStr += letter
        return ans



    def get_dd(self, s=""):
        
        if not s:
            s = self.driver.page_source

        def filter(tags):
            """
            l,r = -1, -1
            for i in range(len(tags)):
                if tags[i].find("body") == 1:
                    if tags[i][0] == "-":
                        l = i
                    else:
                        r = i
            tags = tags[l:r+1]
            """
            newTags = []
            for t in tags:
                if len(t) == 0 or t[0] == "!":
                    continue
                if len(t) == 1 or t[1] == "!" or len(t) < 4:
                    continue
                if len(t) > 2000:
                    t = t[:150] + t[-10:]
                if t[0] == "-":
                    t = "<" + t[1:] + ">"
                if re.sub("[a-zA-Z]", "", t) == t:
                    continue
                if t.find("-meta") == 0:
                    continue
                t = re.sub("( )+", " ", t)
                t = re.sub("(\n)+", " ", t)
                
                newTags += [t]
            return newTags

        tags = self.decompose(s)
        tags = filter(tags)
        dd = {t: Node("") for t in tags}
        
        stack = []
        for i in range(len(tags)):
            if tags[i][0] == "/":
                if not stack:
                    continue
                subtag = stack.pop()
                if stack:
                    childNode = dd[subtag]
                    parentNode = dd[stack[-1]]
                    if (childNode != parentNode):
                        parentNode.children.append(childNode)
            elif tags[i][0] == "<":
                stack.append(tags[i])
            else:
                if stack:
                    dd[stack[-1]].s += tags[i]
                else:
                    dd[tags[0]].s += tags[i]
        for tagString, node in dd.items():
            node.tag = tagString
        return dd[tags[0]]
        

    def login(self):

        nameInp = self.get_waited('//input[@id="username"]')
        nameInp.send_keys(self.username)

        pwInp = self.get_waited('//input[@id="password" and @type="password"]')
        pwInp.send_keys(self.password)

        sign_in = self.get_waited('//button[@class="btn__primary--large from__button--floating"]')
        sign_in.click()
        return

    def get_link(self, tag):

        link = tag.split("href=\"")[1]
        print(link)
        return link[:link.index("\"")]
            
    def get_attribute_value(self, attribute, tag):
        val = tag.split(attribute+"=\"")[1]
        return val[:val.index("\"")]

    # i.e. "button", "Add position"
    def get_job_ids(self):
        s = self.driver.page_source
        lst = self.get_tags(s)
        ans = []
        for i in range(len(lst)):
            if lst[i].find("div") == 0 and "data-job-id" in lst[i]:
                items = lst[i].split(" ")
                for property in items:
                    if "data-job-id" in property:
                        s = property.split("data-job-id=")[1][1:-1]
                        print(s)
                        ans.append(s)
        return ans
    
    def get_labelled_elements(self, element, element_labels):
        s = self.driver.page_source
        lst = self.get_tags(s)
        ans = []
        for i in range(len(lst)):
            if lst[i].find(element) == 0:
                c = 0
                cache = lst[i][lst[i].index(" ")+1:]
                attributes = cache.split(" ")
                newAttributes = []
                for attr in attributes:
                    if "=" in attr:
                        newAttributes.append(attr)
                    else:
                        if not newAttributes:
                            continue
                        newAttributes[-1] += " " + attr
                for attr in newAttributes:
                    key = attr.split("=")[0]
                    if key in element_labels:
                        val = attr[attr.index("="):][1:]
                        if element_labels[key] in val:
                            c += 1

                if c == len(element_labels):
                    ans.append(lst[i]) 
        return ans

    def get_labelled_element(self, element, element_labels):
        s = self.driver.page_source
        lst = self.get_tags(s)
        for i in range(len(lst)):
            if lst[i].find(element) == 0:
                c = 0
                cache = lst[i][lst[i].index(" ")+1:]
                attributes = cache.split(" ")
                newAttributes = []
                for attr in attributes:
                    if "=" in attr:
                        newAttributes.append(attr)
                    else:
                        if not newAttributes:
                            continue
                        newAttributes[-1] += " " + attr
                for attr in newAttributes:
                    key = attr.split("=")[0]
                    if key in element_labels:
                        val = attr[attr.index("="):][1:]
                        if element_labels[key] in val:
                            c += 1

                if c == len(element_labels):
                    return lst[i]
        return None
    
    def replace_link(self, link, id):
        #"https://www.linkedin.com/jobs/search/?currentJobId=3596751029&f_AL=true&f_WT=2&geoId=103644278&sortBy=R"
        digits = [str(i) for i in range(10)]
        lst = link.split("currentJobId=")
        for j in range(len(lst[1])):
            if lst[1][j] not in digits:
                lst[1] = lst[1][j:]
                break
        newLink = lst[0] + "currentJobId=" + id + lst[1]
        print(f" {newLink=} ")
        return newLink

    def get_input_response(self, label):
        time.sleep(1)
        s = ""
        question = self.driver.page_source.split(label)[1]
        print(f" {question[:200]=} ")
        for letter in question:
            if letter == "<":
                break
            s += letter

        if "PHONE" in question.upper():
            return "5307606956"
        if "How many years".upper() in question.upper():
            return "0"
        return ""

    def fill_out_forms(self, job_id):
        """
        labels = self.get_labelled_elements("label", {"for": "signle-line-text-form"})
        print(f" {labels=} ")
        for label in labels:
            print(label)
            input_id = self.get_property("id", label)
            print(f" {input_id=} ")
            input = self.get_labelled_element("input", {"id": input_id})
            response = self.get_input_response(label)
            input.send_keys(response)
        """

        review_tag = self.get_labelled_element("button", {"aria-label": "Review"})
        next_tag = self.get_labelled_element("button", {"aria-label": "next"})
        if review_tag:
            button_tag = review_tag
        if next_tag:
            button_tag = next_tag
        button_id = self.get_property("id", button_tag)
        xpath = '//button[@id="' + button_id + '"]'
        continue_application = self.get_waited(xpath)
        continue_application.click()
        

    def add_start(self, link):
        if "start=" not in link:
            return link + "&start=24"
        lst = link.split("&start=")
        return lst + "&start=" + str(int(lst[1]) + 24)

    # Be on the easy apply page
    def apply(self, job_id):
        if not job_id:
            print("No ea_button_tag")
            return
        
        time.sleep(4)
        ea_button_tag = self.get_labelled_element("button", {"aria-label": "Easy", "data-job-id": job_id})
        print(f" {ea_button_tag=} ")
        ea_button_id = self.get_property("id", ea_button_tag)
        print(f" {ea_button_id=} ")
        xpath = '//button[@id="' + ea_button_id + '"]'
        easy_apply = self.get_waited(xpath)
        easy_apply.click()
        time.sleep(1)

        for i in range(8):
            try:
                time.sleep(0.2)
                submit_tag = self.get_labelled_element("button", {"aria-label": "Submit"})
                print(f" {submit_tag=} ")

                if not submit_tag:
                    print("No Submit Tag")
                    self.fill_out_forms(job_id)
                else:
                    submit_id = self.get_property("id", submit_tag)
                    xpath = '//button[@id="' + submit_id + '"]'
                    submit_application = self.get_waited(xpath)
                    submit_application.click()
                    print("\n\n\nSUBMITTED APPLICATION\n\n\n")
                    with open("submitted.txt", "a") as f:
                        f.write(job_id + "\n")
                    time.sleep(5)
                    break
            except:
                print("Crash in apply", job_id)
                pass
        
        return 

    def easier_apply(self, base_link):
        self.driver.get(base_link)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        base_job_id = base_link.split("currentJobId=")[1]
        self.apply(base_job_id[:base_job_id.index("&")])
        
        job_ids = self.get_job_ids()
        print(f" {job_ids=} ")
        for job_id in job_ids:
            try:
                link = self.replace_link(base_link, job_id)
                self.driver.get(link)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                self.apply(job_id)
            except:
                print("Error on", job_id)        
        print("__________________")
        return

    def apply_jobs(self):
        links = ["https://www.linkedin.com/jobs/search/?currentJobId=3584043464&f_AL=true&f_WT=2&geoId=103644278&keywords=software%20engineer%20intern&location=United%20States&refresh=true",
                 "https://www.linkedin.com/jobs/search/?currentJobId=3579989568&f_AL=true&f_WT=2&geoId=103644278&keywords=node.js&location=United%20States&refresh=true"]
        for link in links:
            try:
                for i in range(15):
                    self.easier_apply(link)
                    link = self.add_start(link)
                    print("New Link", link)
                    time.sleep(4)
            except:
                pass
                

    def run(self):
        self.login()
        time.sleep(20)
    
        self.apply_jobs()


PROMPT = ""
with open("prompt.txt", "r") as f:
    PROMPT = "".join(f.readlines())


async def main():
    prompt = PROMPT + "What is your name?"
    response = await askOpenAI003(prompt)
    response = re.sub("(\n)+", "", response)
    print(f" {response=} ")
    pass

with open("main.py", "rb") as f:
    s = f.readline()
    print("??", s)
    print(s.decode("ascii"))

#bot = JobAppBot("bilan604@yahoo.com", "6047822691aA", "chromedriver.exe")
#bot.run()


