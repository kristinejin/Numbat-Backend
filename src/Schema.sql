CREATE TABLE UserInfo(
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    CompanyCode TEXT NOT NULL,
    email TEXT NOT NULL,
    numrenders integer 0,
    resetcode text,
    UNIQUE (Username, email),
);
CREATE TABLE senders(
    owner text NOT NULL,
    sender text NOT NULL
);
CREATE TABLE companyInfo(
    name VARCHAR(50) NOT NULL,
    abn VARCHAR(11) NOT NULL,
    street VARCHAR(30) NOT NULL,
    suburb VARCHAR(15) NOT NULL,
    postcode VARCHAR(4) NOT NULL,
    companyCode VARCHAR(20) NOT NULL,
    UNIQUE (name, companyCode)
);