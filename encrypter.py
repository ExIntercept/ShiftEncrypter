import random
import numpy as np
import string

def convertBin(message):
    Bin = " ".join(format(ord(char), "08b") for char in message)
    return Bin

def shiftMatrix(matrix):
    shifted_matrix = []
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    for col in range(num_cols):
        shifted_col = []
        for row in range(num_rows):
            # Calculate the shifted index for the current column
            shifted_index = (col + row) % num_cols
            # Append the element at the shifted index in the current column
            shifted_col.append(matrix[row][shifted_index])
        # Append the shifted column to the shifted matrix
        shifted_matrix.append(shifted_col)
    return shifted_matrix

    
def packer(lis):
    list1 = []
    list2 = []
    a = 0
    for i in range(4):
        for j in range(4):
            if a < len(lis):
                list2.append(lis[a])
                a+=1
            else:
                list2.append("00000000")  # Pad with zeros
        list1.append(list2)
        list2 = []
    return list1

def unpacker(matrix):
    unpacked_list = []
    for row in matrix:
        for item in row:
            if item != "":
                unpacked_list.append(item)
    return unpacked_list
    
    
    
def encrypt(line):
    binary = convertBin(line)
    byteList = binary.split()
    a = len(byteList) / 16
    a = int(a + 1)
    b = 0
    c = 0
    
    rows = []
    for i in range(a):
        rows = packer(byteList[b:c])
        rows = shiftMatrix(rows)
        byteList[b:c] = unpacker(rows)
        b+=16
        c+=16
    stringf = ""
    for j in byteList:
        stringf += binary_to_char(j)
    return stringf            
    
def binary_to_char(binary):
    decimal = int(binary, 2)
    char = chr(decimal)
    return char


def makeKey():
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    shuffled_chars = list(chars)
    while any(shuffled_chars[i] == chars[i] for i in range(len(chars))):
        random.shuffle(shuffled_chars)
    return ''.join(shuffled_chars)
        

def unSubstitute(keyS, text):
    key = [k for k in keyS]
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    decypheredText = ""
    for i in text:
        try:
            r = key.index(i)
            decypheredText += chars[r]
        except ValueError:
            # Skip characters not present in the key
            pass
    return decypheredText


def substitute(keyS, text):
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    key = [k for k in keyS]
    # Filter out characters from text that are not present in chars
    text = ''.join(c for c in text if c in chars)
    r = 0
    subText = ""
    for i in text:
        r = chars.index(i)
        subText += key[r]
    return subText

    

lineBinary = ""
eLineBinary = ""
key = makeKey()
with open('key.txt', 'w') as keyFile:
    keyFile.write('key = "{}"'.format(key))

# Encrypt the contents of 'toEncrypt.txt' and write the encrypted content to 'encrypted.txt'
with open('toEncrypt.txt', 'r') as unencryptedFile:
    with open('encrypted.txt', 'w') as encryptedFile:  # Open in write mode ('w') to clear the file
        for line in unencryptedFile:
            line = substitute(key, line)
            eLineBinary = encrypt(line)
            encryptedFile.write(eLineBinary + '\n')
