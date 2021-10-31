# Notion_OLED
Using notion API to retrieve daily tasks on OLED screen

### Current Demo
- youtube link

### Install step
0. Enable your I2C Interface:
- Enable I2C Interface on the Raspberry Pi:  
"https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/"
- Using an I2C OLED Display Module with the Raspberry Pi:  
"https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/"
1. Install driver for OLED screen:  
"https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/README.md"
```
sudo python -m pip install --upgrade pip setuptools wheel
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
```
2. Clone the current repository
```
git clone https://github.com/JAckZ97/Notion_OLED.git
```
3. Create a txt file called "secret_key.txt", and put your notion token and database ID in first two lines
```
nano secret_key.txt
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example like following:
```
secret_neSXGaJ1YP2q0hsNOjxxxxxxxxxxxxxxxxxxxxxxxxx
9bc98e7cba3a46539xxxxxxxxxxxxxxx
```
4. Run the program
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
- [ ] Fix toggle and bracket in sub-task page
- [ ] Scroll bar in task page and sub-task page