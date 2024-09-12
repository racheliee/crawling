from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

# Define ChromeOptions
chrome_options = Options()

# Define ChromeDriver path
chrome_service = Service("/opt/homebrew/Caskroom/chromedriver/128.0.6613.119/chromedriver-mac-arm64/chromedriver")

# Initialize WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get("https://etk.srail.kr/cmc/01/selectLoginForm.do") # srt login page
driver.implicitly_wait(15) # wait for 15 seconds so that the page can load

# variables
departure = "수서"
arrival = "부산"
date = "20240919"
depart_time = "12"
num_trains = 4

# login
with open("srt-credentials.txt", "r") as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
driver.find_element(By.ID, "srchDvNm01").send_keys(username) # 회원번호
driver.find_element(By.ID, "hmpgPwdCphd01").send_keys(password) # 비밀번호

# click login button
driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()

# move to reservation page
driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do") # srt reservation page
driver.implicitly_wait(5)

# 출발지 입력
dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
dep_stn.clear()
dep_stn.send_keys(departure)

# 도착지 입력
arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
arr_stn.clear()
arr_stn.send_keys(arrival)

# 출발 날짜
elm_dptDt = driver.find_element(By.ID, "dptDt")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
Select(driver.find_element(By.ID,"dptDt")).select_by_value(date)

# 출발 시간
elm_dptTm = driver.find_element(By.ID, "dptTm")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(depart_time)

# 조회하기 버튼 클릭
driver.find_element(By.XPATH,"//input[@value='조회하기']").click()
driver.implicitly_wait(5)

# 조회된 열차 리스트 선택
train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')

print(len(train_list)) # 결과: 10 (한 페이지에 10개의 열차 정보가 나옴)

for i in range(1, len(train_list)+1):
    for j in range(3, 8):
        text = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({j})").text.replace("\n"," ")
        print(text, end="")
    print()
    
# 원하는 조건의 열차 선택
for i in range(1, 3): # 첫 두개의 열차가 예약 가능한 열차인지 확인
    standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
    
    if "예약하기" in standard_seat:
        print("예약 가능")        
        driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span").click()


# 매진된 경우:
reserved = False

while True:
    for i in range(1, num_trains+1): # 상위 4개 기차 확인
        standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text

        if "예약하기" in standard_seat:
            print("예약 가능")       
            driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span").click()
            reserved = True
            break

    if not reserved:
        # 5초 기다리기
        time.sleep(5)
        
        # 다시 조회하기
        submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
        driver.execute_script("arguments[0].click();", submit)
        print("새로고침")

        driver.implicitly_wait(10)
        time.sleep(1)
    else:
        break