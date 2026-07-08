import hashlib
import os
import re
import secrets
import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(os.getenv("STREAMLIT_DB_PATH", Path(__file__).with_name("members.sqlite3")))
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()
    return f"{salt}${password_hash}"


def verify_password(password, saved_password):
    try:
        salt, expected_hash = saved_password.split("$", 1)
    except ValueError:
        return False

    actual_hash = hash_password(password, salt).split("$", 1)[1]
    return secrets.compare_digest(actual_hash, expected_hash)


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_members_email
            ON members(email)
            """
        )


def validate_member(username, password, password_confirm, name, email):
    username = username.strip().lower()
    name = name.strip()
    email = email.strip().lower()

    if not USERNAME_PATTERN.fullmatch(username):
        return False, "아이디는 영문, 숫자, 밑줄만 사용해 3~30자로 입력해주세요."
    if len(password) < 8:
        return False, "비밀번호는 8자 이상이어야 합니다."
    if password != password_confirm:
        return False, "비밀번호 확인이 일치하지 않습니다."
    if not name:
        return False, "이름을 입력해주세요."
    if not EMAIL_PATTERN.fullmatch(email):
        return False, "올바른 이메일을 입력해주세요."

    return True, ""


def create_member(username, password, password_confirm, name, email, phone=""):
    init_db()
    username = username.strip().lower()
    name = name.strip()
    email = email.strip().lower()
    phone = phone.strip()

    is_valid, error_message = validate_member(
        username,
        password,
        password_confirm,
        name,
        email,
    )
    if not is_valid:
        return None, error_message

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO members (
                    username,
                    password_hash,
                    name,
                    email,
                    phone,
                    role,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    hash_password(password),
                    name,
                    email,
                    phone,
                    "일반회원",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            member_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return None, "이미 사용 중인 아이디 또는 이메일입니다."

    return member_id, ""


def authenticate(username, password):
    init_db()
    username = username.strip().lower()
    with get_connection() as conn:
        member = conn.execute(
            "SELECT * FROM members WHERE username = ?",
            (username,),
        ).fetchone()

    if member is None:
        return None

    if not verify_password(password, member["password_hash"]):
        return None

    return dict(member)


def get_member_by_id(member_id):
    init_db()
    with get_connection() as conn:
        member = conn.execute(
            """
            SELECT id, username, name, email, phone, role, created_at
            FROM members
            WHERE id = ?
            """,
            (member_id,),
        ).fetchone()

    return dict(member) if member else None
