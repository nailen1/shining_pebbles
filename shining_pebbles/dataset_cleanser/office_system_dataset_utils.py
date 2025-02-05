
def parse_commaed_number(number_str):
    if isinstance(number_str, (int, float)):
        return number_str
    else:
        return float(number_str.replace(',', ''))
   
def force_int(number):
    if isinstance(number, float) and number.is_integer():
        return int(number)
    return number