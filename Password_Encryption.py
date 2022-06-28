from getpass import getpass


def get_chars():
    #To be used once at the beginning of every run of the program
    #Simply generates a list of standard characters (numbers, lower and capital case letters)
    #Returns the completed list, doubled

    #Capital Letters
    Character_List1 = [chr(i) for i in range(65,91)]
    #Lower case letters
    Character_List2 = [chr(i) for i in range(97,123)]
    #Numbers
    Character_List3 = [chr(i) for i in range(48,58)]
    Full_Character_List = []
    for i in range(len(Character_List3)):
        Full_Character_List.append(Character_List3[i])
    for i in range(len(Character_List2)):
        Full_Character_List.append(Character_List2[i])
    for i in range(len(Character_List1)):
        Full_Character_List.append(Character_List1[i])
    Symbols = ['!','@','#','$','%','^','&','*','(',')','?',':',';']
    for i in Symbols:
        Full_Character_List.append(i)

    for i in range(len(Full_Character_List)):
        Full_Character_List.append(Full_Character_List[i])


    # for i in range(len(Int_Value_Of_Character)):
    #     print(Full_Character_List[i],end='')
    return Full_Character_List


def char_input_output(input_char, key, Character_List):
    #Takes in one input character that is searched for in the character list
    #Returns the position of the character in the list, shifted by the amount inputted as encryption_value
    index = 0
    i = 0
    length = len(Character_List) - 1
    #print(length)
    
    while i != -1:
        if input_char == Character_List[i]:
            index = i
            i = -1
        else:
            i+=1

        if i > length:
            i = -1
            return input_char

    return Character_List[index+key]


def message_list_generator(file_name):
    character_list = []
    file = open(file_name, 'r')
    end_of_file = False

    while not end_of_file: 
        # read by character
        character = file.read(1)         
        if not character:
            end_of_file = True
            

        #print(character)
        if character:
            character_list.append(chr(ord(character)))

    file.close()

    #print(character_list)
    #print()
    #print(encrypted_character_list)
    return character_list

def get_vals_from_password(Password, max_key):
    password_vals = []
    Letter_Nums = ''
    key = 0
    for i in range(len(Password)):   
        Letter_Nums = str(ord(Password[i]))
        for j in Letter_Nums:  
            password_vals.append(int(j))

    #Key creation
    #Code here doesn't really matter as long as the key is never allowed to be greater than the max_key. Everything else will produce the 
    #same result when used for encryption and decryption
    for i in password_vals:
        #print(password_vals[-1])
        if password_vals[0] != 0 and password_vals[-1] != 0:
            if i % password_vals[0] < 2 and i % password_vals[-1] < 2:
                key += i
        #key += i
        if key > max_key:
            key = 0
    #print(key)

    return password_vals, key

def encrypt(message, password_values, key, Character_Reference_List):
    encrypted_message = []
    #Converts message string to encrypted_message list of characters
    for i in message:
        encrypted_message.append(i)
    #print("Increase iterations and password length for more security")
    for k in range(key):
        for i in password_values:
            if i == 0:
                #alter every character in message
                for j in range(len(message)):
                    encrypted_message[j] = char_input_output(encrypted_message[j], key, Character_Reference_List)
                    

            else:
                for j in range(len(message)):
                    if j % i == 0:
                        encrypted_message[j] = char_input_output(encrypted_message[j], key, Character_Reference_List)
                        
    return encrypted_message
                    
                    
def decrypt(encrypted_message, password_values, key, Character_Reference_List):
    decrypted_message = []
    password_values.reverse()
    for i in encrypted_message:
        decrypted_message.append(i)
    #print("Increase iterations for more security")
    for k in range(key):
        for i in password_values:
            if i == 0:
                for j in range(len(encrypted_message)):
                    decrypted_message[j] = char_input_output(decrypted_message[j], -key, Character_Reference_List)
                    
            else:
                for j in range(len(encrypted_message)):
                    if j % i == 0:
                        decrypted_message[j] = char_input_output(decrypted_message[j], -key, Character_Reference_List)
                        
    return decrypted_message

    
    

def main():
    Character_Reference_List = get_chars()

    operation_choice = ''
    while operation_choice != 'encryption' and operation_choice != 'decryption' and operation_choice != 'Encryption' and operation_choice != 'Decryption' and operation_choice != 'E' and operation_choice != 'D' and operation_choice != 'e' and operation_choice != 'd':
        operation_choice = input("Encryption or decryption:")

    #print()

    if operation_choice == 'Encryption' or operation_choice == 'encryption' or operation_choice == 'E' or operation_choice == 'e':
        Password_Vals, key = get_vals_from_password(getpass("Password(remember for decryption):"), int(len(Character_Reference_List)/2-1))
        #print(Password_Vals)
        if key == 0:
            key = 1
        encrypted_message = encrypt(message_list_generator(input('Input file:')), Password_Vals, key, Character_Reference_List)
        with open((input("Enter output file name(no file extension):")+'.txt'), 'w') as f:
            for i in encrypted_message:
                f.write(i)

    elif operation_choice == 'Decryption' or operation_choice == 'decryption' or operation_choice =='D' or operation_choice == 'd':
        Input_Password_Vals, input_key = get_vals_from_password(getpass(), int(len(Character_Reference_List)/2-1))
        if input_key == 0:
            input_key = 1
        decrypted_message = decrypt(message_list_generator(input("Encrypted file name/path:")), Input_Password_Vals, input_key, Character_Reference_List)
        with open('Password_Encryption_Output.txt', 'w') as f:
            for i in decrypted_message:
                f.write(i)
        #print("Decrypted message located in Password_Encryption_Output.txt")

    #print()

if __name__ == "__main__":
    main()
    #ADD IN SYSTEM TO SHIFT CHARACTERS UPON EACH ITERATION OF THE ENCRYPTION(i.e. character in position 1 moves to position 2 after being altered, last character moves to position 1)