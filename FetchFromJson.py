import json
import time
from RetriveDB import DatabaseController
from datetime import datetime, timedelta

db = DatabaseController()

# # find the date today, yesterday, tomorrow, etc.
# today = datetime.now()
# yesterday = datetime.now() - timedelta(1)
# the_day_before_yesterday = datetime.now() - timedelta(2)
# tomorrow = datetime.now() + timedelta(1)
# the_day_after_tomorrow = datetime.now() + timedelta(2)

# today_str = datetime.strftime(today, '%Y-%m-%d')
# yesterday_str = datetime.strftime(yesterday, '%Y-%m-%d')
# the_day_before_yesterday_str = datetime.strftime(the_day_before_yesterday, '%Y-%m-%d')
# tomorrow_str = datetime.strftime(tomorrow, '%Y-%m-%d')
# the_day_after_tomorrow_str = datetime.strftime(the_day_after_tomorrow, '%Y-%m-%d')

class JsonFileController:
    def __init__(self):
        # find the date today, yesterday, tomorrow, etc.
        self.today = datetime.now()
        self.yesterday = datetime.now() - timedelta(1)
        self.the_day_before_yesterday = datetime.now() - timedelta(2)
        self.tomorrow = datetime.now() + timedelta(1)
        self.the_day_after_tomorrow = datetime.now() + timedelta(2)

        self.today_str = datetime.strftime(self.today, '%Y-%m-%d')
        self.yesterday_str = datetime.strftime(self.yesterday, '%Y-%m-%d')
        self.the_day_before_yesterday_str = datetime.strftime(self.the_day_before_yesterday, '%Y-%m-%d')
        self.tomorrow_str = datetime.strftime(self.tomorrow, '%Y-%m-%d')
        self.the_day_after_tomorrow_str = datetime.strftime(self.the_day_after_tomorrow, '%Y-%m-%d')
    
    def getTodayDate(self):
        return self.today_str

    def getTmrDate(self):
        return self.tomorrow_str

    def getTheDayAfterTmrDate(self):
        return self.the_day_after_tomorrow_str

    def getYesterdayDate(self):
        return self.yesterday_str

    def getTheDayBeforeYesterdayDate(self):
        return self.the_day_before_yesterday_str

    # find the page belong to today 
    def findPageIdList(self, date_str):
        page_list_id = []
        page_list_name = []

        # load database.json
        with open('./database.json', 'r', encoding='utf8') as f:
            data = json.load(f)

        for page in data["results"]:
            try:
                dates = page["properties"]["Date"]["date"]["start"]
        
                if dates.find(date_str) != -1:
                    page_list_id.append(page["id"])

                    # for item in page["properties"]["Name"]["title"]:
                    #     page_list_name.append(item.get("plain_text"))
            except:
                continue    
        f.close()
        # return page_list_id, page_list_name
        return page_list_id


    # generate blocks based on page id list
    def generateBlocks(self, page_list_id: list):
        block_json = {}

        for num in range(0, len(page_list_id)):
            block_json["task " + str(num)] = db.readBlock(page_list_id[num])

        return block_json


    def generateBlocksFile(self):
        today_page_list = self.findPageIdList(self.today_str)
        yesterdaypage_list = self.findPageIdList(self.yesterday_str)
        the_day_before_yesterday_page_list = self.findPageIdList(self.the_day_before_yesterday_str)
        tomorrow_page_list = self.findPageIdList(self.tomorrow_str)
        the_day_after_tomorrow_page_list = self.findPageIdList(self.the_day_after_tomorrow_str)

        block_total_json = {}
        block_total_json["today"] = self.generateBlocks(today_page_list)
        block_total_json["yesterday"] = self.generateBlocks(yesterdaypage_list)
        block_total_json["the day before yesterday"] = self.generateBlocks(the_day_before_yesterday_page_list)
        block_total_json["tomorrow"] = self.generateBlocks(tomorrow_page_list)
        block_total_json["the day after tomorrow"] = self.generateBlocks(the_day_after_tomorrow_page_list)

        with open('./blocks.json', 'w', encoding='utf8') as f:
            json.dump(block_total_json, f, ensure_ascii=False, indent = 4, sort_keys=True)
        
        f.close()

            
    # generate blocks children based on page id list
    def generateBlocksChildren(self):
        block_children_json = {}
        block_children_json1 = {}
        block_children_json2 = {}
        block_children_json3 = {}
        block_children_json4 = {}
        block_children_total_json = {}

        with open('./blocks.json', 'r', encoding='utf8') as f:
            data = json.load(f)

        for num0 in range(0, len(data["today"])):
            if data["today"]["task " + str(num0)]["has_children"] == True:
                block_children_json["task " + str(num0)] = db.readBlockChildren(data["today"]["task " + str(num0)]["id"])
            else:
                continue

        for num1 in range(0, len(data["yesterday"])):
            if data["yesterday"]["task " + str(num1)]["has_children"] == True:
                block_children_json1["task " + str(num1)] = db.readBlockChildren(data["yesterday"]["task " + str(num1)]["id"])
            else:
                continue

        for num2 in range(0, len(data["the day before yesterday"])):
            if data["the day before yesterday"]["task " + str(num2)]["has_children"] == True:
                block_children_json2["task " + str(num2)] = db.readBlockChildren(data["the day before yesterday"]["task " + str(num2)]["id"])
            else:
                continue

        for num3 in range(0, len(data["tomorrow"])):
            if data["tomorrow"]["task " + str(num3)]["has_children"] == True:
                block_children_json3["task " + str(num3)] = db.readBlockChildren(data["tomorrow"]["task " + str(num3)]["id"])
            else:
                continue
        for num4 in range(0, len(data["the day after tomorrow"])):
            if data["the day after tomorrow"]["task " + str(num4)]["has_children"] == True:
                block_children_json4["task " + str(num4)] = db.readBlockChildren(data["the day after tomorrow"]["task " + str(num4)]["id"])
            else:
                continue    
        f.close()

        block_children_total_json["today"] = block_children_json
        block_children_total_json["yesterday"] = block_children_json1
        block_children_total_json["the day before yesterday"] = block_children_json2
        block_children_total_json["tomorrow"] = block_children_json3
        block_children_total_json["the day after tomorrow"] = block_children_json4

        with open('./block_children.json', 'w', encoding='utf8') as f1:
            json.dump(block_children_total_json, f1, ensure_ascii=False, indent = 4, sort_keys=True)
        f1.close()

    # call function to retrive block content
    def resetBlockContent(self):
        # fetch the newest data into json file
        self.generateBlocksFile()
        time.sleep(.1)
        self.generateBlocksChildren()
        time.sleep(.1)


    # get page name list by date
    def getPageNameListWithChildrenStatus(self, date_str):
        page_list_name = []
        children_list_bool = []

        date_dict = {
            self.the_day_before_yesterday_str : "the day before yesterday",
            self.yesterday_str : "yesterday",
            self.today_str : "today",
            self.tomorrow_str : "tomorrow",
            self.the_day_after_tomorrow_str : "the day after tomorrow"
        }

        # load database.json
        with open('./database.json', 'r', encoding='utf8') as f:
            data = json.load(f)
        
        # load blocks.json
        with open('./blocks.json', 'r', encoding='utf8') as f1:
            data_blocks = json.load(f1)

        for page in data["results"]:
            try:
                dates = page["properties"]["Date"]["date"]["start"]
        
                if dates.find(date_str) != -1:
                    for item in page["properties"]["Name"]["title"]:
                        page_list_name.append(item.get("plain_text"))
            except:
                continue
        
        for num in range(0, len(data_blocks[date_dict[date_str]])):
            if data_blocks[date_dict[date_str]]["task " + str(num)]["child_page"]["title"] in page_list_name:
                children_list_bool.append(data_blocks[date_dict[date_str]]["task " + str(num)]["has_children"])

        f.close()
        f1.close()
        # Format: [page name], [children status]
        # return ["Email with office", "TODO_list"], [False, True]
        return page_list_name, children_list_bool


    # get one page block children list by page name (if have children, if not return page name)
    def getChildrenName(self, date_str, page_name: str, children_bool: bool):
        task_list = []

        date_dict = {
            self.the_day_before_yesterday_str : "the day before yesterday",
            self.yesterday_str : "yesterday",
            self.today_str : "today",
            self.tomorrow_str : "tomorrow",
            self.the_day_after_tomorrow_str : "the day after tomorrow"
        }

        with open('./blocks.json', 'r', encoding='utf8') as f:
            data_blocks = json.load(f)

        for i in range(0, len(data_blocks[date_dict[date_str]])):
            if page_name == data_blocks[date_dict[date_str]]["task " + str(i)]["child_page"]["title"]:
                task_num = "task " + str(i)

        if children_bool == False:
            return None

        else:
            with open('./block_children.json', 'r', encoding='utf8') as f:
                data = json.load(f)
            
            for sub_task in data[date_dict[date_str]][task_num]["results"]:
                if sub_task["type"] == "to_do":
                    to_do_json = sub_task.get("to_do")
                    text_json = to_do_json["text"]
                    task_list.append((text_json[0].get("plain_text"), to_do_json["checked"]))
                else: 
                    continue
            f.close()

        # [(todo_list_name, check_status)]
        # return [(Fix resume, True), (Start new project, False)]
        return task_list


    # update todo check box by check or uncheck
    def updateTodoSubtask(self, task_id):
        # "POST" method to notion api
        db.updateBlockChildren(task_id)



