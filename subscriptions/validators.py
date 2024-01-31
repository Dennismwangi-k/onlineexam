
def validate_possible_number(phone_number):
    validated_phone_number = ""

    if phone_number[0] == "2" or phone_number[0] == 2:
        validated_possible_number = phone_number
    elif phone_number[0] == "+":
        validated_possible_number = phone_number[1:]

    elif phone_number[0] == "0" or phone_number[0] == "0":
        validated_possible_number = "254" + phone_number[1:]
    
    return validated_possible_number

