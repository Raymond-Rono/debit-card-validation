
import re   #   Python module for providing regular expression. This will allow for matching operations for patterns and strings to be searched#[2]
from itertools import groupby # Python module for providing iteration grouping for repeating digits#[1]


COLUMNS_TO_TEST_FOR_VALIDITY = ["debitcard"] # Constant holding the name(s) of columns to test for validity. The column/field list can be expanded

#   NUMERIC_REGEX is the regular expression used to decide ifa value is numeric as per the conditions described in the assignment.
NUMERIC_REGEX = re.compile(r"(\+|-)?([0-9- ]+\.?[\.0-9-]*|\.[0-9-]+)([eE](\+|-)?[0-9-]+)?$")

#   DEBIT_CARD_REGEX is the regular expression used to decide if a given number is valid debit card number or not as per the conditions described in the assignment.
#   A debit card number must start with 4,5 or 6. Must contain exactly 16 digits. Must only consist of digits(0-9).
#   A debit card may have digits in groups of 4, separated by one hyhen "-". Must NOT use any other separtor like '','_' etc.
#   A debit card must NOT have 4 or more consecutive repeated digits
DEBIT_CARD_REGEX = re.compile(r"^([4-6])\d{15}|^([4-6])\d{3}((-{1}\d{4}){3})$")

# FORMAT_CONSTANTS_TO_STRIP is a tuple of constants which will be used to replace separators in debit card before testing for consecutive repeated digits
FORMAT_CONSTANTS_TO_STRIP = (("-",""),("",""))  # this can have longer list and can be changed to suit different conditions e.g. (("-",""),(" ",""),,("_",""))
                                                # the second item ("","") is for replace to work well otherwise it will throw an exception [replace() takes at least 2 arguments]. It has no effect in string being tested

#   ##      ###         ####                START of user defined functions              ####            ###     ##  #

