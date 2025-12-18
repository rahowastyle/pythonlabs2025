import pytest
from user_system import User, Administrator, RegularUser, GuestUser, AccessControl

@pytest.fixture
def system():
    return AccessControl()

def test_user_hashing_and_verification():
    user = User("test_user", "secret123")
    
    assert user.password_hash != "secret123"
    assert user.verify_password("secret123") is True

def test_user_wrong_password():
    user = User("test_user", "secret123")
    assert user.verify_password("wrong_pass") is False

def test_add_user_success(system):
    admin = Administrator("admin", "123")
    system.add_user(admin)
    
    assert "admin" in system.users
    assert system.users["admin"] == admin

def test_add_duplicate_user(system, capsys):
    user1 = User("login", "pass1")
    user2 = User("login", "pass2")
    
    system.add_user(user1)
    system.add_user(user2) # Спроба додати дублікат

    stored_user = system.users["login"]
    assert stored_user.verify_password("pass1") is True
    assert stored_user.verify_password("pass2") is False

def test_auth_success(system):
    user = RegularUser("ivan", "pass")
    system.add_user(user)
    
    result = system.authenticate_user("ivan", "pass")
    assert result == user
    assert result.username == "ivan"

def test_auth_wrong_password(system):
    user = GuestUser("guest", "pass")
    system.add_user(user)
    
    result = system.authenticate_user("guest", "wrong")
    assert result is None

def test_auth_user_not_found(system):
    result = system.authenticate_user("ghost", "0000")
    assert result is None

def test_auth_inactive_user(system):
    banned = User("banned", "123", is_active=False)
    system.add_user(banned)
    
    result = system.authenticate_user("banned", "123")
    assert result is None

def test_regular_user_login_timestamp(system):
    user = RegularUser("ivan", "pass")
    system.add_user(user)
    assert user.last_login is None # До входу часу немає
    system.authenticate_user("ivan", "pass")
    assert user.last_login is not None # Після входу час з'явився
