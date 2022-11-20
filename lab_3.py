import unittest
from ddt import ddt, data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from string import ascii_lowercase
from random import choice
from enum import Enum


class ElementIdentifier(str, Enum):

    def __str__(self):
        return str(self.value)

    ACCOUNT_BUTTON_XPATH = '//*[@id="header"]/div/div[2]/div/a'
    LOGOUT_BUTTON_XPATH = '//*[@id="header-account"]/div/ul/li[5]/a'
    LINK_TO_LOGIN_PAGE_XPATH = '//*[@id="header-account"]/div/ul/li[6]/a'
    LOGIN_EMAIL_FORM_ID = 'email'
    LOGIN_PASSWORD_FORM_ID = 'pass'
    LOGIN_BUTTON_ID = 'send2'
    SEARCH_IN_STORE_FORM_ID = 'search'
    SEARCH_BUTTON_XPATH = '//*[@id="search_mini_form"]/div[1]/button'
    NO_PRODUCT_MSG_XPATH = '//*[@id="top"]/body/div/div[2]/div[2]/div/div[2]/div[1]/p'
    LINK_TO_MY_ACCOUNT_PAGE_XPATH = '//*[@id="header-account"]/div/ul/li[1]/a'
    CREATE_ACCOUNT_BUTTON_XPATH = '//*[@id="login-form"]/div/div[1]/div[2]/a'
    REGISTER_BUTTON_XPATH = '//div[2]/button'
    FIRSTNAME_FORM_ID = 'firstname'
    LASTNAME_FORM_ID = 'lastname'
    EMAIL_FORM_ID = 'email_address'
    PASSWORD_FORM_ID = 'password'
    PASSWORD_CONFIRMATION_FORM_ID = 'confirmation'
    USER_PAGE_TITLE_XPATH = '//h1'
    LINK_TO_HOME_PAGE_XPATH = '//*[@id="header"]/div/a'
    STORE_ITEM_LINK_XPATH = '//*[@id="top"]/body/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/ul/li[1]/a'
    STORE_ITEM_COLOR_BUTTON_ID = 'swatch27'
    STORE_ITEM_SIZE_BUTTON_ID = 'swatch76'
    ADD_TO_CART_BUTTON_XPATH = '//*[@id="product_addtocart_form"]/div[3]/div[6]/div[2]/div[2]/button'
    ADDED_TO_CART_MSG_XPATH = '//*[@id="top"]/body/div/div[2]/div[2]/div/div/div[2]/ul/li/ul/li/span'
    REMOVE_FROM_CART_BUTTON_XPATH = '//*[@id="shopping-cart-table"]/tbody/tr/td[6]/a'


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
        self.driver.find_element(By.XPATH, ElementIdentifier.ACCOUNT_BUTTON_XPATH).click()
        logout_btn = self.driver.find_element(By.XPATH, ElementIdentifier.LOGOUT_BUTTON_XPATH)
        if logout_btn.text == 'Log Out':
            logout_btn.click()

    def login(self, email, password):
        self.driver.find_element(By.XPATH, ElementIdentifier.ACCOUNT_BUTTON_XPATH).click()
        self.driver.find_element(By.XPATH, ElementIdentifier.LINK_TO_LOGIN_PAGE_XPATH).click()

        self.driver.find_element(By.ID, ElementIdentifier.LOGIN_EMAIL_FORM_ID).send_keys(email)
        self.driver.find_element(By.ID, ElementIdentifier.LOGIN_PASSWORD_FORM_ID).send_keys(password)
        self.driver.find_element(By.ID, ElementIdentifier.LOGIN_BUTTON_ID).click()

    @data('dresses', 'earrings', 'not_existing_product_group', 'shirts')
    def test_search_product_group(self, product_group: str):
        search_form = self.driver.find_element(By.ID, ElementIdentifier.SEARCH_IN_STORE_FORM_ID)
        search_form.send_keys(product_group)
        self.driver.find_element(By.XPATH, ElementIdentifier.SEARCH_BUTTON_XPATH).click()

        with self.assertRaises(NoSuchElementException, msg=f"{product_group} is not present in store catalog"):
            self.driver.find_element(By.XPATH, ElementIdentifier.NO_PRODUCT_MSG_XPATH)

    def test_user_registration_and_login(self):
        self.driver.find_element(By.XPATH, ElementIdentifier.ACCOUNT_BUTTON_XPATH).click()
        self.driver.find_element(By.XPATH, ElementIdentifier.LINK_TO_MY_ACCOUNT_PAGE_XPATH).click()
        self.driver.find_element(By.XPATH, ElementIdentifier.CREATE_ACCOUNT_BUTTON_XPATH).click()

        self.driver.find_element(By.ID, ElementIdentifier.FIRSTNAME_FORM_ID).send_keys(self.test_user['first_name'])
        self.driver.find_element(By.ID, ElementIdentifier.LASTNAME_FORM_ID).send_keys(self.test_user['last_name'])
        self.driver.find_element(By.ID, ElementIdentifier.EMAIL_FORM_ID).send_keys(self.test_user['email'])
        self.driver.find_element(By.ID, ElementIdentifier.PASSWORD_FORM_ID).send_keys(self.test_user['password'])
        self.driver.find_element(By.ID, ElementIdentifier.PASSWORD_CONFIRMATION_FORM_ID). \
            send_keys(self.test_user['password'])
        self.driver.find_element(By.XPATH, ElementIdentifier.REGISTER_BUTTON_XPATH).click()

        self.driver.find_element(By.XPATH, ElementIdentifier.ACCOUNT_BUTTON_XPATH).click()
        self.driver.find_element(By.XPATH, ElementIdentifier.LOGOUT_BUTTON_XPATH).click()
        self.login(self.test_user['email'], self.test_user['password'])

        user_page_title = self.driver.find_element(By.XPATH, ElementIdentifier.USER_PAGE_TITLE_XPATH).text

        self.assertEqual(user_page_title, 'MY DASHBOARD', msg='Log in failed')

    def test_adding_to_cart(self):
        self.login('some_test_email@gmail.com', 'ssssss')
        self.driver.find_element(By.XPATH, ElementIdentifier.LINK_TO_HOME_PAGE_XPATH).click()

        self.driver.find_element(By.XPATH, ElementIdentifier.STORE_ITEM_LINK_XPATH).click()
        self.driver.find_element(By.ID, ElementIdentifier.STORE_ITEM_COLOR_BUTTON_ID).click()
        self.driver.find_element(By.ID, ElementIdentifier.STORE_ITEM_SIZE_BUTTON_ID).click()
        self.driver.find_element(By.XPATH, ElementIdentifier.ADD_TO_CART_BUTTON_XPATH).click()

        added_to_cart_msg = self.driver.find_element(By.XPATH, ElementIdentifier.ADDED_TO_CART_MSG_XPATH).text
        self.driver.find_element(By.XPATH, ElementIdentifier.REMOVE_FROM_CART_BUTTON_XPATH).click()

        self.assertIn("was added to your shopping cart.", added_to_cart_msg)


if __name__ == "__main__":
    unittest.main()
