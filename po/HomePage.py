from SeleniumWrapper import SeleniumWrapper as wrapper
import LoginPage

locators = {
    "sign in link": "id=M_M_M_H_H_hlkLogIn"
}

class HomePage(object):
    def get_keyword_names(self):
        return ['open_english_home_page', 'navigate_to_sign_in_page']

    def open_english_home_page(self):
        se = wrapper().connection
        se.open("/Common/HomePage.aspx?lang=EN")
        se.wait_for_page_to_load("20000")
        
    def navigate_to_sign_in_page(self):
        se = wrapper().connection
        se.click(locators["sign in link"])
        se.wait_for_page_to_load("20000")