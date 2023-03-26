from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date

class Test_DemoClass:
    #her testten önce çağrılır
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        #günün tarihini al bu tarih ile bir klasör var mı kontrol et yoksa oluştur.
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)# bu klasör varsa oluşturma bunu kullan.

    #her testten sonra çağrılır.
    def teardown_method(self):
        self.driver.quit()
    # seup -> test_demoFunc -> teardown
    def test_demoFunc(self):
        #3A Act Arrange Assert
        text = "hello"
        assert text == "hello"
    # seup -> test_demo2 -> teardown
    def test_demo2(self):
        assert True

    @pytest.mark.parametrize("username,password",[("1","1"),("username","password")])
    def test_invalid_login(self,username,password):
        self.waitForElementVisible((By.ID,"user-name"))
        userNameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")
        userNameInput.send_keys(username)
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID, "login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{password}.png")
        assert errorMessage.text == "Epic sadface: Username and password do not match any user in this service"
    def waitForElementVisible(self,locator,timeout=5):
        #en fazla 5 saniye olacak şekilde user-name id'li elementin görünmesini bekle.
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located(locator))