from sys import exit
# Using in 'main_menu()'
import os
# Using in 'create_new_dict()'
import json
# Using in 'load_json_file()' and 'save_json_file()'
import random
# Using in 'test_my_knowledge()'
import pyfiglet
# Using in 'show_ascii_logo()'


def show_ascii_logo():
    '''
    Display the 'SmartVoc' logo in the standard font.\n 
    This function is used within the 'greeting()' function to display the 'SmartVoc' logo in ASCII art.
    '''
    custom_font = pyfiglet.Figlet(font='standard')
    ascii_text = custom_font.renderText("SmartVoc")
    print(ascii_text)


def greeting():
    '''
    This function is called when the program starts.
    It displays the SmartVoc logo using 'show_ascii_logo()', greets the user, and opens the main menu using 'main_menu()'.
    '''
    show_ascii_logo()
    print("Welcome to SmartVoc!")
    main_menu()


def main_menu():
    '''
    This function allows the user to choose from various program options by inputting a number.

    Options:
    1) Create a new dictionary
    2) Add a new word
    3) Test my knowledge
    4) About (program documentation)
    5) Quit

    Depending on the input number, the function calls the following functions:
    1) 'create_new_dict()'
    2) 'add_word()'
    3) 'test_my_knowledge()'
    4) (Program documentation, to be implemented)
    5) Exits the program.

    If the user's input is not one of the listed numbers, the function will repeatedly prompt for a valid input.

    This function is called at the start of the program by 'greeting()' and is called again after the user completes any option. 
    '''
    while True:
        try:
            home_input = int(input("""\nWhat you wanna do?
1)Create new dictionary  2)Add a new word
3)Test my knowledge      4)about
5)quit\n>"""))
            if home_input == 1:
                create_new_dict()
                break
            elif home_input == 2:
                add_word()
                break
            elif home_input == 3:
                test_my_knowledge()
                break
            elif home_input == 4:
                show_documentation()
                break
            elif home_input == 5:
                exit('\nGoodbye!')
            else:
                pass
        except ValueError:
            pass
        except EOFError:
            exit('\nGoodbye!')
        except KeyboardInterrupt:
            pass


def create_new_dict():
    '''
    This function creates a new user's dictionary by following these steps:
    1. Asks the user to type the new dictionary name.
    2. Creates a new dictionary inside the path '/cache/dicts/' using the 'input_dictionary_name'.
    3. Inside 'cache/dicts/{input_dictionary_name}/', creates a new JSON file with the name {input_dictionary_name}_dict.json 
    and an empty dictionary in it.

    After that, the function informs the user that the dictionary was created successfully and calls 'main_menu()'.
    This function is used when home_input == 1 in 'main_menu()'.

    If a file with the entered name already exists, the function will print "A dictionary with that name already exists!" and recycle itself.
    If the user tries to enter the name in path format (e.g., '/path/name/'), the function will print "Sorry, the name was typed incorrectly." and recycle itself.
    If the user enters unacceptable symbols, the function will print "Please, don't use the following symbols in the dictionary name: \, /, >, <, *, ?, :" and recycle itself.
    '''
    while True:
        try:
            input_dictionary_name = input(
                "Please, type the new dictionary name: ")
            if '/' in input_dictionary_name:
                raise OSError

        except FileExistsError:
            print("A dictionary with that name already exists!")

        except FileNotFoundError:
            print("Sorry, the name was typed incorrectly.")

        except (ValueError, InterruptedError, PermissionError):
            pass

        except OSError:
            print(
                r"Please, don't use the following symbols in the dictionary name: \, /, >, <, *, ?, :")

        except (KeyboardInterrupt, EOFError):
            exit('\nGoodbye!')

        else:
            os.makedirs(f'cache/dicts/{input_dictionary_name}')

            with open(f"cache/dicts/{input_dictionary_name}/{input_dictionary_name}_dict.json", 'w') as dict_file:
                json.dump({}, dict_file)

            print(
                f"\nNew dictionary '{input_dictionary_name}' created succesfully!\n", flush=True)
            main_menu()
            break


def load_json_file(file_path):
    '''
    Load data from a JSON file specified by the given file path.

    Args:
        file_path (str): The path to the JSON file to be loaded.

    Returns:
        dict: The data from the JSON file, or an empty dictionary if the file is not found or is not valid JSON data.

    This function is used by 'add_word()', 'choose_the_dict()', and 'test_my_knowledge()' to work with user dictionaries.
    '''
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return {}


def save_json_file(file_path, data):
    '''
    Save new data to a JSON file specified by the given file path.

    Args:
        file_path (str): The path to the JSON file to be saved. 
            In SmartVoc, the file path is taken from 'dictionary_input' in 'choose_the_dict()'
            and looks like this: 'cache/dicts/{dictionary_input}/{dictionary_input}_dict.json'
        data (dict): Data to be saved to the JSON file. 
            In SmartVoc, the data for saving to the JSON file is a dictionary containing word-translation pairs.
            It is taken from 'add_word()' and saved to the user's dictionary by 'file_path'. 

    This function is used by 'add_word()' to save new words and translations to the user's dictionary. 
    '''
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def show_documentation():
    '''
    Display user documentation retrieved from 'about.txt' file.

    This function reads and prints the content of the 'about.txt' file, which contains information about the program and its usage. 
    It is typically called from the 'main_menu()' function when the user selects option 4.
    '''
    with open('about.txt', 'r') as file:
        data = file.read()
        print(data)

    main_menu()


