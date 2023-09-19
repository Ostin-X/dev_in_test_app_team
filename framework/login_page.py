from selenium.common.exceptions import TimeoutException

from .page import Page


class LoginPage(Page):

    def find_hello_login_button(self):
        return self.find_element(by='id', value='com.ajaxsystems:id/authHelloLogin')

    def click_hello_login_button(self):
        try:
            hello_login_button = self.find_hello_login_button()
        except TimeoutException:
            pass
        else:
            self.click_element(hello_login_button)

    def find_email_input(self):
        email_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView[1]/android.widget.FrameLayout[1]/androidx.compose.ui.platform.ComposeView/android.view.View/android.widget.EditText'
        return self.find_element(by='xpath', value=email_xpath)

    def find_password_input(self):
        pass_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView[1]/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.widget.EditText'
        return self.find_element(by='xpath', value=pass_xpath)

    def find_login_button(self):
        return self.find_element(by='id', value='com.ajaxsystems:id/authLogin')

    def enter_email(self, email):
        email_input = self.find_email_input()
        self.send_keys_to_element(email_input, email)

    def enter_password(self, password):
        password_input = self.find_password_input()
        self.send_keys_to_element(password_input, password)

    def click_login_button(self):
        login_button = self.find_login_button()
        self.click_element(login_button)

    def check_invalid_reason(self):
        toast = self.find_element(by='id', value='com.ajaxsystems:id/snackbar_text')
        while toast.text == 'Зачекайте, триває синхронізація з сервером':
            toast = self.find_element(by='id', value='com.ajaxsystems:id/snackbar_text')
        return toast.text

    def check_valid_sidebar(self):
        try:
            menu = self.find_element(by='id', value='com.ajaxsystems:id/menuDrawer')
            self.click_element(menu)
            self.find_element(by='id', value='com.ajaxsystems:id/settings')
            return True
        except TimeoutException:
            return False

    def is_login_successful(self):
        try:
            reason = self.check_invalid_reason()
            return False, reason
        except TimeoutException:
            pass
        try:
            self.check_valid_sidebar()
            return True, None
        except TimeoutException:
            return False, None
