import random
import numpy as np
import string

def convertBin(message):
    Bin = " ".join(format(ord(char), "08b") for char in message)
    return Bin


def decrypt(line):
    binary = convertBin(line)
    byteList = binary.split()
    a = len(byteList) / 16
    a = int(a + 1)
    b = 0
    c = 0
    
    rows = []
    for i in range(a):
        rows = packer(byteList[b:c])
        rows = unshiftMatrix(rows)  # Unshift the matrix
        byteList[b:c] = unpacker(rows)
        b += 16
        c += 16
    stringf = ""
    for j in byteList:
        stringf += binary_to_char(j)
    return stringf

def unshiftMatrix(matrix):
    unshifted_matrix = []
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    for col in range(num_cols):
        unshifted_col = []
        for row in range(num_rows):
            # Calculate the unshifted index for the current column
            unshifted_index = (col - row) % num_cols
            # Append the element at the unshifted index in the current column
            unshifted_col.append(matrix[row][unshifted_index])
        # Append the unshifted column to the unshifted matrix
        unshifted_matrix.append(unshifted_col)

    return unshifted_matrix

    
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
            unpacked_list.append(item)
    return unpacked_list


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

def binary_to_char(binary):
    decimal = int(binary, 2)
    char = chr(decimal)
    return char
def readKeyFromFile():
    with open('key.txt', 'r') as keyFile:
        keyLine = keyFile.readline().strip()
        start_quote = keyLine.find('"') + 1
        end_quote = keyLine.rfind('"')
        key = keyLine[start_quote:end_quote]
        return key

def decrypt_file(key):
    print("Using key:", key)
    decrypted_lines = []
    with open('encrypted.txt', 'r') as encrypted_file:
        for line in encrypted_file:
            decrypted_line = decrypt(line.strip())
            decrypted_lines.append(decrypted_line)
    # Remove padding before un-substituting characters
    decrypted_text = ''.join(decrypted_lines).replace("00000000", "")
    decrypted_text = unSubstitute(key, decrypted_text)
    with open('decrypted.txt', 'w') as decrypted_file:
        if decrypted_text:
            decrypted_file.write(decrypted_text)




key = readKeyFromFile()
print("Read key from file:", key)
decrypt_file(key)

