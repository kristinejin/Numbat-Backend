CREATE TABLE UserInfo(
    Username VARCHAR(12) NOT NULL,
    Password VARCHAR(12) NOT NULL,
    UNIQUE (Username)
);