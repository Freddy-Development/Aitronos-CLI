from resources.current_user import CurrentUser


def main():
    current_user = CurrentUser()  # Initialize CurrentUser
    user = current_user.user  # Access the User object managed by CurrentUser
    user_full_name = user.full_name  # Retrieve the full name from the User object
    text = f'### Hello, World! \nAnd a warm welcome to the streamlined development to you, {user_full_name}'
    return text


if __name__ == '__main__':
    print(main())
