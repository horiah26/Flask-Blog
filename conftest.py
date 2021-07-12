import pytest
from flask import Flask
from app import create_app

@pytest.fixture()
def client():
    app = create_app()
    return app.test_client()