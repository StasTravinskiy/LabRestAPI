import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)


@patch("app.core.rate_limiter.r")
def test_anonymous_user_under_limit(mock_redis):
    """Кейс 1: Анонімний юзер ще не досяг ліміту - статус 200[cite: 1]"""
    # Мокаємо асинхронні методи Redis
    mock_redis.zremrangebyscore = AsyncMock()
    # Імітуємо, що це перший запит (ліміт не перевищено)
    mock_redis.zcard = AsyncMock(return_value=1)
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    response = client.get("/books/")

    assert response.status_code == 200
    assert response.json() == {"message": "Success", "data": ["Book 1", "Book 2"]}


@patch("app.core.rate_limiter.r")
def test_anonymous_user_over_limit(mock_redis):
    """Кейс 2: Анонімний юзер досяг ліміту - статус 429[cite: 1]"""
    mock_redis.zremrangebyscore = AsyncMock()
    # Імітуємо, що ліміт (2) вже досягнуто
    mock_redis.zcard = AsyncMock(return_value=2)
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    response = client.get("/books/")

    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"



@patch("app.core.rate_limiter.r")
def test_authenticated_user_under_limit(mock_redis):
    """Кейс 1: Авторизований юзер ще не досяг ліміту - статус 200[cite: 1]"""
    mock_redis.zremrangebyscore = AsyncMock()
    mock_redis.zcard = AsyncMock(return_value=5)
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    headers = {"Authorization": "Bearer secret_token"}
    response = client.get("/books/", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Success", "data": ["Book 1", "Book 2"]}


@patch("app.core.rate_limiter.r")
def test_authenticated_user_over_limit(mock_redis):
    """Кейс 2: Авторизований юзер досяг ліміту - статус 429[cite: 1]"""
    mock_redis.zremrangebyscore = AsyncMock()
    # Імітуємо 10 запитів (ліміт досягнуто)
    mock_redis.zcard = AsyncMock(return_value=10)
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    headers = {"Authorization": "Bearer secret_token"}
    response = client.get("/books/", headers=headers)

    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"