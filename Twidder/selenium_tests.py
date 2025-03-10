from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import random
import unittest

class SeleniumTests(unittest.TestCase):

    def setUp(self):
        base_url = "http://127.0.0.1:5000/"
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(base_url)

        self.test_user = {
            'email': f'TestUser{random.randint(1, 100000000)}@example.com',
            'password': 'password',
            'repeatpassword': 'password',
            'firstname': 'Sara',
            'familyname': 'Kim',
            'gender': 'Female',
            'city': 'Linkoping',
            'country': 'Sweden'
        }

        self.test_user_2 = {
            'email': f'TestUser{random.randint(1, 100000000)}@example.com',
            'password': 'password',
            'repeatpassword': 'password',
            'firstname': 'Sunny',
            'familyname': 'Lee',
            'gender': 'Male',
            'city': 'Linkoping',
            'country': 'Sweden'
        }

        self.unmatched_password_user = {
            'email': f'TestUser{random.randint(1, 100000000)}@example.com',
            'password': 'password',
            'repeatpassword': 'password1111',
            'firstname': 'twidder',
            'familyname': 'app',
            'gender': 'Female',
            'city': 'Linkoping',
            'country': 'Sweden'
        }

    def tearDown(self):
        if self.driver:
            self.driver.quit()
    
    def try_sign_up(self, user_info):
        self.driver.find_element(By.ID, "firstname").send_keys(user_info['firstname'])
        self.driver.find_element(By.ID, "familyname").send_keys(user_info['familyname'])
        gender_select = Select(self.driver.find_element(By.NAME, 'gender'))
        gender_select.select_by_value(user_info['gender'])
        self.driver.find_element(By.ID, "city").send_keys(user_info['city'])
        self.driver.find_element(By.ID, "country").send_keys(user_info['country'])
        self.driver.find_element(By.ID, "email_signup").send_keys(user_info['email'])
        self.driver.find_element(By.ID, "password_signup").send_keys(user_info['password'])
        self.driver.find_element(By.ID, "repeatPSW").send_keys(user_info['repeatpassword'])
        
        self.driver.find_element(By.ID, "signupbtn").click()

    def try_sign_out(self):
        self.driver.find_element(By.ID, "account").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "signoutbtn").click()

    def try_sign_in(self, email, password):
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "submit").click()        

    # Sign up
    def test_1_signup_with_unmatched_passwords(self):
        try:
            print("[Test 1] Test SignUp with unmatched passwords")
            self.try_sign_up(self.unmatched_password_user)
            time.sleep(2)

            error_message = self.driver.find_element(By.ID, "error_message").text
            self.assertEqual(error_message, "Your passwords must be the same.")
            print("[Test 1] passed ✅")

        except AssertionError as ae:
            print("[Test 1] failed: ❌ {ae}")

    # Home Tab
    def test_2(self):
        try:
            print("[Test 2] Test Successful signUp")

            # Try Sign Up with valid information
            self.try_sign_up(self.test_user)
            time.sleep(2)

            # Check if we can see the information of user after signUp
            self.assertEqual(self.driver.find_element(By.ID, "firstname_info").text, self.test_user['firstname'])
            self.assertEqual(self.driver.find_element(By.ID, "familyname_info").text, self.test_user['familyname'])
            self.assertEqual(self.driver.find_element(By.ID, "gender_info").text, self.test_user['gender'])
            self.assertEqual(self.driver.find_element(By.ID, "city_info").text, self.test_user['city'])
            self.assertEqual(self.driver.find_element(By.ID, "country_info").text, self.test_user['country'])
            self.assertEqual(self.driver.find_element(By.ID, "email_info").text, self.test_user['email'])

            print("[Test 2] passed ✅")

        except AssertionError as ae:
            print("[Test 2] failed: ❌ {ae}")

    # Sign In
    def test_3(self):
        try:
            print("[Test 3] Test Sign In")
            
            # Sign Up & Sign Out -> welcome view
            self.try_sign_up(self.test_user)
            time.sleep(2)
            self.try_sign_out()
            time.sleep(2)

            # Try Sign in with wrong info
            self.try_sign_in("wrong_email@example.com", self.test_user['password'])
            time.sleep(2)

            # Test if the error message is correct!
            error_message = self.driver.find_element(By.ID, "login_error_message").text
            self.assertEqual(error_message, "The entered username does not exist! Please try again!")            
            print("[Test 3] passed ✅")

        except AssertionError as ae:
            print("[Test 3] failed: ❌ {ae}")

    # Search other user
    def test_4(self):
        try:
            print("[Test 4] Test Search User that doesn't exist")
            
            # Sign Up & Sign Out
            self.try_sign_up(self.test_user)
            time.sleep(1)   

            # Try to search user that doesn't exist
            self.driver.find_element(By.ID, "browse").click()   
            self.driver.find_element(By.ID, "useremail").send_keys(self.test_user_2['email'])
            self.driver.find_element(By.ID, "searchuserbtn").click()     
            time.sleep(1)       

            # Test if the error message is correct!
            error_message = self.driver.find_element(By.ID, "search_error").text
            self.assertEqual(error_message, "We can't get such userdata.")            
            print("[Test 4] passed ✅")

        except AssertionError as ae:
            print("[Test 4] failed: ❌ {ae}")

    # Post message
    def test_5(self):
        try:
            print("[Test 5] Test Post message")
            
            # Sign Up & Sign Out
            self.try_sign_up(self.test_user)
            time.sleep(1)
            self.try_sign_out()
            time.sleep(1)

            # Sign Up another user
            self.try_sign_up(self.test_user_2)
            time.sleep(1)

            # Search other user
            self.driver.find_element(By.ID, "browse").click()   
            self.driver.find_element(By.ID, "useremail").send_keys(self.test_user['email'])
            self.driver.find_element(By.ID, "searchuserbtn").click()     
            time.sleep(1)       

            # Post message to other user
            self.driver.find_element(By.ID, "post_msg_content_to_other").send_keys("Hello! Nice to meet you:)")
            self.driver.find_element(By.ID, "postmsgbtn_to_other").click()            
            time.sleep(1)
            
            # Test the message when posting succeeds
            self.assertEqual(self.driver.find_element(By.ID, "post_error_message_to_other").text, "Message Posted")

            # Press the renew button
            self.driver.find_element(By.ID, "renewbtn_browse").click()  
            time.sleep(1)

            # Test if the message is posted correctly!
            message_container = self.driver.find_element(By.ID, "message_container")
            message = message_container.find_elements(By.TAG_NAME, "div")
            self.assertEqual(message[0].text, self.test_user_2['email'] + ": Hello! Nice to meet you:)")
            print("[Test 5] passed ✅")

        except AssertionError as ae:
            print("[Test 5] failed: ❌ {ae}")

    # Change password
    def test_6(self):
        try:
            print("[Test 6] Change password")
            
            # Sign Up
            self.try_sign_up(self.test_user)
            time.sleep(1)

            # Press Account Tab
            self.driver.find_element(By.ID, "account").click()   
            time.sleep(1)

            # Change password with unmatched new passwords
            new_password = "newpassword"
            self.driver.find_element(By.ID, "currentpsw").send_keys(self.test_user['password'])
            self.driver.find_element(By.ID, "changepsw").send_keys(new_password)
            self.driver.find_element(By.ID, "repeatchangepsw").send_keys("wrong_password")
            self.driver.find_element(By.ID, "changepswbtn").click()              
            time.sleep(1)
            self.assertEqual(self.driver.find_element(By.ID, "changepsw_error").text, "Your passwords must be the same.")

            # Clear the fields
            self.driver.find_element(By.ID, "currentpsw").clear()
            self.driver.find_element(By.ID, "changepsw").clear()
            self.driver.find_element(By.ID, "repeatchangepsw").clear()
            time.sleep(1)

            # Change password with matched new passwords
            self.driver.find_element(By.ID, "currentpsw").send_keys(self.test_user['password'])
            self.driver.find_element(By.ID, "changepsw").send_keys(new_password)
            self.driver.find_element(By.ID, "repeatchangepsw").send_keys(new_password)
            self.driver.find_element(By.ID, "changepswbtn").click()              
            time.sleep(1)
            self.assertEqual(self.driver.find_element(By.ID, "changepsw_error").text, "Password is changed!")

            # Press the change button one more time after password is changed
            self.driver.find_element(By.ID, "changepswbtn").click()              
            time.sleep(1)
            self.assertEqual(self.driver.find_element(By.ID, "changepsw_error").text, "Incorrect password. Please try again.")            

            print("[Test 6] passed ✅")

        except AssertionError as ae:
            print("[Test 6] failed: ❌ {ae}")

if __name__ == '__main__':
    unittest.main()
