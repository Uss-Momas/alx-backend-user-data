#!/usr/bin/env python3
"""main module
"""
import requests

URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """register_user function test"""
    payload = {"email": email, "password": password}
    r = requests.post(f"{URL}/users", data=payload)
    # print(r.json(), r.status_code)
    assert r.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """log_in_wrong_password function"""
    payload = {"email": email, "password": password}
    r = requests.post(f"{URL}/sessions", data=payload)
    # print(r.text, r.status_code)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """log_in function test"""
    payload = {"email": email, "password": password}
    r = requests.post(f"{URL}/sessions", data=payload)
    # print(r.json(), r.headers)
    assert r.status_code == 200
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    """get profile while unlogged"""
    r = requests.get(f"{URL}/profile")
    # print(r.text, r.status_code)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """profile_logged get profile while logged"""
    r = requests.get(f"{URL}/profile", cookies={"session_id": session_id})
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """log_out function test"""
    r = requests.delete(f"{URL}/sessions", cookies={'session_id': session_id})
    # print("Logout ", r.text, "status", r.status_code, r.cookies)
    assert r.history[0].status_code == 302


def reset_password_token(email: str) -> str:
    """reset_password_token function test"""
    r = requests.post(f"{URL}/reset_password", data={"email": email})
    assert r.status_code == 200
    return r.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update_password function test"""
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    r = requests.put(f"{URL}/reset_password", data=payload)
    assert r.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