def choose_the_dict():
    '''
     Ask the user to input the name of the desired dictionary. Print the number of words inside the chosen dictionary.

    This function lists the names of all directories in the 'cache/dicts' path and takes the 'dictionary_input'
    that the user needs. Afterward, it generates the path to the user's dictionary.

    Returns:
        str: The path to the selected dictionary in the format: 'cache/dicts/{dictionary_input}/{dictionary_input}_dict.json'

    Raises:
        FileNotFoundError: If 'dictionary_input' does not match any directory in 'cache/dicts'.
        EOFError: If the user decides to exit.

    This function is utilized by 'add_word()' and 'test_my_knowledge()' functions to retrieve the dictionary path.
    '''
    while True:
        try:
            print("\nPlease type the name of the dictionary you need:")
            dicts_list = os.listdir('cache/dicts')
            for dicts in dicts_list:
                print(dicts)
            dictionary_input = input('> ')
            if dictionary_input not in dicts_list:
                raise FileNotFoundError()
            else:
                dictionary_path = f'cache/dicts/{dictionary_input}/{dictionary_input}_dict.json'
                data = load_json_file(dictionary_path)
                num_elements = len(data)
                if num_elements == 0:
                    print(f"The dictionary '{dictionary_input}' is empty.")
                else:
                    print(
                        f"The dictionary '{dictionary_input}' contains {num_elements} words.")
                return dictionary_path
        except FileNotFoundError:
            print(
                f"Sorry, the dictionary '{dictionary_input}' does not exist!\n")
        except EOFError:
            exit('\nGoodbye!')
        except ValueError:
            pass


def add_word():
    '''
    Add new word-translation pair to user's dictionary.

    This function is calling 'choose_the_dict()' to get desired user's dictionary path.
    It gives return of 'choose_the_dict()' as argument to load_json_file() for open user's dictionary and change it's data. 
    Afterward, function asks user two inputs:
        word_input: new word in language that user learning.
        translation input: translation of 'word_input' in native user's language.
    New pair 'word':'translation' adds to user's dictionary and saves by 'save_json_file()'.
    User gets message that new pair added succesfully and function calling 'main_menu()'.

    This function can be called if in 'main_menu()' home_input == 2.
    '''
    file_path = choose_the_dict()
    data = load_json_file(file_path)

    word_input = input(
        "Please type the word in the language you are learning: ")
    translation_input = input(
        f"Please type the translation of the word '{word_input}' in your native language: ")

    data[word_input] = translation_input
    save_json_file(file_path, data)

    print(f"\nWord '{word_input}' and its translation '{translation_input}' have been added to your dictionary succesfully.\n")

    main_menu()


def ask_number_of_words_for_test(dictionary_data):
    '''
    Ask the user how many dictionary words they want to include in the test.

    This function prompts the user to enter an integer via 'user_input'. 
    If 'user_input' is less than or equal to the number of words in the dictionary, 
    the function returns 'user_input'.
    If 'user_input' is greater than the number of words in the dictionary, it prints:
        "The entered quantity is greater than the number of words in the dictionary.
        You can enter a lower number or add more words to the dictionary." and reiterates.
    If 'user_input' == 0, it prints "At least 1 word must be included in the test!" and reiterates.

    Args:
        dictionary_data (dict): JSON file data from the user's dictionary, obtained from the return value of 'load_json_file()'.

    Returns:
        int: The user-supplied number of words for the test.

    Raises:
        ValueError: If 'user_input' is not an integer, the function prompts the user to try again.

    This function is used within 'test_my_knowledge()'.
    '''
    while True:
        try:
            user_input = int(
                input("Please enter the number of words you want to include in the test: "))
            words_quantity = len(dictionary_data)
            if user_input > words_quantity:
                print("""\nThe entered quantity is greater than the number of words in the dictionary.
You can enter a lower number or add more words to the dictionary.\n""")
            elif user_input == 0:
                print("At least 1 word must be included in the test!\n")
            else:
                return user_input
        except ValueError:
            pass


def test_my_knowledge():
    '''
    Test the user's knowledge of word translations in a dictionary.

    This function can be called when 'home_input' in 'main_menu()' is set to 3.
    Details in comments. 

    Returns:
        None

    '''
    # Ask the user to enter the name of the desired dictionary and retrieve its path.
    dictionary_path = choose_the_dict()

    # Load dictionary data for testing the user's knowledge.
    dictionary_data = load_json_file(dictionary_path)

    # Check if the dictionary has any words.
    words_quantity = len(dictionary_data)
    if words_quantity == 0:
        print("Please add at least 1 word to this dictionary to use for the test.")
        main_menu()
    else:
        pass

    # Ask the number of words for testing and save it for the testing process.
    number_of_words_to_test = ask_number_of_words_for_test(dictionary_data)

    # Get 'number_of_words_to_test' random words for user translation.
    words_to_test = random.sample(
        list(dictionary_data.keys()), number_of_words_to_test)

    # Initialize counters.
    correct_answers = 0
    incorrect_answers = {}

    # Test the user's translations of words.
    for word in words_to_test:
        user_translation = input(f"Please type the translation of '{word}': ")

        # Check if the user's translation is correct.
        if user_translation.lower() == dictionary_data[word].lower():
            correct_answers += 1
        else:
            incorrect_answers[word] = dictionary_data[word]

    # Display the test results to the user.
    print(
        f"\nYou have correctly translated {correct_answers} words out of {number_of_words_to_test}!")

    # If the user made mistakes, provide the correct translations of the words.
    if incorrect_answers:
        print("\nCorrect translations for mistaken words:")
        for incorrect_word, correct_translation in incorrect_answers.items():
            print(f"{incorrect_word} - {correct_translation}")

    # Return to the main menu.
    main_menu()
