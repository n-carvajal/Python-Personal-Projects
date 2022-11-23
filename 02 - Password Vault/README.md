# 100 Days of Python Code

## Project 30: Password Vault Extra

### Brief

Create a password vault program that allows for the saving and retrieval of
website login information.

### Features

* **Regulated Access**: The program can only be accessed via a `master key`.
* **Encryption**: All user information is saved in an encrypted format.
* **Duplicate Detection**: Automatic duplicate check when saving details
provides the option to cancel current submission or overwrite existing.
* **Export Data Feature**: Allows for decryption and export of entire vault to
file of user's choosing.

### Execution

To run the program execute `python main.py` from a command prompt within the
project folder.

### Description

The program consists of 4 GUI screens:

**WELCOME GUI:** First GUI presented to the user upon opening the application.
It consists of:

* `Enter Master Key`: Place to enter a master key in order to access the
application.  If using the program for the first time the user will be prompted
to setup a master key and given hints as to the suggested format of the the
same. Thereafter, the master key entered at setup  must be used in order to
continue into the application.
* `Show Key`: Button that either shows or hides the master key text input.
* `Submit Key`: Button that submits the master key for validation and entry
into the application. On first use the key is written to 'key_file.json'
thereafter the key is checked against the value found in the same.

**SELECTION GUI:** Presented to the user upon successful master key validation.
It consists of:

* `Save Details`: Button that triggers the application's SAVE GUI.
* `Retrieve Details`: Button that triggers the application's RETRIEVE GUI.
* `Export Vault`: Button that allows the user to export a decrypted version of
their vault. If the vault is empty, the button will be greyed out. Else when
clicked it will ask for the master key to confirm export and prompt user for a
file save location.  The exported file is saved int '.txt' format.

**SAVE GUI:** Allows the user to enter website, username and password details
then save them to the vault. It consists of:

* `Website Name`: Place to enter a user defined name for the website entry.
* `Username`: Place to enter the username for the website entry.
* `Password`: Place to enter a user defined password for the entry.
* `Auto Generate`: Generates a random complex password and populates the
website password entry in place of a user generated one.
* `Submit Details`: Once pressed, it encodes the entry information and writes
the result to `logins.json`.

**RETRIEVE GUI:** Allows the user to check the database for website and
username information and returns the corresponding password if it exists in
vault:

* `Website Name`: Place for user to enter the name of the website entry needing
retrieval.
* `Username`: Corresponding username for the website entry requiring retrieval.
* `Retrieve Entry`: Once pressed, encodes 'Website Name' and 'Username', then
searches for a matching entry in `logins.json`.  If found, it decodes the entry
and returns it to the user in plain text via a popup box.  Additionally the
user's clipboard is populated with the retrieved login password for
convenience.

### Notes

* **BLANKS:** All entries must be filled in to complete any operation. If any
left blank a popup will inform error.
* **ENCRYPTION** Currently the program `encrypts` and `decrypts` data as
follows:
  * **Encoding**: To encode data, the program take a word and creates a list of
  its individual characters.  Then it converts each character in the list into
  its corresponding unicode number, then it **ADDS** `SCRAMBLER` to each number
  in the list, and finally it joins the resulting numbers from the list into a
  string leaving a space between each.  For example if `SCRAMBLER` = 5:
    * 'Hello' - String to encrypt.
    * [H, e, l, l, o] - String separated into a list of its characters.
    * [72, 101, 108, 108, 111] - Each character in list converted into its
    corresponding unicode value.
    * [77, 106, 113, 113, 116] - Each value in list having SCRAMBLER added to
    it.
    * '77 106 113 113 116' - List joined into a single string with a blank
    space as the separator.
  * **Decoding:** The program applies the encoding process in reverse to decode
  entries.  It takes the string encoded string, splits it on white space to
  create a list of numbers, **SUBTRACTS** `SCRAMBLER` from each number,
  converts each resulting number into its corresponding character using the
  unicode table, and finally joins the characters for each word to recompose
  the original this time with no white space as the separator.
  * **Process Complexity**: The user can increase or decrease the encryption
  complexity by changing the `SCRAMBLER` value as well as the operator to be
  applied for the 'shift'.  If the operator is changed it must be ensured that
  whichever operation is used to encode, the inverse operation is used to
  decode. You can find `SCRAMBLER` in 'constants' and the encode/decode
  operator can be changed within the relevant function `encode_string()` or
  `decode_string()`.
