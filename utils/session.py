current_user = None

def login(user_data):
    global current_user
    current_user = user_data

def logout():
    global current_user
    current_user = None

def get_user():
    return current_user

def is_logged_in():
    return current_user is not None

def is_admin():
    if current_user is None:
        return False
    return current_user["role"] == "Admin"

def is_alumni():
    if current_user is None:
        return False
    return current_user["role"] == "Alumni"

# ==========================================
# Selected Alumni (Admin)
# ==========================================

selected_alumni = None


def set_selected_alumni(user):

    global selected_alumni

    selected_alumni = user


def get_selected_alumni():

    return selected_alumni