def namelist(**kargs):

    print("namelist function called with arguments:", kargs)
    print("type of kargs:", type(kargs))
    for key,value in kargs.items():
        print(f"{key}: {value}")

namelist(name1="Alice", name2="Bob", name3="Charlie")