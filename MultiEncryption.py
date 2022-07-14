from email import message
from getpass import getpass
from colorama import init
from termcolor import colored
import random

def get_chars():
    '''
    Simply generates a list of potential characters usable by the encryption and decryption functions
    Changing the list between encryption and decryption will prevent decryption from working properly, but
        if encryption and decryption are run using the same character list, it will work regardless of the list contents
    '''
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
    for i in Character_List3:
        Full_Character_List.append(i)
    for i in Character_List2:
        Full_Character_List.append(i)
    for i in Character_List1:
        Full_Character_List.append(i)
    Symbols = ['!','@','#','$','%','^','&','*','(',')','?',':',';']
    for i in Symbols:
        Full_Character_List.append(i)
    for i in range(len(Full_Character_List)):
        Full_Character_List.append(Full_Character_List[i])
    return Full_Character_List


def char_input_output(input_char, key, Character_List):
    '''
    input_char: character - character to be modified
    key: int - number of spaces to shift the character along the...
    character_list: list of characters - this list should contain every potential character twice (ie. [1,2,3,1,2,3])
        list is used to translate input characters to output characters
    '''
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
    '''
    file_name: string - name or path of a text file that will be turned into a list of characters
    '''
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
    '''
    password: string - user-inputted password to be used in the decryption/encryption processes
    max_key: integer - equal to int(len(get_chars())/2-1)
    ^^^ I don't know why I made this this way, but it's staying like this for a while probably. I might fix it someday
    '''
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
            key = 1
    if key == 0:
        key = 1
    #print(key)
    return password_vals, key

def encrypt(message, password_values, key, Character_Reference_List):
    '''
    message: string - data to be encrypted
    password_values: list of integers - generated from the get_vals_from_password() function
    key: integer - generated from the get_vals_from_password() function
    character_reference_list: list of characters - generated from the get_chars() function
    '''
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
    '''
    encrypted_message: string - data to be encrypted
    password_values: list of integers - generated from the get_vals_from_password() function
    key: integer - generated from the get_vals_from_password() function
    character_reference_list: list of characters - generated from the get_chars() function
    '''
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

def decrypt_password_list(Master_Password,message):
    password_values,key = get_vals_from_password(Master_Password,int(len(get_chars())/2-1))
    decrypted_lines_list = ('').join(decrypt(message,password_values,key,get_chars())).split(('\n'))
    for i in range(len(decrypted_lines_list)):
        decrypted_lines_list[i] = decrypted_lines_list[i].split(': ')
    return decrypted_lines_list

def encrypt_password_list(Master_Password,message):
    password_values,key = get_vals_from_password(Master_Password,int(len(get_chars())/2-1))
    encrypted_lines_list = ('').join(encrypt(message,password_values,key,get_chars()))
    return encrypted_lines_list

def randomize_password():
    new_password = ''
    length = 0
    number_index = -1
    #char_options = list(string.ascii_letters)
    #for i in string.punctuation:
    #    char_options.append(i)
    char_options = get_chars()
    while True:
        try:
            length = int(input('Enter preferred length:'))
            break
        except:
            print('Enter a valid number')
    if input("Is a number required?('YES'):") == 'YES':
        number_index = random.randint(0,length)

    for i in range(length):
        if i != number_index:
            character = random.choice(char_options)
            new_password = new_password + character
        elif i == number_index:
            character = random.choice(char_options[0:9])
    
    
    
    print('Your new password is: '+colored(str(new_password),'green'))
    return new_password