def validateDebitCard(str_debit_card): #[7][4][6]
    """
    summary : code to take a string input and return if the debit card number is valid or not (TRUE if valid, FALSE if NOT).
    Function Name: validateDeditCard
    Function Use: Function will check if a given number is valid debit card number or not
    FunctionsCalled:    REGEX.match() - Python regular expression which searches a string for a match. retruns true if it matches and false otherwise
                        replace() - Python in-built string function which returns a copy of string with all occurrences of old substring old replaced by new
                        max() - Python in-built function which returns largest item in an iterable
                        len() - Python in-built function which returns the number of items of an object
                        list() - Python in-built object function which a list whose items are the same
                        Decimal() - Python in-built object fixed-point for representing values in an exact manner
    Argument(s) Accepted: [str_debit_card]: The string consisting of debit card value which needs to be tested
    Value(s) Returned: Boolean True or False. True if conditions are met, False otherwise.
    """
    # importing Decimal to be used in converting exponential debit card strings to decimal for analysis
    from decimal import Decimal # to assist in conversion # used in validateDebitCard to convert exponential strings to decimal common in text files for input data

    # this regular expression is used to test whether a number string is in exponential form. If so it needs to be converted to Decimal before being tested. Otherwise the string remains as is.
    EXPONENT_NUMERIC_REGEX = re.compile(r"(\+|-)?([0-9- ]+\.?[\.0-9-]*|\.[0-9-]+)([eE](\+|-)[0-9-]+)$")

    
    #   Check if the debit card meets conditions described below:
    #   1. A debit card number must start with 4,5 or 6. Must contain exactly 16 digits. Must only consist of digits(0-9).
    #   2. A debit card may have digits in groups of 4, separated by one hyhen "-". Must NOT use any other separtor like '','_' etc.
    #   3. A debit card must NOT have 4 or more consecutive repeated digits
    #   DEBIT_CARD_REGEX = re.compile(r"^([4-6])\d{15}|^([4-6])\d{3}((-{1}\d{4}){3})$")
    #   DEBIT_CARD_REGEX is the regular expression costant used to decide if a given number is valid debit card number or not as per the conditions described in the assignment.

    # if it matches the regex constant defined, then proceed to remove separators and test for 4 or more consecutive repeated digits
    # But before testing debit card conditions , the string must be tested first to check if it meets the basic numeric conditions neccessary for a debit card to exist as numeric
    is_valid = False # Assuming initially the debit card string is not valid. The code will be looking for an opportunity to confirm its validity and assign boolean true to is_valid variable.
                     # Until all the conditions are met, is_valid will remain False
    if NUMERIC_REGEX.match(str_debit_card): # check if debit card string is numeric and meeting the basic conditions of being considered so. The strings not meeting the condition will return false.

        # if string is in exponential form, convert it to float then to decimal then revert it back to string to allow for debit card regex testing. some debit cards especially in tabular text input files may be expressed exponentially
        if EXPONENT_NUMERIC_REGEX.match(str_debit_card): # check if in exponent form.
            num_debit_card = str(Decimal(float(str_debit_card))) #  convert to float then to decimal and revert to string 
        else: # else leave it the way it is if not exponential
            num_debit_card = str_debit_card
        # testing debit card conditions starts.
        if DEBIT_CARD_REGEX.match(num_debit_card): # is the str_debit_card matching the DEBIT_CARD_REGEX regex? DEBIT_CARD_REGEX contains 1 and 2 conditions above. (Testing condition 1 and 2 above)
            for constant in FORMAT_CONSTANTS_TO_STRIP: # currently defined FORMAT_CONSTANTS_TO_STRIP = (("-","")). This can be expanded depending on configs. 
                num_debit_card = num_debit_card.replace(*constant) # strip/remove separators from the debit card string. Remove as many constants as defined before returning the string to be tested for repeating digits
            max_len_for_repeating_digits = max(len(list(e)) for _, e in groupby(num_debit_card)) # get the maximum length for repeating digits after grouping them
            is_valid =  (max_len_for_repeating_digits < 4) # test for 4 or more consecutive repeated digits. Will return FALSE if having 4 or more consecutive repeated digits and TRUE otherwise. (Testing condition 3 above)
    return is_valid # return false to mean debit card string is not matching the regex defined hence not meeting conditions presented. It may also not be meeting even the numeric conditions let alone debit card conditions
 
def removeInvalidDebitCardEntries(pre_processed_data): #[8]
    """
    summary : code to remove all the rows having invalid debit card numbers. Accepts preproccessed data and returns data without invalid debit card entries
    Function Name: removeInvalidDebitCardEntries
    Function Use:   Function will remove all the rows having invalid debit card numbers
    FunctionsCalled:    validateDebitCard() - user defined function to check if a given number is a valid debit card number or not
                        append() - Python built-in function to append items to a list.
    Argument(s) Accepted:   [pre_processed_data]: this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be proccessed further through sorting
    Value(s) Returned: None: [new_pre_processed_data] data in a list of dictionaries without invalid debit card numbers in specified columns/fields(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]  
    """
   
    new_pre_processed_data = []
    for obj in pre_processed_data:
        debit_card_is_valid = False  # assuming the debit card is not valid as per prescribed conditions.
        for key in obj:
            # test whether we are testing values in the correct columns/fields as per the constant COLUMNS_TO_TEST_FOR_VALIDITY and also whether debit card is valid. Both must be TRUE
            if ((key in COLUMNS_TO_TEST_FOR_VALIDITY)):
                if ((validateDebitCard(str(obj[key])))): # convert to string before validating if not in string format
                    debit_card_is_valid = True # if the test is passed then debit_card_is_valid is assigned boolean value TRUE and so row/object with the debit card qualifies to be retained.
        if debit_card_is_valid: # if the debit_card_is_valid has value TRUE, its corresponding row/object can be appended to the list of those objects with valid debit cards.
            new_pre_processed_data.append(obj)

    return new_pre_processed_data  
#   ##      ###         ####                END OF user defined functions              ####            ###     ##  #

