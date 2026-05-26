passwords = ["123456", "admin", "password", "admin123"]

target = "admin123"

for i in passwords:
    print("Trying:", i)

    if i == target:
        print("Password Cracked:", i)
        break
