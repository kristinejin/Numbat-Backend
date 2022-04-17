CREATE TABLE UserInfo(
    Username VARCHAR(12) NOT NULL,
    Password VARCHAR(12) NOT NULL,
    UNIQUE (Username)
);
CREATE TABLE senders(
    owner VARCHAR(20) NOT NULL,
    sender VARCHAR(20) NOT NULL
CREATE TABLE companyInfo(
    name VARCHAR(50) NOT NULL,
    abn VARCHAR(11) NOT NULL,
    street VARCHAR(30) NOT NULL,
    suburb VARCHAR(15) NOT NULL,
    postcode VARCHAR(4) NOT NULL,
    companyCode VARCHAR(20) NOT NULL,
    UNIQUE (name, companyCode)
);