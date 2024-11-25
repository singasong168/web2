from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


url = "http://www.gench.edu.cn"
driver.get(url)
driver.maximize_window()

links = driver.find_elements("xpath", "//a[@href]")

for link in links:
    if "English" in link.get_attribute("innerHTML"):
        print(link)
        link.click()
        break


