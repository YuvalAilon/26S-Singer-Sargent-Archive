DROP DATABASE IF EXISTS `Singer-Sargent-Archive`;

CREATE DATABASE IF NOT EXISTS `Singer-Sargent-Archive`;

USE `Singer-Sargent-Archive`;

CREATE TABLE Roles(
    roleID int PRIMARY KEY ,
    roleName varchar(50)
);

CREATE TABLE MuseumWorker(
    employeeID int PRIMARY KEY,
    firstName varchar(50),
    middleName varchar(50),
    lastName varchar(50),
    email varchar(50),
    phone varchar(20),
    roleID int,
    FOREIGN KEY (roleID) REFERENCES Roles (roleID)
);

CREATE TABLE MuseumBranch(
    branchID int PRIMARY KEY,
    branchName varchar(50),

    contactFirstName varchar(50),
    contactMiddleName varchar(50),
    contactLastName varchar(50),
    contactPhone varchar(20),
    contactEmail varchar(50),

    street varchar(50),
    city varchar(30),
    zip varchar(15)
);

CREATE TABLE Galleries(
    galleryID int,
    branchID int NOT NULL,
    name varchar(50),
    wing varchar(50),
    artworkCapacity int,
    PRIMARY KEY (galleryID, branchID),
    FOREIGN KEY (branchID) REFERENCES MuseumBranch (branchID)
);

CREATE TABLE Exhibits(
    exhibitID int PRIMARY KEY,
    galleryID int NOT NULL,
    branchID int NOT NULL,
    name varchar(50),
    description text,
    dateStart DATETIME NOT NULL,
    dateEnd DATETIME,
    FOREIGN KEY (galleryID, branchID) REFERENCES Galleries (galleryID, branchID)
);

CREATE TABLE Donors(
    donorID int PRIMARY KEY,
    organizationName varchar(100),
    email varchar(50),

    contactTitle varchar(10),
    contactFirstName varchar(50),
    contactMiddleName varchar(50),
    contactLastName varchar(50),

    street varchar(30),
    city varchar(30),
    state varchar(2),
    zip varchar(10)
);

CREATE TABLE ArtifactRequest(
    requestID int PRIMARY KEY ,
    exhibitID int,
    loaningDonorID int,
    requestingEmployeeID int NOT NULL ,
    loanDateStart DATETIME NOT NULL ,
    loanDateEnd DATETIME NOT NULL,
    status ENUM('pending', 'approved', 'denied', 'ongoing') NOT NULL,
    FOREIGN KEY (loaningDonorID) REFERENCES Donors (donorID),
    FOREIGN KEY (requestingEmployeeID) REFERENCES MuseumWorker (employeeID),
    FOREIGN KEY (exhibitID) REFERENCES Exhibits (exhibitID)
);

CREATE TABLE ExpansionProject(
    projectID int PRIMARY KEY,
    headedByBranchID int NOT NULL ,
    description text,
    status ENUM('pending', 'approved', 'denied', 'ongoing') NOT NULL,
    costDollarAmount int,
    contactName varchar(50),
    contactphone varchar(20),
    contactEmail varchar(50),

    FOREIGN KEY (headedByBranchID) REFERENCES MuseumBranch (branchID)

);

CREATE TABLE Artist(
    artistID int PRIMARY KEY ,
    firstName varchar(50),
    middleName varchar(50),
    lastName varchar(50),
    bio text
);

CREATE TABLE Artifact(
    artifactID int PRIMARY KEY,
    artistID int,
    name varchar(50) NOT NULL ,
    description text,
    imageURL text,
    artifactCondition ENUM('pristine', 'good', 'fair', 'poor', 'requires restoration'),
    style varchar(50),
    createdYear int,
    medium varchar(50),
    archivedByEmployeeID int NOT NULL ,
    displayedInExhibitID int,
    FOREIGN KEY (artistID) REFERENCES Artist (artistID),
    FOREIGN KEY (archivedByEmployeeID) REFERENCES MuseumWorker (employeeID),
    FOREIGN KEY (displayedInExhibitID) REFERENCES Exhibits (exhibitID)
);

CREATE TABLE ArtifactSet(
    artifactSetID int PRIMARY KEY,
    name varchar(100),
    description text
);

CREATE TABLE ArtifactSetRelations(
    artifactSetID int,
    artifactID int,
    PRIMARY KEY (artifactSetID, artifactID),
    FOREIGN KEY (artifactID) REFERENCES Artifact (artifactID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (artifactSetID) REFERENCES ArtifactSet (artifactSetID)
);

CREATE TABLE ArtifactRequestRelations(
    requestID int,
    artifactID int,
    PRIMARY KEY (requestID, artifactID),
    FOREIGN KEY (artifactID) REFERENCES Artifact (artifactID) ON UPDATE CASCADE ON DELETE CASCADE ,
    FOREIGN KEY (requestID) REFERENCES ArtifactRequest (requestID)
);

CREATE TABLE MonetaryDonation(
    monetaryDonationID int PRIMARY KEY,
    amount int,
    reason text,
    donorID int NOT NULL ,
    branchID int,
    FOREIGN KEY (donorID) REFERENCES Donors (donorID),
    FOREIGN KEY (branchID) REFERENCES MuseumBranch (branchID)
);