import lib.imageSteganography  as IS


welcome_msg = """
*********** STEGANOGRAPHY PRIVATE MESSAGE ****************

Welcome to steganography private message program, you can
do the the following things:

    1. Write text in image 
    2. Decode text in image
    3. write text in video
    4. decode text in video

enter esc to close the program

"""

def main():
    print(welcome_msg)
    choice = ""

    while choice not in ("1", "2", "3", "4", "esc"):
        choice = input(">> ")

    if choice == "1":
        IS.encodeMessageInImage()

    elif choice == "2":
        IS.decodeMessageInImage()

    elif choice == "3":
        print("sorry this functionaly is not already implemented")

    elif choice == "4":
        print("sorry this functionaly is not already implemented")


if __name__ == "__main__":
    main()