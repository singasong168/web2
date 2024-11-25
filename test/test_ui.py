import time
import unittest
import random
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class UserInterfaceTestCase(unittest.TestCase):


    def setUp(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.client = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        # self.client=webdriver.Chrome()
        if not self.client:
            self.skipTest("Chrome not available")


    def tearDown(self):
        if self.client:
            self.client.quit()






    def test_index(self):
        self.client.get("http://127.0.0.1:5011")
        time.sleep(2)
        self.assertIn("Let's refill", self.client.page_source)


    def login(self):
        self.client.get("http://127.0.0.1:5011")
        links = self.client.find_elements("xpath", "//a[contains(@href,'login')]")
        links[0].click()
        time.sleep(2)
        self.client.find_element(by=By.NAME, value="email").send_keys("aaa@qq.com")
        time.sleep(1)
        self.client.find_element(by=By.NAME, value="password").send_keys("1234")
        time.sleep(1)
        self.client.find_element(by=By.ID, value="submit").click()
        time.sleep(1)

    def test_login(self):
        self.client.get("http://127.0.0.1:5011")
        links = self.client.find_elements("xpath", "//a[contains(@href,'login')]")
        links[0].click()
        time.sleep(2)
        self.client.find_element(by=By.NAME, value="email").send_keys("aaa@qq.com")
        time.sleep(1)
        self.client.find_element(by=By.NAME, value="password").send_keys("1234")
        time.sleep(1)
        self.client.find_element(by=By.ID, value="submit").click()
        time.sleep(3)
        self.assertIn("logout", self.client.page_source)

    def test_login_fail(self):
        links = self.client.find_elements("xpath", "//a[contains(@href,'logout')]")
        if links:
            links[0].click()

        time.sleep(2)
        self.client.get("http://127.0.0.1:5011/login")
        time.sleep(2)
        self.client.find_element(by=By.NAME, value="email").send_keys("aaa@qq.com")
        time.sleep(1)
        self.client.find_element(by=By.NAME, value="password").send_keys("124")
        time.sleep(1)
        self.client.find_element(by=By.ID, value="submit").click()
        time.sleep(3)
        self.assertIn("Unsuccess", self.client.page_source)


    def test_add_to_cart(self):
        self.login()
        self.client.get("http://127.0.0.1:5011/cart")
        time.sleep(2)
        before_total=self.client.find_element(by=By.ID, value="subtotal").get_attribute("innerText")
        print(f"before_total:{before_total}")
        product_link = self.client.find_elements("xpath", "//a[contains(@href,'products')]")
        product_link[0].click()
        time.sleep(2)
        add_link = self.client.find_elements("xpath", "//a[contains(@href,'addToCart')]")
        add_link[randint(0,3)].click()
        time.sleep(2)
        self.client.get("http://127.0.0.1:5011/cart")
        time.sleep(4)
        after_total = self.client.find_element(by=By.ID, value="subtotal").get_attribute("innerText")
        print(f"after_total:{after_total}")
        time.sleep(1)
        self.assertNotEqual(before_total, after_total)

if __name__ == "__main__":
    unittest.main()
