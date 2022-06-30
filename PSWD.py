from getpass import getpass

from rsa import verify
import Password_Encryption
import sys
import string
import random
from colorama import init
from termcolor import colored
import smtplib
#from email.mime.multipart import MIMEMultipart


def decrypt_password_list(Master_Password):
    password_values,key = Password_Encryption.get_vals_from_password(Master_Password,int(len(Password_Encryption.get_chars())/2-1))
    decrypted_password_list = ('').join(Password_Encryption.decrypt(Password_Encryption.message_list_generator('c:/users/jpglo/mypythonscripts/Encrypted_Passwords.txt'),password_values,key,Password_Encryption.get_chars())).split(('\n'))
    for i in range(len(decrypted_password_list)):
        decrypted_password_list[i] = decrypted_password_list[i].split(': ')
    return decrypted_password_list

def encrypt_password_list(Master_Password,message):
    password_values,key = Password_Encryption.get_vals_from_password(Master_Password,int(len(Password_Encryption.get_chars())/2-1))
    encrypted_password_list = ('').join(Password_Encryption.encrypt(message,password_values,key,Password_Encryption.get_chars()))
    return encrypted_password_list
    
def rewrite_to_file(decrypted_list,Master_Password):
    lines = []
    for i in decrypted_list:
        lines.append((': ').join(i))
    lines = ('\n').join(lines)
    with open('c:/users/jpglo/mypythonscripts/Encrypted_Passwords.txt','w') as Output:
        Output.write(encrypt_password_list(Master_Password,lines))

def randomize_password():
    new_password = ''
    length = 0
    char_options = list(string.ascii_letters)
    for i in string.punctuation:
        char_options.append(i)
    while True:
        try:
            length = int(input('Enter preferred length:'))
            break
        except:
            print('Enter a valid number')
    for i in range(length):
        new_password = new_password + random.choice(char_options)
    print('Your new password is: '+colored(str(new_password),'green'))

    if input('Would you like to email this password to yourself("YES"):') == 'YES':
        print(new_password)
        email_password(new_password)

    return new_password

def email_password(password):
    sender_add = 'jpgloyer@gmail.com'
    if input('Email may be unsecure. Continue at your own risk("YES"):'):
        receiver_add=input("Exact Recipient Email:")
        email_password='vapdoemguofindyt'
        #print(password)
        smtp_server=smtplib.SMTP('smtp.gmail.com',587)

        #Logon
        smtp_server.ehlo()
        #Encrypt
        smtp_server.starttls()
        #Logon again
        smtp_server.ehlo()

        smtp_server.login(sender_add,email_password)

        msg_to_be_sent=f'''\\From: {sender_add} \nSubject: New Password \n\n{password}'''
        print('msg:'+msg_to_be_sent)
        smtp_server.sendmail(sender_add,receiver_add,msg_to_be_sent)
        smtp_server.quit()

