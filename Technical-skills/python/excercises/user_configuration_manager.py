# Project 1 : User Configuration Manager
'''
Build a User Configuration Manager
In this lab, you will build a User Configuration Manager that allows users to manage their settings such as theme, 
language, and notifications. You will implement functions to add, update, delete, and view user settings.

Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

You should define a function named add_setting with two parameters representing a dictionary of settings and 
a tuple containing a key-value pair

add_setting function should:

Convert the key and value to lowercase.
If the key setting exists, return Setting '[key]' already exists! Cannot add a new setting with this name.
If the key setting doesn't exist, add the key-value pair to the given dictionary of settings and return Setting '[key]' a
dded with value '[value]' successfully!.
The messages returned should have the key and value in lowercase.
You should define a function named update_setting with two parameters representing a dictionary of settings and 
a tuple containing a key-value pair.

update_setting function should:

Convert the key and value to lowercase.
If the key setting exists, update its value in the given dictionary of settings and return: Setting '[key]' 
updated to '[value]' successfully!
If the key setting doesn't exist, return Setting '[key]' does not exist! Cannot update a non-existing setting.
The messages returned should have the key and value in lowercase.
You should define a function named delete_setting with two parameters representing a dictionary of settings and a key.

delete_setting function should:

Convert the key passed to lowercase.
If the key setting exists, remove the key-value pair from the given dictionary of settings and return Setting '[key]' deleted successfully!
If the key setting does not exist, return Setting not found!
The messages returned should have the key in lowercase.
You should define a function named view_settings with one parameter representing a dictionary of settings.

view_settings function should:

Return No settings available. if the given dictionary of settings is empty.
If the dictionary contains any settings, return a string displaying the settings. 
The string should start with Current User Settings: followed by the key-value pairs, each on a new line and with the key capitalized. 
For example, view_settings({'theme': 'dark', 'notifications': 'enabled', 'volume': 'high'}) should return:
Current User Settings:
Theme: dark
Notifications: enabled
Volume: high

For testing the code, you should create a dictionary named test_settings to store some user configuration preferences.
'''

def add_setting(settings: dict, setting: tuple):
    key, value = setting
    key, value = key.lower(), value.lower()

    if key in settings:
        return f"Setting '{key}' already exists! Cannot add a new setting with this name."
    settings[key] = value
    return f"Setting '{key}' added with value '{value}' successfully!"

def update_setting(settings: dict, setting: tuple):
    key, value = setting
    key, value = key.lower(), value.lower()

    if key in settings:
        settings[key] = value
        return f"Setting '{key}' updated to '{value}' successfully!"
    return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

def delete_setting(settings: dict, key):
    key = key.lower()

    if key in settings:
        del settings[key]
        return f"Setting '{key}' deleted successfully!"
    return "Setting not found!"

def view_settings(settings: dict):
    if not settings:
        return "No settings available."
    result = "Current User Settings:\n"
    for key,value in settings.items():
        result += f"{key.capitalize()}: {value}\n"
    return result

# Create test_settings dictionary
test_settings = {
    "theme": "dark",
    "language": "english",
    "notifications": "enabled"
}

#print("Initial settings:")
#print(view_settings(test_settings))

# Test add_setting
#print(add_setting(test_settings, ("Volume", "High")))
#print(view_settings(test_settings))

# Try adding an existing setting
#print(add_setting(test_settings, ("THEME", "Light")))

# Test update_setting
#print(update_setting(test_settings, ("Theme", "Light")))
#print(view_settings(test_settings))

# Try updating a non-existing setting
#print(update_setting(test_settings, ("Font", "Large")))

# Test delete_setting
#print(delete_setting(test_settings, "Notifications"))
#print(view_settings(test_settings))

# Try deleting a non-existing setting
#print(delete_setting(test_settings, "Brightness"))

# Delete remaining settings to test empty dictionary
#delete_setting(test_settings, "theme")
#delete_setting(test_settings, "language")
#delete_setting(test_settings, "volume")

#print(view_settings(test_settings))

