import requests, json

# load token and database ID
with open('./secret_key.txt', 'r') as f:
    temp_list = f.read().splitlines()
f.close()

token_backup = temp_list[0]
database_id_backup = temp_list[1]


class DatabaseController:

    def __init__(self):
        self.token = token_backup
        self.database_id = database_id_backup
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-07-27"
        }

    # read the entire database and load it into json format
    def readDatabase(self):
        readUrl = "https://api.notion.com/v1/databases/" + self.database_id + "/query"

        res = requests.request("POST", readUrl, headers = self.headers)
        data = res.json()

        with open('./database.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent = 4, sort_keys=True)


    # # read daily tasks based on sorted pageId and load it into json format
    # def readPage(self, pageId):
    #     readUrl = f"https://api.notion.com/v1/pages/{pageId}"

    #     res = requests.request("GET", readUrl, headers=self.headers)
    #     data = res.json()
    #     # print(res.status_code)

    #     with open('./page.json', 'w', encoding='utf8') as f:
    #         json.dump(data, f, ensure_ascii=False, indent = 4, sort_keys=True)


    # read page content as block and check if have children
    def readBlock(self, pageId):
        readUrl = f"https://api.notion.com/v1/blocks/{pageId}"

        res = requests.request("GET", readUrl, headers=self.headers)
        data = res.json()
        return data

    
    # def updateBlock(self, pageId):
    #     readUrl = f"https://api.notion.com/v1/blocks/{pageId}"

    #     res = requests.request("GET", readUrl, headers=self.headers)
    #     data = res.json()
    #     # print(res.status_code)

    #     return data
    #     with open('./blocks.json', 'a', encoding='utf8') as f:
    #         json.dump(data, f, ensure_ascii=False, indent = 4, sort_keys=True)


    # read its children and load it into json format
    def readBlockChildren(self, pageId):
        readUrl = f"https://api.notion.com/v1/blocks/{pageId}/children"

        res = requests.request("GET", readUrl, headers=self.headers)
        data = res.json()
        return data

    def updateBlockChildren(self, blockID):
        check_status = False
        updateUrl = f"https://api.notion.com/v1/blocks/{blockID}"

        res = requests.request("GET", updateUrl, headers=self.headers)
        current_data = res.json()
        current_status = current_data["to_do"]["checked"]

        if current_status == False:
            check_status = True
        elif current_status == True:
            check_status = False

        update_data = {
            "to_do": {
                "checked": check_status
                # "checked": check_status,
                # "text": [{ 
                #     "text": { "content": "review resume" } 
                #     }]
            }
        }

        data = json.dumps(update_data)
        response = requests.request("PATCH", updateUrl, headers=self.headers, data=data)
        # print(response.status_code)
        # print(response.text)



# db = DatabaseController()
# db.readDatabase()
# readPage(page_id, headers)
# readBlock(page_id, headers)
# readBlockChildren(page_id, headers)
# db.updateBlockChildren("3ea087d6-d5e0-4056-98de-3f3e6666d069")