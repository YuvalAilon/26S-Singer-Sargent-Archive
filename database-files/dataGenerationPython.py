from faker import Faker
from faker.providers import address
import random
import requests
import time

GLOBAL_LOCALIZATION = "en_GB"
ARTISTS = [
    "Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso",
    "Claude Monet", "Michelangelo Buonarroti", "Rembrandt van Rijn",
    "Johannes Vermeer", "Salvador Dalí", "Frida Kahlo",
    "Andy Warhol", "Georgia O''Keeffe", "Gustav Klimt",
    "Edvard Munch", "Henri Matisse", "Jackson Pollock",
    "Auguste Rodin", "Artemisia Gentileschi", "Katsushika Hokusai",
    "Pierre-Auguste Renoir", "John Singer Sargent", "Thomas Cole"
]
STATUSES = ['pending', 'approved', 'denied', 'ongoing']
museumIDs = [432110, 482743, 443755, 492860, 481322, 480244, 411616, 400024, 404681, 484166, 474015, 422135]
galleryIDs = {432110: [419, 177, 986], 482743: [100, 323, 576, 804, 216], 443755: [609, 159, 874, 755],
              492860: [970, 373, 535, 635], 481322: [793, 584, 433, 754, 447], 480244: [347, 474, 417, 601],
              411616: [716, 660, 347, 259], 400024: [403, 482, 794, 869, 819], 404681: [245, 471, 874, 758],
              484166: [198, 879, 359, 822], 474015: [404, 667, 375, 605, 687], 422135: [766, 392, 707]}
artistIDs = {'Leonardo da Vinci': 349, 'Vincent van Gogh': 350, 'Pablo Picasso': 351, 'Claude Monet': 352,
             'Michelangelo Buonarroti': 353, 'Rembrandt van Rijn': 354, 'Johannes Vermeer': 355, 'Salvador Dalí': 356,
             'Frida Kahlo': 357, 'Andy Warhol': 358, "Georgia O'Keeffe": 359, 'Gustav Klimt': 360, 'Edvard Munch': 361,
             'Henri Matisse': 362, 'Jackson Pollock': 363, 'Auguste Rodin': 364, 'Artemisia Gentileschi': 365,
             'Katsushika Hokusai': 366, 'Pierre-Auguste Renoir': 367, 'John Singer Sargent': 368, 'Thomas Cole': 369}
donorIDs = [449381, 938292, 910714, 108593, 464137, 852822, 807697, 972079, 892808, 221161, 831347, 398805, 521869,
            669876, 591448, 147787, 418078, 235932, 983659, 269977, 459492, 928904, 194024, 950386, 161592, 538036,
            429644, 438042, 991744, 857679, 662385, 290946]
archivistIDs = [3324, 3328, 3330, 3331, 3336, 3339, 3343, 3344, 3350, 3357, 3358, 3360]
curatorIDs = [3326, 3341, 3349, 3356]
artifactIDs = {349: [3007529, 3008869, 3007766, 3009061, 3002857, 3005099, 3007583, 3000981], 350: [3001061, 3009324, 3009503, 3002367, 3007975], 351: [3001827, 3006843, 3004201, 3006366, 3007344, 3005781, 3001026, 3002110], 352: [3009402, 3002871, 3001420, 3002924, 3009318], 353: [3003911, 3006659, 3009944, 3004843, 3002910], 354: [3001448, 3008213, 3009531, 3004879, 3009564, 3002299, 3002507], 355: [3007612, 3009715, 3006305, 3000497, 3007123, 3004852], 356: [3007207, 3001485, 3006634, 3007587, 3000054, 3005950, 3006804], 357: [3003362, 3005057, 3009209, 3001190, 3008834, 3003158, 3004039, 3009886], 358: [3008789, 3001749, 3002256, 3005292, 3006470, 3005570, 3005582], 359: [3009688, 3005204, 3002489, 3002787, 3009102, 3001591], 360: [3000836, 3000868, 3007869, 3004640, 3006688, 3009706, 3005534], 361: [3003467, 3009712, 3006578, 3008704, 3005821, 3001276], 362: [3005049, 3008191, 3005064, 3003532, 3002194], 363: [3002097, 3007951, 3009590, 3005447, 3001477, 3007810, 3008822], 364: [3001823, 3008311, 3003043, 3005011, 3000757, 3007406], 365: [3000749, 3001447, 3008940, 3001149, 3008841, 3000577, 3004745, 3005671], 366: [3002424, 3001848, 3001721, 3005419, 3006035, 3009001], 367: [3009454, 3008978, 3004012, 3001363, 3001090, 3001521], 368: [3003071, 3006494, 3009461, 3007499, 3001977], 369: [3007315, 3007729, 3000887, 3000319, 3005113, 3006582, 3000680]}
exhibitIDs = [823, 293, 703, 705, 707, 709, 711, 713, 715, 717, 719, 721, 723, 725, 727, 729, 731, 733, 735, 737, 739, 741, 743]
artifactRequestIDs = [3736000, 5662000, 7992000, 9003000, 4507000, 3122000, 8814000, 9037000, 7606000, 1713000, 9877000, 4649000, 8975000, 9260000, 8759000, 1447000, 5560000, 1444000, 4379000, 3478000, 3244000, 2092000, 3936000, 6145000, 2856000, 1759000, 1530000, 3057000, 6812000, 3012000, 7657000, 9994000, 3689000, 9780000, 4065000, 1639000, 6889000, 9742000, 3758000, 9847000, 6001000, 8007000, 1745000, 9039000, 8081000, 7974000, 5393000]


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
    exhibits = ["Best of " + artist, "The " + artist + " Collection", artist + ": A Review",
                "A selection of " + artist + "s",
                artist + ": Biography Through Art", artist + " and Their Works"]
    return random.choice(exhibits)