def initialize_database():
    users = []
    default_user_data = "WebsiteHere: UsernameHere: PasswordHere:"

    #Get number of users
    try:
        number_of_users = int(input("How many users?"))
    except:
        print("Enter a valid number")

    #Collect initial usernames
    for i in range(number_of_users):
        users.append(input(f"Username({i}):"))
    print("Default password for all users is 'Password'")

    #encrypted_default_user_data will be inserted in every user's section
    password_vals, key = get_vals_from_password('Password',int(len(get_chars())/2-1))
    encrypted_default_user_data = ('').join(encrypt(default_user_data,password_vals,key,get_chars()))

    unencrypted_document = ''
    unencrypted_document = unencrypted_document + "Preamble: " + input("Group name:") + '\n'
    counter = 1
    for i in users:
        unencrypted_document = unencrypted_document + i + f': {counter}\n'
        counter += 1
    for i in users:
        unencrypted_document = unencrypted_document + "2jg08#8h2g0**@)2hfwlWIGhlwenUHw3*\n" + encrypted_default_user_data + '\n'

    unencrypted_document = unencrypted_document[:-1]

    with open("OurPasswords.txt",'w') as NewFile:
        NewFile.write(('').join(encrypt(unencrypted_document,password_vals,key,get_chars())))


def reencrypt(file_sections,group_password):
    unencrypted_string = file_sections[0]
    for i in file_sections[1:]:
        unencrypted_string = unencrypted_string + '\n2jg08#8h2g0**@)2hfwlWIGhlwenUHw3*\n'
        unencrypted_string = unencrypted_string + i
    password_vals, key = get_vals_from_password(group_password,int(len(get_chars())/2-1))
    with open("OurPasswords.txt",'w') as UpdatedFile:
        UpdatedFile.write(('').join(encrypt(unencrypted_string,password_vals,key,get_chars())))


    


    

class PersonalInformation:
    def __init__(self,unencrypted_information,encryption_password):
        #2D lists by line and entry
        self.unencrypted_information = unencrypted_information
        self.encrypted_information = self.change_password(encryption_password)
        self.encryption_password = encryption_password
        self.actions = {"0": self.reveal, "1": self.add_entry, "2": self.change_entry_password, "3": self.remove_entry, "4": self.change_password}

    def menu(self):
        choice = ''
        while choice != 'q':
            print("0 - Reveal Password\n1 - Add Entry\n2 - Change Entry Password\n3 - Remove Entry\n4 - Change Personal Password")
            choice = input('Action ("q" to quit):')
            if choice == '0' or choice == '1' or choice == '2' or choice == '3' or choice == '4':
                self.actions.get(choice)()
    
    def reveal(self):
        print(''.ljust(5)+'Website:'.ljust(20) + 'Username:'.ljust(40))
        for i in range(len(self.unencrypted_information)):
            print(f'{i}:'.ljust(5) + f'{self.unencrypted_information[i][0]}'.ljust(20,'-') + f'{self.unencrypted_information[i][1]}'.ljust(40))
        password_choice = input('Select password number to reveal:')
        #print('-----------------------------------------')
        #Print entry info
        print('\n\n')
        print(f'Website:'.ljust(14) + f'{self.unencrypted_information[int(password_choice)][0]}'.ljust(30) + '\n'
            f'Username:'.ljust(15) + f'{self.unencrypted_information[int(password_choice)][1]}'.ljust(30) + '\n'
            +f'Password:'.ljust(14) + colored(f'{self.unencrypted_information[int(password_choice)][2]}'.ljust(30),color='red',attrs=['bold']))
        print('\n\n')

    def add_entry(self):
        password = ''
        confirmed_password = ' '
        website = (input('Website:')).upper()
        username = input('Username:')
        if input('Would you like to randomize this password(YES):') == 'YES':
            password = randomize_password()
            confirmed_password = password
        while password != confirmed_password:
            password = getpass('Password:')
            confirmed_password = getpass('Confirm password:')
        self.unencrypted_information.append([website,username,password])
        return self.unencrypted_information

    def change_entry_password(self):
        for i in range(len(self.unencrypted_information)):
            print(f'{i}:'.ljust(5) + f'{self.unencrypted_information[i][0]}'.ljust(20,'-') + f'{self.unencrypted_information[i][1]}'.ljust(40))

        password_choice = input('Select password number to change:')    
        print(self.unencrypted_information[int(password_choice)][0])
        new_password = ''
        new_confirmed_password = ' '
        if input('Would you like to randomize this password(YES):') == 'YES':
            new_password = randomize_password()
            new_confirmed_password = new_password
        while new_password != new_confirmed_password:
            new_password = getpass('New password:')
            new_confirmed_password = getpass('Confirm password:')
        self.unencrypted_information[int(password_choice)][2] = new_password 
        return self.unencrypted_information

    def remove_entry(self):
        unencrypted_information_new = []
        choice = '0'
        for i in range(len(self.unencrypted_information)):
            print(f'{i}:'.ljust(5) + f'{self.unencrypted_information[i][0]}'.ljust(20,'-') + f'{self.unencrypted_information[i][1]}'.ljust(40))
        #Input validation here
        choice = input('Select entry number to be removed (-1 to cancel):')
        for i in range(len(self.unencrypted_information)):
            if str(i) != choice:
                #print(i,choice)
                unencrypted_information_new.append(self.unencrypted_information[i])
        self.unencrypted_information = unencrypted_information_new
        return self.unencrypted_information

    def change_password(self,password=''):
        information_string = ''
        confirmed_password = ' '
        
        unencrypted_information_temp = []
        if password:
            confirmed_password = password
        for i in range(len(self.unencrypted_information)):
            unencrypted_information_temp.append((': ').join(self.unencrypted_information[i]))
        information_string = ('\n').join(unencrypted_information_temp)

        while password != confirmed_password:
            password = getpass('New password:')
            confirmed_password = getpass('Confirm password:')

        self.encryption_password = password
        password_values, key = get_vals_from_password(password,int(len(get_chars())/2-1))
        self.encrypted_information = encrypt(information_string,password_values,key,get_chars()) 
        self.encrypted_information = ('').join(self.encrypted_information).split('\n')
        return self.encrypted_information

    def save_changes(self):
        lines = []
        for i in self.unencrypted_information:
            lines.append((': ').join(i))
        lines = ('\n').join(lines)
        password_values, key = get_vals_from_password(self.encryption_password,int(len(get_chars())/2-1))
        encrypted_lines = encrypt(lines,password_values,key,get_chars())
        encrypted_lines = ('').join(encrypted_lines)
        return encrypted_lines




