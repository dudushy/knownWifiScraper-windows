#imports
import subprocess
import os
import time

#main
while True:
    os.system('cls')
    # reset vars
    profiles = []
    passwords = {}
    count = 0

    # grab all profiles (raw data)
    profiles_raw = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding="cp858")
    
    # format profiles into list
    for line in profiles_raw.split("\n"):
        if "Profile     :" in line:
            profiles.append(line[(line.find(":")) + 2:])

    # print info
    print(f"""
-----] Wifi Key Scraper [-----
| [!] ({len(profiles)}) Profiles found""")
    # wait 1s
    time.sleep(1)

    # grab each key
    for profile in profiles:
        print(f'|\n| [! INIT] Profile: {profile}')
        # try execute code
        try:
            password_raw = subprocess.check_output(["netsh", "wlan", "show", "profile", f'name="{profile}"', "key=clear"], encoding="cp858")
            for line in password_raw.split("\n"):
                if "Key Content            :" in line:
                    passwords[f"profile{count}"] = {
                        "status": "SUCESS",
                        "id": profile,
                        "password": line[(line.find(":")) + 2:]
                        }
                    print(f'|\n| [! DONE] Profile: {profile} // Password: {line[(line.find(":")) + 2:]}')
        # set password to null if fail
        except Exception as e:
            print(f'|\n| [! ERROR] Profile: {profile} // FAIL')
            passwords[f"profile{count}"] = {
                        "status": "ERROR",
                        "id": profile,
                        "password": "null"
                        }
        count += 1

    # save output text
    with open("output.txt", "w") as file:
        for item in passwords:
            file.write(f"[{item}/{passwords[item]['status']}] {passwords[item]['id']}: {passwords[item]['password']}\n")
        print("|\n| [!] 'output.txt' saved")
    
    # repeat loop?
    if input("|\n-----] Execute again? (y/n) [-----\n>> ") == "n":
        break

#end
os.system('pause')

