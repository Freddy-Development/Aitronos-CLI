# hello world execution script
from ...resources import CurrentUser


def main():
    user = CurrentUser()
    user_full_name = user.full_name
    text = f'###Hello, World! \n and a warm welcome to the ++stream line development** to you {user_full_name}'
    return text


if __name__ == '__main__':
    print(main())
