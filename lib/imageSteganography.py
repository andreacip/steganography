"""
This module implements the writing functionality of
text in an image and its decoding
"""
from PIL import Image


term_char = '1111111' # binary ASCII string terminator

class colors:
    WARNING = "\033[93m" # yellow
    SUCCESS = "\033[92m" # green
    MESSAGE = "\033[94m" # blue
    RESET = "\033[0m" # default color


def openImage():
    """
    Create pillow Image from given path.
    
        Return:
            img: Pillow Image
    """

    while True:
        img_path = input(">> please insert your image path: ")
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            print(f"{colors.WARNING}[ERROR]{colors.RESET}: path not valid")
            continue
        else:
            break
    return img



def saveImage(img):
    """
    Asks the user for the name of image
    and saves it with the selected extension.

        Parameters:
            img : Pillow Image  
    """

    formats = """
    plese select one of the following format:

    1. PNG          
    2. GIF      
    3. BITMAP      
    """
    saved_msg = f"{colors.SUCCESS}image correctly saved!{colors.RESET}"

    img_name = input("\n>> name of output image with no extension: ")
    print(formats)

    while True:
        selected = input(">> ")
        if selected == '1':
            img.save(img_name + '.png')
        elif selected == '2':
            img.save(img_name + '.bmp')
        elif selected == '3':
            img.save(img_name + '.tif')
        elif selected == 'esc':
            break
        else:
            print(f"{colors.WARNING}[WARNING]{colors.RESET}: format selected not valid, plese select valid format:")
            continue
        break

    print(saved_msg)



def stringToBinaryASCII(string):
    """
    Convert string in binary ascii code (7 bit for char).
    ex: "ciao mondo" --> "110010011919911199991..."

        Parameters:
            string (str): string to covert
        Returns:
            bin_string (str): string converted in sequence of binary ASCII code 
    """
    asci_arr = [ord(c) for c in string]
    bin_string = ''

    for el in asci_arr:
        bin_value = format(el, 'b')

        if len(bin_value) == 7:
            bin_string += bin_value
        else:
            while len(bin_value) < 7:
                bin_value = '0' + bin_value
            bin_string += bin_value

    return bin_string



def binaryToStringASCII(string):
    """
    Convert binary string to redable string.
    ex: "110010011919911199991..." --> "ciao mondo!"

        Parameters:
            string (str): string to convert
    """
    decoded_string = ""

    # legge la stringa 7 bit per volta
    for i in range(0, len(string), 7):
        decoded_string += (chr(int(string[i:i+7], 2)))
    return decoded_string



def modifyPixel(img, bin_msg):
        """
        Create an array with new pixels value to write.

            Parameters:
                img: pillow Image
                bin_msg: the binary message to write

        """
        pixels = img.getdata() 
        new_pixels = []

        for i in range(0, len(bin_msg)):
            # convert red pixel value in binary number
            bin_pixel = format(pixels[i][0], 'b')
            # modifies the least significant bit 
            int_bin_pxls = int(bin_pixel[:-1] + bin_msg[i], 2)

            # add to 
            new_pixels.append((int_bin_pxls, pixels[i][1], pixels[i][2]))

        return new_pixels



def encodeMessageInImage():
    """Decode message in image"""
    img = openImage()
    # get the message to write
    msg = input(">> your message: ")
    # convert the message in binary string 
    # and add the terminator charapter
    bin_message = stringToBinaryASCII(msg) + term_char

    new_pixels = modifyPixel(img, bin_message)
    pxl_iter = [0, 0]

    for pixel in new_pixels:
        img.putpixel((pxl_iter[0], pxl_iter[1]), pixel)
        if (pxl_iter[0] == img.width - 1):
            pxl_iter[1] += 1
            pxl_iter[0] = 0
        else:
            pxl_iter[0] += 1

    saveImage(img)



def decodeMessageInImage():
    """
    Decodes written text into an image.
    The decode end with the message terminator charapter
    """
    msg_bin = ""
    img = openImage()
    pxl = img.getdata() 

    pxl_range = [0, 7]
    
    while True:
        binary_char = ''
        for i in range(pxl_range[0], pxl_range[1]):
            value = format(pxl[i][0], 'b')
            binary_char += value[-1]
        if binary_char == term_char:
            break
        else:
            msg_bin += binary_char
            pxl_range[0] += 7
            pxl_range[1] += 7
    
    msg = binaryToStringASCII(msg_bin)
    print(f">> message: {colors.MESSAGE}{msg}{colors.RESET}")

