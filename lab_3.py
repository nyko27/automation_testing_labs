import unittest
from ddt import ddt, data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from string import ascii_lowercase
from random import choice


@ddt
class StoreTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StoreTester, self).__init__(*args, **kwargs)
        self.test_user = {
            'first_name': 'test_user_first_name',
            'last_name': 'test_user_last_name',
            'email': f"{''.join(choice(ascii_lowercase) for i in range(10))}@gmail.com",
            'password': 'test_user_password',
        }

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.get("http://demo-store.seleniumacademy.com")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def tearDown(self):
        self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div[2]/div/a').click()
        logout_btn = self.driver.find_element(By.XPATH, '//*[@id="header-account"]/div/ul/li[5]/a')
        if logout_btn.text == 'Log Out':
            logout_btn.click()

    def login(self, email, password):
        self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div[2]/div/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="header-account"]/div/ul/li[6]/a').click()

        self.driver.find_element(By.ID, 'email').send_keys(email)
        self.driver.find_element(By.ID, 'pass').send_keys(password)
        self.driver.find_element(By.ID, 'send2').click()

    @data('dresses', 'earrings', 'not_existing_product_group', 'shirts')
    def test_search_product_group(self, product_group: str):
        search_form = self.driver.find_element(By.ID, 'search')
        search_form.send_keys(product_group)
        self.driver.find_element(By.XPATH, '//*[@id="search_mini_form"]/div[1]/button').click()

        with self.assertRaises(NoSuchElementException, msg=f"{product_group} is not present in store catalog"):
            self.driver.find_element(By.XPATH, '//*[@id="top"]/body/div/div[2]/div[2]/div/div[2]/div[1]/p')

    def test_user_registration_and_login(self):
        self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div[2]/div/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="header-account"]/div/ul/li[1]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div/div[1]/div[2]/a').click()

        self.driver.find_element(By.ID, 'firstname').send_keys(self.test_user['first_name'])
        self.driver.find_element(By.ID, 'lastname').send_keys(self.test_user['last_name'])
        self.driver.find_element(By.ID, 'email_address').send_keys(self.test_user['email'])
        self.driver.find_element(By.ID, 'password').send_keys(self.test_user['password'])
        self.driver.find_element(By.ID, 'confirmation').send_keys(self.test_user['password'])
        self.driver.find_element(By.XPATH, '//div[2]/button').click()

        self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div[2]/div/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="header-account"]/div/ul/li[5]/a').click()
        self.login(self.test_user['email'], self.test_user['password'])

        user_page_title = self.driver.find_element(By.XPATH, '//h1').text

        self.assertEqual(user_page_title, 'MY DASHBOARD', msg='Log in failed')

    def test_adding_to_cart(self):
        self.login('some_test_email@gmail.com', 'ssssss')
        self.driver.find_element(By.XPATH, '//*[@id="header"]/div/a').click()

        el_xpath = '//*[@id="top"]/body/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/ul/li[1]/a'
        self.driver.find_element(By.XPATH, el_xpath).click()
        self.driver.find_element(By.ID, 'swatch22').click()
        self.driver.find_element(By.ID, 'swatch80').click()

        el_xpath = '//*[@id="product_addtocart_form"]/div[3]/div[6]/div[2]/div[2]/button'
        self.driver.find_element(By.XPATH, el_xpath).click()

        el_xpath = '//*[@id="top"]/body/div/div[2]/div[2]/div/div/div[2]/ul/li/ul/li/span'
        added_to_cart_msg = self.driver.find_element(By.XPATH, el_xpath).text

        remove_from_cart_xpath = '//*[@id="shopping-cart-table"]/tbody/tr/td[6]/a'
        self.driver.find_element(By.XPATH, remove_from_cart_xpath).click()

        self.assertIn("was added to your shopping cart.", added_to_cart_msg)


if __name__ == "__main__":
    unittest.main()
