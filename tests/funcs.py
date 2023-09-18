import subprocess


def get_android_udid():
    try:
        output = subprocess.check_output(["adb", "devices"], universal_newlines=True)
        device_list = output.strip().split('\n')[1:]

        if device_list:
            first_device = device_list[0].split('\t')[0]
            return first_device
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def login_to_app(login_page, email, password):
    login_page.reset_app()
    login_page.click_hello_login_button()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_login_button()

    return login_page.is_login_successful()
