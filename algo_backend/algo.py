import math
import random
import numpy as np
from random import randint
import base64

dimensions = 10

# Generate keys
def generate_keys(n=10):
    # Generate private key
    flag = True
    while flag:
        privateB=np.identity(n)
        for i in range(n):
            privateB[i][i] = randint(2, 10)

        det = np.linalg.det(privateB)
        if det != 0:
            flag = False
            print("Done")
            
    ratio = hamdamard_ratio(privateB,n)
    print("Ratio: ",ratio)
    print("Private Key: ")
    print(privateB)

    unimodular_matrix, uni_upper, uni_lower = generate_unimodular_matrix(n)
    print("Unimodular Matrix: \n",unimodular_matrix)

    # Generate public key
    publicB = np.dot(unimodular_matrix,privateB)
    # ratio = hamdamard_ratio(publicB,n)
    # print("Ratio: ",ratio)
    print("Uni Inverse: ")
    print(uni_upper)
    print(uni_lower)

    # uni_inv = np.matmul(np.linalg.inv(uni_inv[1]),np.linalg.inv(uni_inv[0]))
    print("Public Key: ")
    print(publicB)

    return [privateB, publicB, unimodular_matrix, uni_upper,uni_lower]



# Generate unimodular matrix
def generate_unimodular_matrix(n):
    random_matrix = [ [np.random.randint(-10,10,) for _ in range(n) ] for _ in range(n) ]
    upperTri = np.triu(random_matrix,0)
    lowerTri = random_matrix - upperTri

    for i in range(n):
        val = randint(0,1)
        if val == 1:
            upperTri[i][i] = 1
        else:
            upperTri[i][i] = -1
        val = randint(0,1)
        if val == 1:
            lowerTri[i][i] = 1
        else:
            lowerTri[i][i] = -1


    unimodular_matrix = np.dot(upperTri,lowerTri)

    return [unimodular_matrix,upperTri,lowerTri]


# Add noise to ciphertext
def add_noise(cyphertext):
    noise = np.random.randint(-1,1,cyphertext.shape)
    cyphertext = cyphertext + noise
    return cyphertext

def divide_to_blocks(plaintext,dimensions):
    blocks = []
    for i in range(0,len(plaintext),dimensions):
        blocks.append(plaintext[i:i+dimensions])
    if blocks[-1] != dimensions:
        blocks[-1] = blocks[-1] + "#"*(dimensions-len(blocks[-1]))
    return blocks

def convert_to_ascii(blocks):
    ascii = []
    for block in blocks:
        print(block)
        ascii.append([ord(char) for char in block])
    return ascii


def array_to_base64_string(array):
    # Convert the NumPy array to bytes
    byte_string = array.tobytes()

    # Encode the byte string to base64
    base64_string = base64.b64encode(byte_string).decode('utf-8')
    return base64_string

def base64_string_to_array(base64_string, dtype, shape):
    # Decode the base64 string to bytes
    byte_string = base64.b64decode(base64_string)

    # Convert the byte string back to a NumPy array
    array = np.frombuffer(byte_string, dtype=dtype).reshape(shape)
    return array

# Encrypt plaintext using public key
def encrypt(plaintext,public_key):

    blocks = divide_to_blocks(plaintext,dimensions)

    ascii = convert_to_ascii(blocks)
    encoded_plain_text = np.array(ascii)

    cyphertext = np.matmul(encoded_plain_text,public_key)
    print("\n\nEncoded ciphertext\n",cyphertext)

    cyphertext = add_noise(cyphertext)
    print("\nNoisy cyphertext\n",cyphertext)

    # val = array_to_base64_string(cyphertext)
    # print(cyphertext.dtype,cyphertext.shape)

    return np.array(cyphertext)
    
def ascii_to_string(blocks):
    print(blocks)
    string = ""
    try:
        string += "".join([chr(char) for char in blocks])
        return string.rstrip("#")
    except:
        return string


# Decrypt ciphertext using private key
def decrypt(cyphertext,private_key,uni_inv_upper,uni_inv_lower):
    # Decode base64 string to NumPy array
    print(len(cyphertext))
    print("Decoded cyphertext\n",cyphertext)



    # uni = np.matmul(uni_inv_lower,uni_inv_upper)
    uni_inv = np.matmul(np.linalg.inv(uni_inv_lower),np.linalg.inv(uni_inv_upper))
    result = ""
    
    for i in range(0,len(cyphertext),dimensions):
        decrypted = remove_noise(cyphertext[i:i+dimensions],private_key)
        decrypted = np.matmul(decrypted,uni_inv)
        decrypted = np.round(decrypted).astype(int)
        print("Decrypted\n",decrypted)

        result += ascii_to_string(decrypted)

    print("Result: ",result)
    return result

def decrypt_with_pub_key(cyphertext,public_key):
    # Decode base64 string to NumPy array
    cyphertext = base64_string_to_array(cyphertext, np.float64, (3, dimensions))
    print("Decoded cyphertext\n",cyphertext)

    decrypted = remove_noise(cyphertext,public_key)

    decrypted = np.round(decrypted).astype(int)
    print("Decrypted\n",decrypted)

    # result = ascii_to_string(decrypted)
    # print("Result: ",result)
    # return result

# Calculate Hamdamard ratio
def hamdamard_ratio(basis,dimension):
    detOfLattice = np.linalg.det(basis)
    mult=1
    for v in basis:
        mult = mult * np.linalg.norm(v)#(np.sqrt((v.dot(v))))
    hratio = (detOfLattice / mult) ** (1.0/dimension)
    return hratio

# Babais algo to remove noise
def remove_noise(cyphertext,private_key):
    res = np.matmul(cyphertext,np.linalg.inv(private_key))
    print("real num comb\n",res)

    res = np.round(res).astype(int)
    print("rounded num comb\n",res)

    return res



# if __name__ == "__main__":
#     plaintext = "Hello I am Siddhartha"

#     # Generate a public and private key
#     keys = generate_keys(dimensions)


#     encryptedtext = encrypt(plaintext,keys[1])
#     print("Encrypted text: ",encryptedtext)


#     decryptedtext = decrypt(encryptedtext,keys[0],keys[3],keys[4])
#     print("Decrypted text: ",decryptedtext)
#     print("\n\n\n\n")

#     decryptedtext = decrypt_with_pub_key(encryptedtext,keys[1])
#     print("Decrypted text: ",decryptedtext)

