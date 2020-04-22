#!/usr/bin/python3
"""Python implementation of the EFF Dicepass protocol

Generate strong passphrases using the EFF dicespass protocol presented at
www.dicepass.org

This module uses the secrets module as a source of cryptographically secure
random numbers. If you have a better source, fork this code and modify.

This code is provided under a MIT License. See the LICENSE file for more details
"""
import os
import json
import secrets
import warnings
import string

import pyperclip

#Change this to work on your system
working_directory_target = '/Users/mattc/Documents/GitHub/dicepass/'

def wordlist_to_json(in_file, out_file):
    """Import a given word list and output a JSON dictionary for use in the
    passphrase generator

    This function assumes that the word list is an unstructured set of words in
    a text file. The words can be formatted one word per line, or all on lines
    separated by spaces. The words are split up and assigned a diceroll before
    being zipped into a dictionary and saved out to a json.

    If the list of words is too small for the number of rolls, this function
    will raise a ValueError. If the number of words is too large, the word list
    will be truncated to the correct size.
    """

    #Get the words and split them up
    with open(in_file) as f_in:
        raw = f_in.read()
        f_in.close()
    words = raw.split()

    #Build the list of possible dice rolls. This is probably the hard way.
    rolls = []
    for c1 in range(6):
        for c2 in range(6):
            for c3 in range(6):
                for c4 in range(6):
                    for c5 in range(6):
                        rolls.append(str(c1+1) + str(c2+1) + str(c3+1) +
                        str(c4+1) + str(c5+1))

    if len(rolls) > len(words): #not enough
        msg = "Not enough words to map to all dice rolls. #Rolls="+str(len(rolls))+" #Words="+str(len(words))
        raise ValueError(msg)
    elif len(rolls) < len(words): #too many
        words = words[:len(rolls)]
        msg = "Too many words to map to all dice rolls. Truncating word list"
        warnings.warn(msg,Warning)

    word_dict = dict(zip(rolls,words))

    with open(out_file,'w') as f_out:
        json.dump(word_dict, f_out)
        f_out.flush()
        f_out.close()

def generate_passphrase_basic(word_count=5, word_list_file="eff_large_wordlist.json"):
    """Generate a passphrase of a given length from a given JSON file containing
    a dict of diceroll:word pairs.

    If no parameters are given, the function will default to a 5-word phrase
    generated from the EFF Large Word List.

    This function does not permit repeated words in a passphrase.
    """

    #Get word list
    with open(working_directory_target+word_list_file) as f_in:
        word_list = json.load(f_in)

    #Initialize important variables
    pass_string = ""
    dice_rolls = []
    word_list_keys = list(word_list.keys()) #need to cast dict_list to list
    k = secrets.choice(word_list_keys) #initialize k to check for repeats

    #Generate pass phrase
    for ct in range(word_count):

        while k in dice_rolls: #This gaurantees no repeated words
            k = secrets.choice(word_list_keys)

        pass_string = pass_string + " " + word_list[k]
        dice_rolls.append(k)

    pass_string = pass_string[1:]
    return pass_string

def generate_passphrase_3scheme(word_count=5,numeric_count=5, word_list_file="eff_large_wordlist.json"):
    """Generate a passphrase of a given length from a given JSON file containing
    a dict of diceroll:word pairs. Passphrase  will have capitalized  words and
    a  numeric of length numeric_count inserted somewhere in the sequence.

    If no parameters are given, the function will default to a 5-word phrase
    generated from the EFF Large Word List with a 5-digit numeric.

    This function does not permit repeated words in a passphrase.
    """

    #Get word list
    with open(working_directory_target+word_list_file) as f_in:
        word_list = json.load(f_in)

    #Initialize important variables
    pass_elements = []
    dice_rolls = []
    word_list_keys = list(word_list.keys()) #need to cast dict_list to list
    k = secrets.choice(word_list_keys) #initialize k to check for repeats

    #Build the numeric element
    numeric_element = ''.join(secrets.choice(string.digits) for  i in range(numeric_count))
    pass_elements.append(numeric_element)

    #Get the phrase
    for ct in range(word_count):
        while k in dice_rolls: #This gaurantees no repeated words
            k = secrets.choice(word_list_keys)
        pass_elements.append(word_list[k])
        dice_rolls.append(k)

    #Shuffle it up, do the capitalization
    pass_string = ''
    while len(pass_elements) is not 0:
        elem = secrets.choice(pass_elements)
        pass_elements.remove(elem)
        pass_string = pass_string + elem + ' '
    pass_string= string.capwords(pass_string, ' ')

    return pass_string

if __name__ == '__main__':
    #wordlist_to_json("eff_large_wordlist_tall_long.txt", "eff_large_wordlist.json")
    x = generate_passphrase_3scheme()
    pyperclip.copy(x)
    print(x)
