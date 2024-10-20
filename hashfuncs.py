import hashlib
import random
import string
import time
import matplotlib.pyplot as plt

def hashSHA256(input_string):
    # Create a hash object
    hash_object = hashlib.sha256()
    # Convert the input string to bytes
    input_string = input_string.encode('utf-8')
    # Update the hash object with the input string
    hash_object.update(input_string)
    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()
    return hex_dig

def hashSHA256_truncated(input_str, bits):
    if bits < 8 or bits > 50:
        raise ValueError("Bits should be between 8 and 50")
    # Hash the input string
    sha256_hash = hashlib.sha256(input_str.encode('utf-8')).digest()
    sha256_hash_bin = bin(int.from_bytes(sha256_hash, 'big'))[2:]
    # Truncate the hash to the specified number of bits
    truncated_hash = sha256_hash_bin[:bits]
    return truncated_hash

def collisionSHA256(string_length, bits_to_truncate_to):
    num_strings = 0
    # Generate random strings until a collision is found
    while True:
        # Generate two random strings
        string1 = ''.join(random.choices(string.ascii_letters, k=string_length))
        string2 = ''.join(random.choices(string.ascii_letters, k=string_length))
        num_strings += 2
        
        # Hash the strings
        hash1 = hashSHA256_truncated(string1, bits_to_truncate_to)
        hash2 = hashSHA256_truncated(string2, bits_to_truncate_to)
        # Check if the hashes are the same
        if hash1 == hash2:
            return string1, string2, hash1, hash2, num_strings


# Method to find a collision using the Birthday attack (Option ii)
def find_collision_birthday(num_bits):
    hash_dict = {}
    attempts = 0
    while True:
        attempts += 1
        m = str(random.random())  # Generate a random input
        h = hashSHA256_truncated(m, num_bits)
        if h in hash_dict and hash_dict[h] != m:
            return hash_dict[h], m, attempts
        hash_dict[h] = m

# Plotting
def plot_results(bit_sizes, times, inputs):
    # Plot 1: Digest size vs. Collision time
    plt.figure(1)
    plt.plot(bit_sizes, times, marker='o')
    plt.xlabel("Digest Size (bits)")
    plt.ylabel("Collision Time (seconds)")
    plt.title("Digest Size vs Collision Time")
    plt.grid(True)
    
    # Plot 2: Digest size vs. Number of inputs
    plt.figure(2)
    plt.plot(bit_sizes, inputs, marker='o')
    plt.xlabel("Digest Size (bits)")
    plt.ylabel("Number of Inputs")
    plt.title("Digest Size vs Number of Inputs")
    plt.grid(True)
    
    plt.show()

if __name__ == "__main__":
    # **********Task 1 (a)**********
    init_string = "Hey im in CSC 321, this hacking stuff is cool!"
    init_string_2 = "Hello guys I like going out to eat"
    print(f"TASK 1(a)\nHash of string '{init_string}' in hex is: {hashSHA256(init_string)}\n")
    print(f"Hash of string '{init_string_2}' in hex is: {hashSHA256(init_string_2)}\n")

    # **********Task 1 (b)**********
    # Hamming distance between two strings is 1 bit
    pairs = [("11010100", "11010101"), ("110101010010", "110101010011"), ("110101010", "110101011")]
    print("TASK 1(b)")
    for pair in pairs:
        hash1 = hashSHA256(pair[0])
        hash2 = hashSHA256(pair[1])
        print(f"Hash for '{pair[0]}': {hash1}")
        print(f"Hash for '{pair[1]}': {hash2}\n")

    # **********Task 1 (c)**********
    # Truncate the hash to a desired amount of bits
    print("TASK 1(c)")
    bits_to_truncate_to = 20
    print(f"Truncated hash of string '{init_string}' to {bits_to_truncate_to} bits: {hashSHA256_truncated(init_string, bits_to_truncate_to)}\n")
    
    # Find collisions with random strings given a string length and number of bits to truncate to
    string_length = 20
    start_time = time.time()
    output = collisionSHA256(string_length, bits_to_truncate_to)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to find collision: {elapsed_time} seconds")
    print(f"Number of strings generated: {output[4]}")
    print(f"Collision found between strings: {output[0], output[1]},\nand their hashes are: {output[2], output[3]} respectively\n")

    # (ii) approach using birthday problem finding two messages that arent the same given they hash to the same value
    times = []
    inputs = []
    bit_sizes = list(range(8, 51, 2))
    
    for bits in bit_sizes:
        start_time = time.time()
        # use the return values if needed
        _, _, num_inputs = find_collision_birthday(bits)  # Use birthday attack method
        end_time = time.time()
        
        collision_time = end_time - start_time
        times.append(collision_time)
        inputs.append(num_inputs)
        print(f"Bits: {bits}, Time: {collision_time}, Inputs: {num_inputs}")

    plot_results(bit_sizes, times, inputs)

    # (i) approach but takes too long
    # for i in range(34, 50, 2):
    #     start_time = time.time()
    #     output = collisionSHA256(string_length, i)
    #     end_time = time.time()
    #     elapsed_time = end_time - start_time
    #     print(f"Time taken to find collision with {i} bits: {elapsed_time} seconds")
    #     print(f"Number of strings generated: {output[4]}")