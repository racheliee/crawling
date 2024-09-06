from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# Define ChromeOptions
chrome_options = Options()

# Define ChromeDriver path
chrome_service = Service("/opt/homebrew/Caskroom/chromedriver/128.0.6613.119/chromedriver-mac-arm64/chromedriver")

# Initialize WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get("https://etk.srail.kr/cmc/01/selectLoginForm.do") # srt login page
driver.implicitly_wait(15) # wait for 15 seconds so that the page can load

# login
driver.find_element(By.ID, "srchDvNm01").send_keys("1234") # 회원번호
driver.find_element(By.ID, "hmpgPwdCphd01").send_keys("1234") # 비밀번호

# click login button
driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()

# move to reservation page
driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do") # srt reservation page
driver.implicitly_wait(5)

# 출발지 입력
dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
dep_stn.clear()
dep_stn.send_keys("동탄")

# 도착지 입력
arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
arr_stn.clear()
arr_stn.send_keys("수서")

# 출발 날짜
elm_dptDt = driver.find_element(By.ID, "dptDt")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
Select(driver.find_element(By.ID,"dptDt")).select_by_value("20240912")

# 출발 시간
elm_dptTm = driver.find_element(By.ID, "dptTm")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text("12")

# 조회하기 버튼 클릭
driver.find_element(By.XPATH,"//input[@value='조회하기']").click()
driver.implicitly_wait(5)

