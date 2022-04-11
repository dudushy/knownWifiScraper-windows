# sourcery skip: convert-to-enumerate, for-append-to-extend, list-comprehension, move-assign-in-block, use-dict-items
# Imports
import subprocess
import os
import time

# Main
while True:
    # Clear screen
    os.system('cls')

    # Reset vars
    profiles = []
    passwords = {}
    count = 0

    # Grab all profiles (raw data)
    profiles_raw = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding="cp858")
    
    # Format profiles into list
    for line in profiles_raw.split("\n"):
        if "Profile     :" in line:
            profiles.append(line[(line.find(":")) + 2:])

    # Print info
    print(f"""
-----] Wifi Key Scraper [-----
| [!] ({len(profiles)}) Profiles found""")

    # Wait 1 seconds
    time.sleep(1)

    # Grab each key
    for profile in profiles:
        print(f'|\n| [! INIT] Profile: "{profile}"')
        # Try execute code
        try:
            password_raw = subprocess.check_output(["netsh", "wlan", "show", "profile", f'name={profile.replace(" ", "*")}', "key=clear"], shell=True, encoding="cp858")
            for line in password_raw.split("\n"):
                if "Key Content            :" in line:
                    passwords[f"profile{count + 1}"] = {
                        "status": "SUCESS",
                        "id": profile,
                        "password": line[(line.find(":")) + 2:]
                        }
                    print(f'|\n| [! DONE] Profile: "{profile}" // Password: "{line[(line.find(":")) + 2:]}"')
        # Set password to null if fail
        except Exception as e:
            print(f'|\n| [! ERROR] Profile: "{profile}" // FAIL')
            passwords[f"profile{count + 1}"] = {
                        "status": "ERROR",
                        "id": profile,
                        "password": "null"
                        }
        count += 1

    # Save output text
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        for item in passwords:
            file.write(f"[{item}/{passwords[item]['status']}] {passwords[item]['id']} <|> {passwords[item]['password']}\n")
        print("|\n| [!] 'output.txt' saved")
    
    # Repeat loop?
    if input("|\n-----] Execute again? (y/n) [-----\n>> ").lower() == "n":
        break

# End
os.system('pause')
