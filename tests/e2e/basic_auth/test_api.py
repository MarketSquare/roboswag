import secrets
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .. import run_e2e

app = FastAPI(title="RoboswagTestAPI")

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "testuser")
    correct_password = secrets.compare_digest(credentials.password, "1234pass")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me", operation_id="users_me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


def test_e2e():
    test_name = Path(__file__).parent.name
    run_e2e(app, test_name)