def main():
    init()
    decrypted_password_list = [[]]
    Master_Password = getpass("Master Password:")
    operation_choice = -1
    if Master_Password != 'New':
        decrypted_password_list = decrypt_password_list(Master_Password)
        if decrypted_password_list[0] != ['Website', 'Username', 'Password']:
            sys.exit("Incorrect Password")
    if Master_Password == 'New':
        decrypted_password_list[0] = ['Website', 'Username', 'Password']

    options = [['Find Password',0],['Add Password',1],['Change Master Password',2],['Change Password',3],['Remove Entry',4],['Generate Random Password',5]]
    
    while operation_choice != 'q':
        #print('-----------------------------------------')
        for i in options:
            print(f'{i[1]}:\t{i[0]}\n')
        if Master_Password != 'New':
            operation_choice = input('Enter operation number("q" to quit):')
        else: 
            operation_choice = '2'
        
        decrypted_password_list[1:] = sorted(decrypted_password_list[1:],key=lambda k: k[0]) 
        
        #print(decrypted_password_list)
        
        if operation_choice == '0':
            #Reveal entry password---------------------------------------------------------------------------------------------------
            #Print options
            for i in range(len(decrypted_password_list)):
                print(f'{i}:'.ljust(5) + f'{decrypted_password_list[i][0]}'.ljust(20,'-') + f'{decrypted_password_list[i][1]}'.ljust(40))
            password_choice = input('Select password number to reveal:')
            #print('-----------------------------------------')
            #Print entry info
            print('\n\n')
            print(f'{decrypted_password_list[0][0]}:'.ljust(14) + f'{decrypted_password_list[int(password_choice)][0]}'.ljust(30) + '\n'
                f'{decrypted_password_list[0][1]}:'.ljust(15) + f'{decrypted_password_list[int(password_choice)][1]}'.ljust(30) + '\n'
                +f'{decrypted_password_list[0][2]}:'.ljust(14) + colored(f'{decrypted_password_list[int(password_choice)][2]}'.ljust(30),color='red',attrs=['bold']))
            print('\n\n')
            if input('Would you like to email this password to yourself("YES"):') == 'YES':
                #print(decrypted_password_list[int(password_choice)][2])
                email_password(decrypted_password_list[int(password_choice)][2])

        elif operation_choice == '1':
            #Add new entry---------------------------------------------------------------------------------------------------
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

            decrypted_password_list.append([website,username,password])
            #rewrite_to_file(decrypted_password_list,Master_Password)

        elif operation_choice == '2':
            #Change master password---------------------------------------------------------------------------------------------------
            new_password = ''
            new_confirmed_password = ' '
            while new_password != new_confirmed_password:
                new_password = getpass('New password:')
                new_confirmed_password = getpass('Confirm password:')
            Master_Password = new_password

            #rewrite_to_file(decrypted_password_list,Master_Password)

        elif operation_choice == '3':
            #Change entry---------------------------------------------------------------------------------------------------
            for i in range(len(decrypted_password_list)):
                print(f'{i}:'.ljust(5) + f'{decrypted_password_list[i][0]}'.ljust(20,'-') + f'{decrypted_password_list[i][1]}'.ljust(40))
            password_choice = 0
            choice_checks = False

            #Runs until user entered value serves as a valid list index
            while not choice_checks:
                try:
                    password_choice = input('Select password number to change:')
                    decrypted_password_list[int(password_choice)]
                    if password_choice != 0:
                        choice_checks = True
                    else:
                        print('Enter a valid number')
                except:
                    print('Enter a valid number')
            print(decrypted_password_list[int(password_choice)][0])
            new_password = ''
            new_confirmed_password = ' '
            if input('Would you like to randomize this password(YES):') == 'YES':
                new_password = randomize_password()
                new_confirmed_password = new_password
            while new_password != new_confirmed_password:
                new_password = getpass('New password:')
                new_confirmed_password = getpass('Confirm password:')
            decrypted_password_list[int(password_choice)][2] = new_password 

            #rewrite_to_file(decrypted_password_list,Master_Password)


        elif operation_choice == '4':
            #Remove entry---------------------------------------------------------------------------------------------------
            decrypted_password_list_new = []
            choice = '0'
            for i in range(len(decrypted_password_list)):
                print(f'{i}:'.ljust(5) + f'{decrypted_password_list[i][0]}'.ljust(20,'-') + f'{decrypted_password_list[i][1]}'.ljust(40))
            while choice == '0':
                choice = input('Select entry number to be removed (-1 to cancel):')
            for i in range(len(decrypted_password_list)):
                if str(i) != choice:
                    #print(i,choice)
                    decrypted_password_list_new.append(decrypted_password_list[i])
            decrypted_password_list = decrypted_password_list_new
        
            #rewrite_to_file(decrypted_password_list,Master_Password)

        elif operation_choice == '5':
            print('Copy for later use')
            randomize_password()

    rewrite_to_file(decrypted_password_list,Master_Password)
    
    
             

if __name__ == '__main__':
    main()