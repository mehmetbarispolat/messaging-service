import httpx

client = httpx.AsyncClient()


# User create an account and login.
def test_user_create_and_login():

    # Sign up
    register_resp = client.post(
        "localhost:8000/register/",
        json={
            "username": "test",
            "password": "test",
            "email": "test@gmail.com",
            "full_name": "test test",
        },
        headers={"content-type": "multipart/form-data"},
    )

    assert register_resp.status == 201
    # Login
    login_resp = client.post(
        "localhost:8000/login/",
        json={"username": "test", "password": "test"},
        headers={"content-type": "multipart/form-data"},
    )

    assert login_resp.status == 201
    assert login_resp.json()["content"].get("token", False)


# User message other user
def test_user_message_to_others_usernames():
    pass


# User display their own message history
def test_user_display_their_message_history():
    pass
