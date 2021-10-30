# Notion_OLED
Using notion API to retrieve daily tasks on OLED screen

### Current Demo
- youtube link

### Install step
1. install driver for OLED screen, "https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/README.md"
```
sudo python -m pip install --upgrade pip setuptools wheel
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
```
2. clone the current repository
```
git clone https://github.com/JAckZ97/Notion_OLED.git
```
3. create a txt file called "secret_key.txt", and put your notion token and database ID in first two lines
```
nano secret_key.txt
```
4. run the program
```
python3 notion.py
```

### TODO
- [x] Date title
- [x] Task page
- [x] Toggle in task page
- [x] Resetting page
- [x] Sub-task page content
- [x] POST to Notion database
- [ ] FIX toggle and bracket in sub-task page
- [ ] scroll bar in task page and sub-task page