#--------------------------------------------------------------------------------------------------------------------------------------------
def multi_encrypt_main():
    #Decrypt a fully encoded file to allow individual, isolated user access
    Master_Password = getpass('Master Password:')
    Password_Vals, key = get_vals_from_password(Master_Password,int(len(get_chars())/2-1))
    master_decrypted_message = decrypt(message_list_generator('OurPasswords.txt'),Password_Vals,key,get_chars())
    #File sections includes an unencrypted preamble containing information about the organization and user section ownership, as well as a section dedicated to each users' encrypted password list
    file_sections = ('').join(master_decrypted_message).split('\n2jg08#8h2g0**@)2hfwlWIGhlwenUHw3*\n')

    #Create user dictionary from file preamble:
    users = {}
    for line in file_sections[0].split('\n'):
       users[line.split(': ')[0]] = line.split(': ')[1]

    #Personal decryption section
        #Username validation
    section_number = None
    while not section_number:
        try:    
            username = input('Username:')
            section_number = int(users[username])
        except:
            print('Invalid username')

    personal_password = getpass('Personal Password:')
    Password_Vals,key=get_vals_from_password(personal_password,int(len(get_chars())/2-1))
    Personal_Decrypted_Information = ('').join(decrypt(file_sections[section_number],Password_Vals,key,get_chars())).split('\n')
    
    for i in range(len(Personal_Decrypted_Information)):
        Personal_Decrypted_Information[i] = Personal_Decrypted_Information[i].split(': ')

    
    User = PersonalInformation(Personal_Decrypted_Information,personal_password)
    User.menu()
    file_sections[section_number] = User.save_changes()
    #for i in file_sections:
    #    print(i)

    reencrypt(file_sections,Master_Password)

if __name__ == "__main__":
    multi_encrypt_main()
    #initialize_database()
    #I desperately need to clean my s*** up