import time
from datetime import datetime, timedelta

from RetriveDB import DatabaseController
from FetchFromJson import JsonFileController

# initialize dbcontroller and jsoncontroller
db = DatabaseController()
js = JsonFileController()

db.readDatabase()
time.sleep(0.1)
js.resetBlockContent()
time.sleep(0.1)

while True:
    # find the date today, yesterday, tomorrow, etc.
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(1)

    today_str = datetime.strftime(today, '%Y-%m-%d')
    tomorrow_str = datetime.strftime(tomorrow, '%Y-%m-%d')
    temp_date_str = time.localtime()

    # fetch the newest database at 23:57 everyday
    if temp_date_str[3:5] == (23,57):
        db.readDatabase()
        time.sleep(0.1)
        js.resetBlockContent()
        time.sleep(0.1)

    # reset local datebase if new day start
    if temp_date_str[3:5] == (23,59):

        unfinished_task_list = []
        page_list, children_list = js.getPageNameListWithChildrenStatus(today_str)
        time_str = js.getTodayDate()

        try:
            # get the children list
            task_list, task_id_list = js.getChildrenName(time_str, "TODO", True)

            for item in range(0, len(task_list)):
                if task_list[item][1] == True:
                    pass
                elif task_list[item][1] == False:
                    unfinished_task_list.append(task_list[item][0])
            
            db.readDatabase()
            time.sleep(0.1)
            js.resetBlockContent()
            time.sleep(0.1)
        except:
            continue


        # Create new TODO for tmr 
        db.createNewTODOforTmr(tomorrow_str,unfinished_task_list)
        # TODO: delet unfinished task of today????
        # ----------------------------------------

    time.sleep(30)
    # ----------------------------------------