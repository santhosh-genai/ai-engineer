with open("C:\\Users\\2276038\\Desktop\\Learning\\classes\\report.txt", "w") as file:
        file.write("TestCase1 - Passed")
        file.write("\nTestCase2 - Failed")
        file.write("\nTestCase3 - Passed")

with open("C:\\Users\\2276038\\Desktop\\Learning\\classes\\report.txt", "a") as file:
        file.write("\nTestCase4 - Failed")
        file.write("\nTestCase5 - Passed")

with open("C:\\Users\\2276038\\Desktop\\Learning\\classes\\report.txt", "r") as file:
        content = file.read()
        print(content)
        passed_count = 0
        failed_count = 0
        for line in content.splitlines():
            if "Passed" in line:
                passed_count += 1
            else:
                failed_count += 1        
print(f"Total count - Passed: {passed_count}, Failed: {failed_count}")
print(file.name)
print(file.closed)  
print(file.mode)
