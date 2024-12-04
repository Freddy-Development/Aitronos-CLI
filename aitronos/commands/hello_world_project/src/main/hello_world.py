from resources import CurrentUser
import Aitronos


def main():
    current_user = CurrentUser()  # Initialize CurrentUser
    user = current_user.user  # Access the User object managed by CurrentUser
    assistant_messaging = Aitronos.Aitronos(api_key=user.user_token).AssistantMessaging  # Initialize Aitronos

    # create a nice welcome message with freddy
    payload = Aitronos.MessageRequestPayload(
        organization_id=1,
        assistant_id=1,
        # model="ftg-1.5",
        instructions="You are a funny person and you are the welcoming officer of the hello world project and you like to attach jokes to everything.",
        messages=[Aitronos.Message(content=f"Welcome this user {user.full_name} to the world, and provide a warm welcome message.",
                                   role="user")]
    )
    message = assistant_messaging.execute_run(payload=payload)

    return message


if __name__ == "__main__":
    print(main())