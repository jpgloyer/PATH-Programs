from getpass import getpass
from colorama import init
from termcolor import colored
import random

class MasterDatabase():
    def __init__(self, file_name):
        self.file_name = file_name
        self.Reference_Character_List = self.get_chars()
        self.max_key = int(len(self.Reference_Character_List)/2-1)
        self.message_list = self.message_list_generator()
        


    #Setter functions
    def input_master_password(self,pswd):
        self.master_password = pswd
        self.m_pw_vals, self.m_pw_key = self.get_vals_from_password(self.master_password)

    def input_personal_password(self,pswd):
        self.personal_password = pswd
        self.p_pw_vals, self.p_pw_key = self.get_vals_from_password(self.personal_password)

    def input_username(self, username):
        self.username = username

    def get_chars(self):
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
        Reference_Character_list = []
        for i in Character_List3:
            Reference_Character_list.append(i)
        for i in Character_List2:
            Reference_Character_list.append(i)
        for i in Character_List1:
            Reference_Character_list.append(i)
        Symbols = ['!','@','#','$','%','^','&','*','(',')','?',':',';']
        for i in Symbols:
            Reference_Character_list.append(i)
        for i in range(len(Reference_Character_list)):
            Reference_Character_list.append(Reference_Character_list[i])
        return Reference_Character_list

    def message_list_generator(self):
        '''
        file_name: string - name or path of a text file that will be turned into a list of characters
        Returns encrypted list of characters
        '''
        message_list = []
        file = open(self.file_name, 'r')
        end_of_file = False
        while not end_of_file: 
            # read by character
            character = file.read(1)         
            if not character:
                end_of_file = True
            #print(character)
            if character:
                message_list.append(chr(ord(character)))
        file.close()

        return message_list


    def get_vals_from_password(self, Password):
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
            if key > self.max_key:
                key = 1
        if key == 0:
            key = 1
        #print(key)
        return password_vals, key


    def char_input_output(self, input_char, key):
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
        length = len(self.Reference_Character_List) - 1
        #print(length)
        while i != -1:
            if input_char == self.Reference_Character_List[i]:
                index = i
                i = -1
            else:
                i+=1
            if i > length:
                i = -1
                return input_char
        return self.Reference_Character_List[index+key]

    def encrypt(self, doc_type, message_to_encrypt):
        '''
        doc_type: str = 'Master' or 'Personal'
        '''
        if doc_type == 'Master':
            key = self.m_pw_key
            password_values = self.m_pw_vals
        elif doc_type == 'Personal':
            key = self.p_pw_key
            password_values = self.p_pw_vals
        elif doc_type == 'Temp':
            key = self.temp_key
            password_values = self.temp_password_vals

        encrypted_message = []
        #Converts message string to encrypted_message list of characters
        for i in message_to_encrypt:
            encrypted_message.append(i)
        #print("Increase iterations and password length for more security")
        for k in range(key):
            for i in password_values:
                if i == 0:
                    #alter every character in message
                    for j in range(len(message_to_encrypt)):
                        encrypted_message[j] = self.char_input_output(encrypted_message[j], key)
                else:
                    for j in range(len(message_to_encrypt)):
                        if j % i == 0:
                            encrypted_message[j] = self.char_input_output(encrypted_message[j], key)        
        if doc_type == 'Master':
            self.master_encrypted_message = encrypted_message
        elif doc_type == 'Personal':
            self.personal_encrypted_message = encrypted_message
        
        
        return encrypted_message                  

    def decrypt(self, doc_type, encrypted_message):
        '''
        doc_type: string 'Master', 'Personal', or 'Temp'
        '''
        if doc_type == 'Master':
            key = self.m_pw_key
            password_values = self.m_pw_vals
        elif doc_type == 'Personal':
            key = self.p_pw_key
            password_values = self.p_pw_vals
        decrypted_message = []
        password_values.reverse()
        for i in encrypted_message:
            decrypted_message.append(i)
        #print("Increase iterations for more security")
        for k in range(key):
            for i in password_values:
                if i == 0:
                    for j in range(len(encrypted_message)):
                        decrypted_message[j] = self.char_input_output(decrypted_message[j], -key)
                        
                else:
                    for j in range(len(encrypted_message)):
                        if j % i == 0:
                            decrypted_message[j] = self.char_input_output(decrypted_message[j], -key)
        if doc_type == 'Master':
            self.decrypted_master_message = ('').join(decrypted_message)
        elif doc_type == 'Personal':
            self.decrypted_personal_message = ('').join(decrypted_message)
        return decrypted_message

    def randomize_password(self):
        new_password = ''
        length = 0
        number_index = -1
        #char_options = list(string.ascii_letters)
        #for i in string.punctuation:
        #    char_options.append(i)
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
                character = random.choice(self.Reference_Character_List)
                new_password = new_password + character
            elif i == number_index:
                character = random.choice(self.Reference_Character_List[0:9])
        
        return new_password

    def initialize_database(self):
        users = []
        default_user_data = "Website: Username: Password: "

        #Get number of users
        try:
            number_of_users = int(input("How many users?"))
        except:
            print("Enter a valid number")

        #Collect initial usernames
        for i in range(number_of_users):
            users.append(input(f"Username({i}):"))


        #encrypted_default_user_data will be inserted in every user's section
        self.temp_password_vals, self.temp_key = self.get_vals_from_password('Password')
        encrypted_default_user_data = ('').join(self.encrypt('Temp',default_user_data))

        unencrypted_document = ''
        unencrypted_document = unencrypted_document + "Preamble: " + input("Group name:") + '\n'
        counter = 1
        for i in users:
            unencrypted_document = unencrypted_document + i + f': {counter}\n'
            counter += 1
        for i in users:
            unencrypted_document = unencrypted_document + "2jg08#8h2g0**@)2hfwlWIGhlwenUHw3*\n" + encrypted_default_user_data + '\n'

        unencrypted_document = unencrypted_document[:-1]

        with open("OurPasswordsTest.txt",'w') as NewFile:
            NewFile.write(('').join(self.encrypt('Temp',unencrypted_document)))
        pass

    def split_file_information(self):
        self.file_sections = self.decrypted_master_message.split('\n2jg08#8h2g0**@)2hfwlWIGhlwenUHw3*\n')
        self.users = {}
        for line in self.file_sections[0].split('\n'):
            self.users[line.split(': ')[0]] = line.split(': ')[1]
        return self.file_sections,self.users

    #Personal Information Functions

    def make_personal_info_list(self):
        self.personal_info_list = []
        for i in self.decrypted_personal_message.split('\n'):
            self.personal_info_list.append(i)
        for i in range(len(self.personal_info_list)):
            self.personal_info_list[i] = self.personal_info_list[i].split(': ')
        return self.personal_info_list

    def save_changes(self):
        lines = []
        for i in self.personal_info_list:
            lines.append((': ').join(i))
        lines = ('\n').join(lines)
        encrypted_lines = ('').join(self.encrypt('Personal', lines))
        self.file_sections[int(self.users[self.username])] = encrypted_lines
        return encrypted_lines

    def reencrypt(self):
        unencrypted_string = self.file_sections[0]
        for i in self.file_sections[1:]:
            unencrypted_string = unencrypted_string + '\n2jg08#8h2g0**@)2hfwlWIGhlwenUHw3*\n'
            unencrypted_string = unencrypted_string + i
        with open('OurPasswords.txt','w') as UpdatedFile:
            UpdatedFile.write(('').join(self.encrypt('Master',unencrypted_string)))



if __name__ == '__main__':
    Database = MasterDatabase('OurPasswords.txt')
    Database.input_master_password('Password')
    Database.input_username('Pierce')
    Database.input_personal_password('Password')
    Database.decrypt('Master',Database.message_list_generator())
    print(Database.split_file_information())
    Database.decrypt('Personal',Database.file_sections[2])
    print(Database.decrypted_personal_message)
    print(Database.make_personal_info_list())
    Database.save_changes()
    print(Database.file_sections)