password = "openAI123"
for attempt in range(3):
    user_input = input("Enter the password: ")
    if user_input == password:
        print("Access Granted")
        break
    elif attempt == 3 - 1: # Last attempt
        print("Access Denied")
    else:
        print("Incorrect password. Try again.")