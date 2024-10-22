import bcrypt
import time
from nltk.corpus import words


# get all the words between 6 and 10 letters long from the word corpus
word_list = [word for word in words.words() if 6 <= len(word) <= 10]

def parse_shadow_entry(entry):
    user, bcrypt_string = entry.split(':')
    algo, work_factor, salt_hash = bcrypt_string.split('$')[1:4]
    salt = salt_hash[:22]  # First 22 chars are the salt
    hash_value = salt_hash[22:]
    return user, algo, int(work_factor), salt, hash_value

def crack_password(user, work_factor, salt, hash_value, word_list):
    # Prepare the salt for comparison, dynamically using the work factor
    bcrypt_salt = f"$2b${work_factor:02}${salt}".encode('utf-8')  # Use the correct cost factor
    for word in word_list:
        # Hash the word with the extracted salt
        hashed = bcrypt.hashpw(word.encode('utf-8'), bcrypt_salt)
        # Compare the generated hash with the full original bcrypt hash
        if hashed.decode('utf-8') == f"$2b${work_factor:02}${salt}{hash_value}":
            return word
    return None


# Read shadow file (replace with actual file path)
shadow_file = """
               Bilbo:$2b$08$L.z8uq99JkFAvX/Q1jGRI.TzrHIIxWMoRi/VzO1sj/UvVFPgW8dW.
               Gandalf:$2b$08$J9FW66ZdPI2nrIMcOxFYI.q2PW6mqALUl2/uFvV9OFNPmHGNPa6YC 
               Thorin:$2b$08$J9FW66ZdPI2nrIMcOxFYI.6B7jUcPdnqJz4tIUwKBu8lNMs5NdT9q
               Fili:$2b$09$M9xNRFBDn0pUkPKIVCSBzuwNDDNTMWlvn7lezPr8IwVUsJbys3YZm
               Kili:$2b$09$M9xNRFBDn0pUkPKIVCSBzuPD2bsU1q8yZPlgSdQXIBILSMCbdE4Im
               Balin:$2b$10$xGKjb94iwmlth954hEaw3O3YmtDO/mEFLIO0a0xLK1vL79LA73Gom
               Dwalin:$2b$10$xGKjb94iwmlth954hEaw3OFxNMF64erUqDNj6TMMKVDcsETsKK5be
               Oin:$2b$10$xGKjb94iwmlth954hEaw3OcXR2H2PRHCgo98mjS11UIrVZLKxyABK
               Gloin:$2b$11$/8UByex2ktrWATZOBLZ0DuAXTQl4mWX1hfSjliCvFfGH7w1tX5/3q
               Dori:$2b$11$/8UByex2ktrWATZOBLZ0Dub5AmZeqtn7kv/3NCWBrDaRCFahGYyiq
               Nori:$2b$11$/8UByex2ktrWATZOBLZ0DuER3Ee1GdP6f30TVIXoEhvhQDwghaU12
               Ori:$2b$12$rMeWZtAVcGHLEiDNeKCz8OiERmh0dh8AiNcf7ON3O3P0GWTABKh0O
               Bifur:$2b$12$rMeWZtAVcGHLEiDNeKCz8OMoFL0k33O8Lcq33f6AznAZ/cL1LAOyK
               Bofur:$2b$12$rMeWZtAVcGHLEiDNeKCz8Ose2KNe821.l2h5eLffzWoP01DlQb72O
               Durin:$2b$13$6ypcazOOkUT/a7EwMuIjH.qbdqmHPDAC9B5c37RT9gEw18BX6FOay
               """
entries = shadow_file.strip().splitlines()

# Crack each user's password and measure time
for entry in entries:
    user, algo, work_factor, salt, hash_value = parse_shadow_entry(entry.strip())
    print(f"Cracking password for {user}...")
    print("algo is " , algo)
    print("work_factor is " , work_factor)
    print("salt is " , salt)
    print("hash_value is " , hash_value)
    start_time = time.time()
    password = crack_password(user, work_factor, salt, hash_value, word_list)
    end_time = time.time()

    if password:
        print(f"Password for {user}: {password} (Time taken: {end_time - start_time:.2f} seconds)")
    else:
        print(f"Password for {user} not found")
