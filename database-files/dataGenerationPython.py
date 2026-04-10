from faker import Faker
from faker.providers import address
import random
import requests

GLOBAL_LOCALIZATION = "en_GB"
ARTISTS = [
    "Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso",
    "Claude Monet", "Michelangelo Buonarroti", "Rembrandt van Rijn",
    "Johannes Vermeer", "Salvador Dalí", "Frida Kahlo",
    "Andy Warhol", "Georgia O'Keeffe", "Gustav Klimt",
    "Edvard Munch", "Henri Matisse", "Jackson Pollock",
    "Auguste Rodin", "Artemisia Gentileschi", "Katsushika Hokusai",
    "Pierre-Auguste Renoir", "John Singer Sargent", "Thomas Cole"
]

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
            email += name[0: random.randrange(int(len(name) / 2), len(name))]
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

def museumBranchName(location, localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    nameBeginning = [location + "\'s ", "The " + location + " ", "The " + fake.name() + " "]
    nameEnd = ["Art Museum", "Institute for the Arts", "Museum of Fine Art", "Museum", "Collection", "Galleries"]
    return nameBeginning[random.randrange(0, len(nameBeginning))] + nameEnd[random.randrange(0, len(nameEnd))]

def exhibitName(artist):
    exhibits = ["Best of " + artist, "The " + artist + " Collection", artist + ": A Review", "A selection of " + artist + "s",
                artist + ": Biography Through Art", artist + " and Their Works"]
    return random.choice(exhibits)

def foundationName(city, representative, prefix, localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    nameBeginning = ["The " + prefix + " " + representative[-1] + " ", "The " + city + " ",
                     representative[0] + " " + representative[-1] + "\'\'s ", city + "\'\'s "]
    nameEnd = ["Foundation", "Conservation Society", "Historical Society", "Collective for the Arts", "Art Group",
               "Conservation Group", "Fund", "Estate", "Council", "Committee", "Grant"]
    return nameBeginning[random.randrange(0, len(nameBeginning))] + nameEnd[random.randrange(0, len(nameEnd))]

def museumWorkerData(amount):
    values = []
    for i in range(amount):
        curName = name(random.randrange(0, 2), random.randrange(0, 2))
        email = emailFromName(curName, "metmuseum.org")
        curName = prepName(curName)
        values.append([i + 3328, curName[0], curName[1], curName[2], email, phone(), random.randrange(1, 7)])
    print(insert("MuseumWorkers", values))

def artistWikipediaBio(artist):
    headers = {
        "User-Agent": "CS3200 Project (ailon.y@northeastern.edu)"
    }

    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + artist.replace(" ", "_")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['extract'].replace("\'", "\'\'")
    else:
        return "No Artist Data :/"

def normalizeArtistName(artist):
    artistSplit = artist.split(" ")
    if len(artistSplit) == 2:
        return [artistSplit[0], None, artistSplit[1]]
    else:
        return [artistSplit[0], artistSplit[1], artistSplit[2]]

def getDateTime(yearMin = 2026, canBeNull = False):
    if canBeNull and random.randrange(1,4) == 1:
        return None
    return str(yearMin + random.randrange(1,6)) + "-" + str(random.randrange(1,13)) + "-" + str(random.randrange(1,29))

def museumBranchData(amount):
    values = []
    branchIDs = []
    fake = Faker(GLOBAL_LOCALIZATION)
    fake.add_provider(address)
    for i in range(amount):
        curName = name(random.randrange(0, 2), random.randrange(0, 2))
        city = fake.city()
        email = emailFromName(curName)
        curName = prepName(curName)
        branchID = 400000 + random.randrange(0, 100000)
        values.append(
            [branchID, museumBranchName(city), curName[0], curName[1], curName[2], phone(),
             email, fake.street_address(), city, fake.postcode()])
        branchIDs.append(branchID)
    print(insert("MuseumBranch", values))
    return branchIDs

def galleryData(branchIDs, galleryPerBranchMin, galleryPerBranchMax, localization = GLOBAL_LOCALIZATION):
    values = []
    galleryIDs = {}
    fake = Faker(localization)
    for branchID in branchIDs:
        wings = ["The " + fake.name() + " Wing", "The " + fake.name() + " Wing"]
        galleryIDs[branchID] = []
        for _ in range(random.randrange(galleryPerBranchMin, galleryPerBranchMax)):
            galleryName = "The " + fake.name() + " Gallery"
            if random.randrange(0,2) == 0:
                galleryName = "The " + fake.first_name() + " & " + fake.first_name() + " " + fake.last_name() + " Gallery"
            galleryID = random.randrange(100, 1000)
            values.append([galleryID, branchID, galleryName,
                           wings[random.randrange(0, len(wings))], random.randrange(50, 100)]
                          )
            galleryIDs[branchID].append(galleryID)
    print(insert("Galleries", values))
    return galleryIDs

def getDonorData(amount, localization=GLOBAL_LOCALIZATION):
    # (44938, 'The Elizabeth Bennet Foundation for the Arts', 'jane.au@EBFA.org',
    #         'Ms.', 'Jane', NULL, 'Austen',
    #         'Winchester Rd', 'Chawton', NULL, 'GU34 1SD'),
    fake = Faker(localization)
    values = []
    donorIDs = []
    for i in range (amount):
        donorID = random.randrange(100000, 1000000)
        gender = random.randrange(0, 2)
        representative = name(gender, random.randrange(0, 2))
        prefix = fake.prefix_female()
        if gender != 1:
            prefix = fake.prefix_male()
        city = fake.city()
        organizationName = foundationName(city, representative, prefix)
        email = emailFromName(representative, "".join([word[:1] for word in organizationName.split(" ")]) + ".org")
        representative = prepName(representative)
        values.append([donorID, organizationName, email, prefix, representative[0], representative[1],
                       representative[2], fake.street_address().replace("\n", " "), city, fake.postcode()])
        donorIDs.append(donorID)
    print(insert("Donors", values))
    return donorIDs

def getArtistData(artists):
    values = []
    artistIDs = {}
    artistIDCurrent = 348#random.randrange(200,400)
    for artist in artists:
        artistIDCurrent += 1
        nameList = normalizeArtistName(artist)
        values.append([artistIDCurrent, nameList[0], nameList[1], nameList[2], artistWikipediaBio(artist)])
        artistIDs[artist] = artistIDCurrent
    print(insert("Artist", values))
    return artistIDs

def getExhibitData(artistIDs, galleryIDlist):
    values = []
    museumBranches = list(galleryIDs)
    for artist, artistID in artistIDs.items():
        branchID = random.choice(museumBranches)

        galleriesCount = len(galleryIDlist[branchID])
        galleryIndex = random.randrange(0, galleriesCount)
        galleryID = galleryIDlist[branchID][galleryIndex]
        galleryIDlist[branchID].pop(galleryIndex)
        if galleriesCount == 1:
            museumBranches.remove(branchID)
        startTime = getDateTime()
        startTimeArray = startTime.split("-")
        endTime = getDateTime(int(startTimeArray[0]), True)
        values.append([artistID * 2 + 5, galleryID, branchID, exhibitName(artist), artistWikipediaBio(artist)[:50] + "...", startTime, endTime])
    print(insert('Exhibits', values))

#def getArtistWorks(artist, artistID, startIDat, maxWorks)


museumIDs = [432110, 482743, 443755, 492860, 481322, 480244, 411616, 400024, 404681, 484166, 474015, 422135]
galleryIDs = {432110: [419, 177, 986], 482743: [100, 323, 576, 804, 216], 443755: [609, 159, 874, 755], 492860: [970, 373, 535, 635], 481322: [793, 584, 433, 754, 447], 480244: [347, 474, 417, 601], 411616: [716, 660, 347, 259], 400024: [403, 482, 794, 869, 819], 404681: [245, 471, 874, 758], 484166: [198, 879, 359, 822], 474015: [404, 667, 375, 605, 687], 422135: [766, 392, 707]}
artistIDs = {'Leonardo da Vinci': 349, 'Vincent van Gogh': 350, 'Pablo Picasso': 351, 'Claude Monet': 352, 'Michelangelo Buonarroti': 353, 'Rembrandt van Rijn': 354, 'Johannes Vermeer': 355, 'Salvador Dalí': 356, 'Frida Kahlo': 357, 'Andy Warhol': 358, "Georgia O'Keeffe": 359, 'Gustav Klimt': 360, 'Edvard Munch': 361, 'Henri Matisse': 362, 'Jackson Pollock': 363, 'Auguste Rodin': 364, 'Artemisia Gentileschi': 365, 'Katsushika Hokusai': 366, 'Pierre-Auguste Renoir': 367, 'John Singer Sargent': 368, 'Thomas Cole': 369}
print(getExhibitData(artistIDs, galleryIDs))