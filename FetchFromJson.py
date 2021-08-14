import json
import time
from RetriveDB import DatabaseController
from datetime import datetime, timedelta

db = DatabaseController()
date_dict = {
    -2 : "the_day_before_yesterday",
    -1 : "yesterday",
    0 : "today",
    1 : "tomorrow",
    2 : "the_day_after_tomorrow"
}

# find the date today, yesterday, tomorrow, etc.
today = datetime.now()
yesterday = datetime.now() - timedelta(1)
the_day_before_yesterday = datetime.now() - timedelta(2)
tomorrow = datetime.now() + timedelta(1)
the_day_after_tomorrow = datetime.now() + timedelta(2)

today_str = datetime.strftime(today, '%Y-%m-%d')
yesterday_str = datetime.strftime(yesterday, '%Y-%m-%d')
the_day_before_yesterday_str = datetime.strftime(the_day_before_yesterday, '%Y-%m-%d')
tomorrow_str = datetime.strftime(tomorrow, '%Y-%m-%d')
the_day_after_tomorrow_str = datetime.strftime(the_day_after_tomorrow, '%Y-%m-%d')


# find the page belong to today 
def findPageIdList(date_str):
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

                for item in page["properties"]["Name"]["title"]:
                    page_list_name.append(item.get("plain_text"))
        except:
            continue    
    # return page_list_id, page_list_name
    return page_list_id


# generate blocks based on page id list
def generateBlocks(page_list_id: list):
    block_json = {}

    for num in range(0, len(page_list_id)):
        block_json["task " + str(num)] = db.readBlock(page_list_id[num])

    return block_json


def generateBlocksFile():
    today_page_list = findPageIdList(today_str)
    yesterdaypage_list = findPageIdList(yesterday_str)
    the_day_before_yesterday_page_list = findPageIdList(the_day_before_yesterday_str)
    tomorrow_page_list = findPageIdList(tomorrow_str)
    the_day_after_tomorrow_page_list = findPageIdList(the_day_after_tomorrow_str)

    block_total_json = {}
    block_total_json["today"] = generateBlocks(today_page_list)
    block_total_json["yesterday"] = generateBlocks(yesterdaypage_list)
    block_total_json["the day before yesterday"] = generateBlocks(the_day_before_yesterday_page_list)
    block_total_json["tomorrow"] = generateBlocks(tomorrow_page_list)
    block_total_json["the day after tomorrow"] = generateBlocks(the_day_after_tomorrow_page_list)

    with open('./blocks.json', 'w', encoding='utf8') as f:
        json.dump(block_total_json, f, ensure_ascii=False, indent = 4, sort_keys=True)

        
# generate blocks children based on page id list
def generateBlocksChildren():
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

    block_children_total_json["today"] = block_children_json
    block_children_total_json["yesterday"] = block_children_json1
    block_children_total_json["the day before yesterday"] = block_children_json2
    block_children_total_json["tomorrow"] = block_children_json3
    block_children_total_json["the day after tomorrow"] = block_children_json4

    with open('./block_children.json', 'w', encoding='utf8') as f:
        json.dump(block_children_total_json, f, ensure_ascii=False, indent = 4, sort_keys=True)


# 




# fetch the newest data into json file
generateBlocksFile()
time.sleep(1)
generateBlocksChildren()


# while True:



