# User Manual for Group Password Manager
* Group Password Manager(GPM) is designed for organizations that have a mix of personal accounts with private passwords and shared accounts with shared passwords
## Inner Workings
* GPM runs based around a proprietary encryption model designed to make saved text files entirely unreadable. The file can be saved in an unsecure location because the file itself contains the security. The actual information contained within can only be accessed upon execution of a decryption given the same password 'seed.' 
* GPM was designed with the idea of shared network drives in mind. Currently, GPM knows where to find the Password data by attempting to access the file name/path written in the final line of DataBase_location.txt. This will likely be updated to be an option on the initial login screen.
## Use Instructions
* When a user runs GPM, they will be prompted to enter three pieces of information:
    * A Group Master Password will allow the decryption of the skeleton of the shared file. This skeleton includes a group name, a list of enabled users, and sections of user passwords that remain under another level of encryption. 
        * The first 'user' will act as the organization's shared password drive. One initial decryption will not reveal these passwords, but GPM will automatically run a second decryption using the Group Master Password that will open access.
    * A Username will tell GPM which section of encrypted information to evaluate with the:...
    * An Individual Password will allow a user to decrypt and access their private list of passwords 
* Available Actions:
    * Reveal Password
        * When an entry is highlighted, clicking 'Reveal Password' will bring up a dialog window revealing the login credentials for that entry. An option to copy the password to the user's clipboard is given.
    * Add Password
        * Brings up a series of dialog boxes allowing the user to write an entry's website, username, and password. 
        * All three must contain SOME text, and duplicate website names are not allowed.
        * An option to add a random password will be added in the future
    * Change Password
        * When an entry is highlighted, clicking 'Change Password' will bring up a single dialog window accepting a new password. 
        * An option to change an entry's username is not given. Entry must be removed and recreated to change the username.
    * Remove Password
        * Removes the selected password after prompting user to confirm decision by typing "CONFIRM"
    * Change Personal Encryption Password
        * Brings up a quick text entry box to allow the user to change their password credential for GPM
    * Import Passwords
        * Imports a correctly formatted .csv file that contains unencrypted lines of "website, username, password"
* Available Admin Options:
    * Current Admin is defaulted to the first user.
        * This will change in next update, where shared group passwords will be stored in the first user slot, and Admin is defaulted to be the second user