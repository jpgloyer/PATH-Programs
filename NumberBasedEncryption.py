
import random


def get_chars_from_unencrypted_file(filename: str):
    end_of_file = False
    characters = []
    with open(filename) as Input:
        while not end_of_file:
            char = Input.read(1)
            if char:
                characters.append(char)
            elif not char:
                end_of_file = True
    return characters

def get_chars_from_encrypted_file(filename: str):
    end_of_file = False
    characters = []
    with open(filename) as Input:
        while not end_of_file:
            char = Input.read(1)
            if char:
                if char != '\n':
                    characters.append(char)
            elif not char:
                end_of_file = True
    return characters



def get_ascii_for_char_list(characters: list[str]):
    ascii_vals = []
    for i in characters:
        ascii_vals.append(ord(i))
    for i in range(len(ascii_vals)):
        if ascii_vals[i] < 10:
            ascii_vals[i] = [0,0,ascii_vals[i]]
        elif ascii_vals[i] > 9 and ascii_vals[i] < 100:
            ascii_vals[i] = [0,int(ascii_vals[i]/10),ascii_vals[i]%10]
        elif ascii_vals[i] > 99:
            ascii_vals[i] = [int(ascii_vals[i]/100),int((ascii_vals[i]%100)/10),ascii_vals[i]%10]
    return ascii_vals

def get_values_from_password(password: str):
    password_ascii = []
    for i in password:
        password_ascii.append(ord(i))
    #print(password_ascii)
    password_digits = []
    for i in password_ascii:
        for j in str(i):
            if int(j) != 0:
                password_digits.append(int(j))
    #print(password_digits)
    even_sum = 0
    odd_sum = 0
    for i in range(len(password_digits)):
        if i % 2 == 0:
            even_sum += password_digits[i]
        else:
            odd_sum += password_digits[i]
    iterations = ((even_sum*odd_sum)%100)+100
    return password_digits, iterations

def test_with_many_passwords():
    Character_List1 = [chr(i) for i in range(65,91)]
    Character_List2 = [chr(i) for i in range(97,123)]
    Character_List3 = [chr(i) for i in range(48,58)]
    reference_list = []
    for i in Character_List1:
        reference_list.append(i)
    for i in Character_List2:
        reference_list.append(i)
    for i in Character_List3:
        reference_list.append(i)
    
    # highest = 0
    # lowest = 200
    for i in reference_list:
        for j in reference_list:
            for k in reference_list:
                password = i+j+k
                # if get_values_from_password(password)[1] > highest:
                #     highest = get_values_from_password(password)[1]
                # if get_values_from_password(password)[1] < lowest:
                #     lowest = get_values_from_password(password)[1]


def add_x_to_list_vals(list: list[int], x: int):
    for i in range(len(list)):
        list[i] = list[i] + x
    return list

def pull_vals_from_2d_list(list: list[list[int]], index: int):
    vals = []
    for i in list:
        vals.append(i[index])
    return vals

def right_rotate(list: list[int], n: int):
    output_list = []
    x = len(list)

    for item in range(x-n, x):
        output_list.append(list[item])
    for item in range(0,x-n):
        output_list.append(list[item])
    return output_list

def left_rotate(list: list[int], n: int):
    output_list = []
    x = len(list)

    for item in range(n,x):
        output_list.append(list[item])
    for item in range(0,n):
        output_list.append(list[item])
    return output_list

def encryption_single_iteration(information: list[list[int]], j: int):
    temp_nums = []
    # Add value at index to list (j%3 = 1 -> [a,x,x][b,x,x][c,x,x] -> [a,b,c])
    for k in range(len(information)):
        temp_nums.append(information[k][j%3])
    # Add j to each value in temp list
    # (j%3 = 1 -> [a+1,b+1,c+1])
    # Modulo result by 10 to prevent overflow
    for k in range(len(temp_nums)):
        temp_nums[k] = (temp_nums[k] + j + 10)%10
    # Shift temp list right by j spaces
    temp_nums = right_rotate(temp_nums,j)
    # Re fill information with modified, rotated information
    # (j%3 = 1 -> [c+1,a+1,b+1] -> [c+1,x,x][a+1,x,x][b+1,x,x])
    for k in range(len(information)):
        information[k][j%3] = temp_nums[k]
    return information

def decryption_single_iteration(information: list[list[int]], j:int):
    temp_nums = []
    for k in range(len(information)):
        temp_nums.append(information[k][j%3])
    temp_nums = left_rotate(temp_nums,j)
    for k in range(len(temp_nums)):
        temp_nums[k] = (temp_nums[k] - j + 10)%10
    for k in range(len(information)):
        information[k][j%3] = temp_nums[k]
    return information
    


def encrypt(information: list[list[int]], password_values: list[int], iterations: int):
    for i in range(iterations):
        password_values = right_rotate(password_values,1)
        for j in password_values:
            # if j == 0:
            #     for k in range(len(information)):
            #         information[k] = right_rotate(information[k],1)
            # else:
            encryption_single_iteration(information,j)
    return information




def decrypt(information: list[list[int]], password_values: list[int], iterations: int):
    for i in range(iterations):
        password_values = right_rotate(password_values,1)
    for i in range(iterations):
        password_values = left_rotate(password_values,1)
        for j in password_values:
            # if j == 0:
            #     for k in range(len(information)):
            #         information[k] = left_rotate(information[k],1)
            # else:
            decryption_single_iteration(information,j)

    return information



#password_vals = []

def test_encryption():
    password_vals, iterations = get_values_from_password('Password')
    for k in range(0,1000):
        test = []
        for i in range(11):
            #password_vals.append(random.randint(0,9))
            test.append([])
            for j in range(0,3):
                test[i].append(random.randint(0,9))

        #print(test)
        encrypted_info = encrypt(test,password_vals, iterations)
        #print(encrypted_info)
        if decrypt(encrypted_info,password_vals,iterations) != test:
            print('ERROR')



characters = get_chars_from_unencrypted_file('testing.txt')
characters = get_ascii_for_char_list(characters)
password_vals, iterations = get_values_from_password('Password')
encrypted_info = encrypt(characters,password_vals,iterations)
with open('Encryptedtesting.txt','w') as Output:
    for i in encrypted_info:
        for j in i:
            Output.write(str(j))

encrypted_info = get_chars_from_unencrypted_file('Encryptedtesting.txt')
decrypted_info = decrypt(encrypted_info,password_vals,iterations)
for i in decrypted_info:
    print(chr(100*i[0] + 10*i[1] + i[2]),end='')