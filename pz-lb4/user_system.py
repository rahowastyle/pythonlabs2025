import hashlib
from datetime import datetime

# class
class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)

    def get_details(self):
        return f"User: {self.username}, Active: {self.is_active}, Role: Base User"

# subclasses
class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions if permissions else []

    def get_details(self):
        return f"Admin: {self.username}, Permissions: {', '.join(self.permissions)}"

class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.last_login = None

    def login(self):
        self.last_login = datetime.now()
        print(f"Користувач {self.username} увійшов у систему о {self.last_login}")

    def get_details(self):
        return f"Regular User: {self.username}, Last Login: {self.last_login}"

class GuestUser(User):
    def __init__(self, username, password=""):
        super().__init__(username, password)
        self.access_level = "read_only"

    def get_details(self):
        return f"Guest: {self.username}, Access: {self.access_level}"

class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.username in self.users:
            print(f"Помилка: Користувач {user.username} вже існує.")
        else:
            self.users[user.username] = user
            print(f"Користувача {user.username} успішно додано.")

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        
        if user and user.verify_password(password):
            if user.is_active:
                print(f"Автентифікація успішна: {user.get_details()}")
                if isinstance(user, RegularUser):
                    user.login()
                return user
            else:
                print("Акаунт деактивовано.")
                return None
        else:
            print("Невірне ім'я користувача або пароль.")
            return None

if __name__ == "__main__":
    system = AccessControl()

    admin = Administrator("admin_max", "secure_pass_123", permissions=["all_access"])
    user1 = RegularUser("ivan_stepanenko", "userPass1")
    guest = GuestUser("guest_client")
  
    system.add_user(admin)
    system.add_user(user1)
    system.add_user(guest)
  
    #  тест входу
    print("\n--- Тест ---")
    
    auth_user = system.authenticate_user("admin_max", "secure_pass_123")

    auth_user2 = system.authenticate_user("ivan_stepanenko", "userPass1")

    system.authenticate_user("admin_max", "wrong_password")

    system.authenticate_user("ghost", "0000")
