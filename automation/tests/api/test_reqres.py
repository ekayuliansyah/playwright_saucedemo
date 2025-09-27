from __future__ import annotations
import httpx
import pytest
from utils.schema import (ReqresLoginSuccess, ReqresLoginError, ReqresListUsers, ReqresCreateUser)

pytestmark = pytest.mark.api

UNAUTH = {401, 403, 429}

def _xfail_if_blocked(resp: httpx.Response, endpoint: str):
    if resp.status_code in UNAUTH:
        pytest.xfail(f"Reqres blocked/rate-limited ({resp.status_code}) at {endpoint}")

def test_login_success(base_url_api):
    url = f"{base_url_api}api/login"
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    r = httpx.post(url, json=payload, timeout=10)
    _xfail_if_blocked(r, "POST /api/login")
    assert r.status_code == 200
    ReqresLoginSuccess.model_validate(r.json())

def test_login_failure(base_url_api):
    url = f"{base_url_api}api/login"
    payload = {"email": "peter@klaven"}
    r = httpx.post(url, json=payload, timeout=10)
    _xfail_if_blocked(r, "POST /api/login (failure)")
    assert r.status_code == 400
    ReqresLoginError.model_validate(r.json())

def test_list_users_schema(base_url_api):
    url = f"{base_url_api}api/users?page=2"
    r = httpx.get(url, timeout=10)
    _xfail_if_blocked(r, "GET /api/users?page=2")
    assert r.status_code == 200
    data = ReqresListUsers.model_validate(r.json())
    assert len(data.data) > 0

def test_create_and_delete_user(base_url_api):
    create_url = f"{base_url_api}api/users"
    r = httpx.post(create_url, json={"name": "QA Bot", "job": "Tester"}, timeout=10)
    _xfail_if_blocked(r, "POST /api/users")
    assert r.status_code == 201
    created = ReqresCreateUser.model_validate(r.json())

    del_url = f"{base_url_api}api/users/{created.id}"
    r2 = httpx.delete(del_url, timeout=10)
    _xfail_if_blocked(r2, f"DELETE /api/users/{created.id}")
    assert r2.status_code == 204
