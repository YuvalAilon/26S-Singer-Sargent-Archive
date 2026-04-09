from faker import Faker
import random
GLOBAL_LOCALIZATION = "de_DE"
# into is the table to insert data into, values is an array of arrays
# Ex. insert( "TableA",
#   [
#       ['A', True, 24,  '1900-02-02'],
#       ['B', False, 29, '1990-04-30'],
#       ['C', True, 59,  '1910-04-02']
#   ]
def insert(into, values):
    returnString = 'INSERT INTO ' + into + '\nVALUES ('
    for setIndex in range(len(values)):
        set = values[setIndex]
        if setIndex != 0:
            returnString += "\t("
        for attribute in range(len(set)):
            if isinstance(set[attribute], str):
                returnString += "\'" + set[attribute] + "\'"
            elif set[attribute] is None:
                returnString += "NULL"
            else:
                returnString += str(set[attribute])
            if attribute != len(set) - 1:
                returnString += ", "
        returnString += ")"
        if setIndex != len(values) - 1:
            returnString += ",\n"
    return returnString


def name(isFemale, hasMiddle, localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    nameArray = [fake.last_name()]
    if isFemale:
        nameArray.insert(0, fake.first_name_female())
        if hasMiddle:
            nameArray.insert(0, fake.first_name_female())
    else:
        nameArray.insert(0, fake.first_name_male())
        if hasMiddle:
            nameArray.insert(0, fake.first_name_male())

    return nameArray

def emailFromName(fullNameArray, domain=None, localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    fullName = fullNameArray.copy()
    random.shuffle(fullName)
    email = ""
    if random.randrange(0, 3) == 1:
        fullName.pop(0)
    for name in fullName:
        if random.randrange(0, 2) == 1:
            email += name[0 : random.randrange(int(len(name)/2), len(name))]
        else:
            email += name
        email += "."
    email = email[0:len(email) - 1]
    if random.randrange(0, 3) == 1:
        email += str(random.randrange(0, 999))
    email = email.lower()
    if domain is not None:
        return email + "@" + domain
    else:
        return email + "@" + fake.free_email_domain()

def prepName(name):
    if len(name) == 2:
        name.insert(1, None)
    return name

def phone(localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    return fake.phone_number()

values = []
for i in range(30):
    curName = name(random.randrange(0,2), random.randrange(0,2))
    email = emailFromName(curName, "metmuseum.org")
    curName = prepName(curName)
    values.append([i + 3328, curName[0], curName[1], curName[2], email,phone(), random.randrange(1,4)] )
print(values)
print(insert("MuseumWorkers", values))