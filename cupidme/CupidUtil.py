class CupidException(Exception): pass

#string_between is used primarily to help extract information from script tags
#could replace with regex
def string_between(text, before, after):
    return (text.split(before))[1].split(after)[0]