'''
1. reset whole database when we make a change on Notion (press three buttons together)
2. display page name of (task of) today
    1. press button 1 with button 2 or 3 to switch days
    2. press button 1 to confirm which page to get in to set sub-tasks (TODO_list: check boxs)
    3. press button 2 or 3 to go up or down to choose different pages
3. when get in one page to be able to see page sub-tasks
    1. press button 1 to check completeness sub-tasks (check boxs)
    2. press button 2 to go back last page
    3. press button 3 to go down to other sub-tasks
'''

# TEST functions
# js = JsonFileController()
# print(js.getTodayDate())
# js.resetBlockContent()

# while True:
#     info = input('Message : ')

#     if info == "1":
#         db.readDatabase()
#     elif info == "2":
#         js.resetBlockContent()
#     elif info == "3":
#         print(js.getPageNameListWithChildrenStatus("2021-08-15"))
#     elif info == 4:
#         js.getPageNameListWithChildrenStatus(tomorrow_str)
#     elif info == 5:
#         js.getPageNameListWithChildrenStatus(the_day_after_tomorrow_str)
#     elif info == "6":
#         print(js.getPageNameListWithChildrenStatus("2021-08-14"))
#     elif info == 7:
#         js.getPageNameListWithChildrenStatus(the_day_before_yesterday_str)
#     elif info == 7:
#         js.getChildrenName(today_str, "TODO", True)
#     elif info == "7":
#         print(js.getChildrenName("2021-08-15", "TODO", True))