def renoReason(localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    renoAction = ["Expanding ", "Improving ", "Building ", "Fixing up ", "Repairing ", "Modernizing ", "Demolishing "]
    renoLocation = ["the museum''s courtyard ", "the research department ", "the galleries ", "a new gallery ",
                    "the cafe ", "the main entrance ", 'the gift shop ',
                    str(random.randrange(1, 20)) + " new galleries ",
                    "the " + fake.name() + " wing ", "the anti-theft system ", "air conditioning "]
    renoJustification = ["for improved functionality", "since we just got a huge grant", "",
                         "to enhance the user experience", "by discretion of the board",
                         "per request of " + fake.name(),
                         "after numerous patron complaints", "with the donation from " + fake.name()
                         ]
    return (random.choice(renoAction) + random.choice(renoLocation) + random.choice(renoJustification)).strip()


def donationAmount():
    donationSize = random.randint(1, 3)
    if donationSize == 1:
        return random.randint(1000, 9999)
    elif donationSize == 2:
        return random.randint(10000, 99999)
    else:
        return random.randint(100000, 999999)


def donationReason(localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    thankYou = ["Thank you, here''s", "Because of your generosity we are providing", "Please expect",
                "To help with operation costs,", "For hosting the gala,", "I love this museum, so I''ve sent",
                "Your archivists made some interesting points, so have", "For the restoration of our artworks:",
                "To show our appreciation:", "We are so incredibly thankful, find attached",
                "After my discussion with " + fake.name() + ", I''ve decided to donate",
                fake.name() + " has convinced me to give you"]
    donationType = ["a grant", "a small sum", "a recurring donation", "a one time donation", "a large sum",
                    "definitely legally acquired funds", "a research stipend", "funds", "money"]
    donationDescription = ["via wire transfer", "sent by check", "in an unmarked package", "in cash",
                           "to be used for acquiring new art", "to help cover the cost of renovations",
                           "that should arrive by the end of the week", "for all the amazing work you do",
                           "to fund the projects we were discussing", "delivered by " + fake.name(),
                           "send by my assistant, " + fake.name()]
    return random.choice(thankYou) + " " + random.choice(donationType) + " " + random.choice(donationDescription)


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


def getDateTime(yearMin=2026, canBeNull=False):
    if canBeNull and random.randrange(1, 4) == 1:
        return None
    return str(yearMin + random.randrange(1, 6)) + "-" + str(random.randrange(1, 13)) + "-" + str(
        random.randrange(1, 29))


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


def galleryData(branchIDs, galleryPerBranchMin, galleryPerBranchMax, localization=GLOBAL_LOCALIZATION):
    values = []
    galleryIDs = {}
    fake = Faker(localization)
    for branchID in branchIDs:
        wings = ["The " + fake.name() + " Wing", "The " + fake.name() + " Wing"]
        galleryIDs[branchID] = []
        for _ in range(random.randrange(galleryPerBranchMin, galleryPerBranchMax)):
            galleryName = "The " + fake.name() + " Gallery"
            if random.randrange(0, 2) == 0:
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
    for i in range(amount):
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
    artistIDCurrent = 348  # random.randrange(200,400)
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
        values.append(
            [artistID * 2 + 5, galleryID, branchID, exhibitName(artist), artistWikipediaBio(artist)[:50] + "...",
             startTime, endTime])
    print(insert('Exhibits', values))


def getArtifactGroupData(artistIDs):
    values = []
    for artist, artistID in artistIDs.items():
        values.append([artistID, artist, "A collection of " + artist + "''s work"])
    print(insert("ArtifactSet", values))


def getExpansionProjectData(amount, branchIDs, statuses=STATUSES, localization=GLOBAL_LOCALIZATION):
    fake = Faker(localization)
    values = []
    for i in range(amount):
        representative = name(random.randrange(0, 2), random.randrange(0, 2))
        email = emailFromName(representative)
        representative = prepName(representative)
        description = renoReason()
        values.append(
            [100000 + random.randrange(0, 2000), random.choice(branchIDs), description, random.choice(statuses),
             random.randrange(5000, 200000), representative[0], representative[1],
             representative[2], fake.phone_number(), email])
    print(insert("ExpansionProject", values))


def getMonetaryDonationData(amount, museumIDs, donorIDs):
    values = []
    for i in range(amount):
        amount = donationAmount()
        reason = donationReason()
        values.append(
            [random.randrange(0, 10000) + 20000, amount, reason, random.choice(donorIDs), random.choice(museumIDs)])
    print(insert("MonetaryDonation", values))


def getArtifactFromMet(artistName, minArtifacts, maxArtifacts):
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    object_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"

    # We use artistDisplayName=true to ensure we match the specific creator
    params = {'artistDisplayName': 'true', 'q': artistName}

    try:
        search_response = requests.get(search_url, params=params, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()
    except Exception as e:
        print(f"Search failed for {artistName}: {e}")
        return []

    # FIX: Robust check for objectIDs to prevent "NoneType" slicing errors
    object_ids = search_data.get('objectIDs')
    if object_ids is None or not isinstance(object_ids, list):
        return []

    # Determine safe amount to fetch
    actual_count = len(object_ids)
    num_to_fetch = min(actual_count, random.randint(minArtifacts, maxArtifacts))

    random.shuffle(object_ids)
    selected_ids = object_ids[:num_to_fetch]

    artifacts = []

    for obj_id in selected_ids:
        # Throttling to prevent 403 Forbidden rate-limit blocks
        time.sleep(1)

        try:
            obj_res = requests.get(f"{object_url}{obj_id}", timeout=10)

            # Handle potential 403 blocks with a longer cooldown
            if obj_res.status_code == 403:
                print(f"Rate limited on {obj_id}. Cooling down for 2s...")
                time.sleep(2)
                obj_res = requests.get(f"{object_url}{obj_id}", timeout=10)

            obj_res.raise_for_status()
            obj_data = obj_res.json()

            # Ensure obj_data is the dictionary we expect
            if not isinstance(obj_data, dict):
                continue

            # Helper to return None (SQL NULL) instead of empty strings
            def clean(val):
                return val if val else None

            # Create the individual artifact dictionary
            new_artifact = {
                "name": clean(obj_data.get("title")),
                "description": clean(obj_data.get("objectName")),
                "imageURL": clean(obj_data.get("primaryImage")),
                "style": clean(obj_data.get("period") or obj_data.get("classification")),
                "year": obj_data.get("objectEndDate"),
                "medium": clean(obj_data.get("medium"))
            }

            artifacts.append(new_artifact)

            # Progress check: Reference the DICTIONARY (new_artifact), not the LIST (artifacts)
            # F-string handles None types safely
            print(f"GOT ARTIFACT | {new_artifact['name']} by {artistName}")

        except Exception as e:
            print(f"Error skipping object {obj_id}: {e}")
            continue

    return artifacts


def getArtifactData(artistIDs, minArtifacts, maxArtifacts, archivistIDs):
    values = []
    artifactIDs = {}
    conditions = ['pristine', 'good', 'fair', 'poor', 'requires restoration']
    styleList = ['impressionism', 'pop art', 'rococo', 'modern', 'renaissance', 'realism']
    for artistName, artistID in artistIDs.items():
        artifactIDs[artistID] = []
        artifactFromMET = getArtifactFromMet(artistName, minArtifacts, maxArtifacts)
        for artifact in artifactFromMET:
            artifactID = 3000000 + random.randint(0, 10000)
            artifactIDs[artistID].append(artifactID)
            style = random.choice(styleList)
            values.append([artifactID, artistID, artifact["name"],
                           artifact["name"] + " by " + artistName + " is an artwork in the " + style + " style" ,
                           artifact["imageURL"], random.choice(conditions), style, artifact["year"],
                           artifact["medium"], random.choice(archivistIDs), artistID * 2 + 5])
    print(insert("Artifact", values))
    return artifactIDs


def getArtifactRequestData(amount, curatorIDs, exhibitIDs, donorIDs):
    values = []
    requestIDs = []
    for i in range(amount):
        startDate = getDateTime()
        requestID = random.randint(1000, 10000) * 1000
        requestIDs.append(requestID)
        startTimeArray = startDate.split("-")
        endTime = getDateTime(int(startTimeArray[0]))
        values.append([requestID, random.choice(exhibitIDs), random.choice(donorIDs), random.choice(curatorIDs),
                       startDate, endTime, random.choice(STATUSES)])
    print(insert("ArtifactRequest", values))
    return requestIDs


def getArtifactSetRelations(artifactIDs):
    values = []
    for artistID, artifactIDs in artifactIDs.items():
        for artifactID in artifactIDs:
            values.append([artistID, artifactID])
    print(insert("ArtifactSetRelation", values))


def getArtifactRequest(amount, artifactRequestIDs, artifactIDs):
    artifactIDsNoArtist = []
    for artistID, artifactIDList in artifactIDs.items():
        artifactIDsNoArtist += artifactIDList

    values = []
    for i in range(amount):
        values.append([random.choice(artifactRequestIDs), random.choice(artifactIDsNoArtist)])
    print(insert("ArtifactRequestRelations", values))
