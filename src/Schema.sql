CREATE TABLE UserInfo(
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    CompanyCode TEXT NOT NULL,
    email TEXT NOT NULL,
    numrenders integer DEFAULT 0,
    --resetcode text,
    UNIQUE (Username, email)
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
CREATE TABLE invoices (
    id1 SERIAL PRIMARY KEY,
    file_name text NOT NULL,
    xml text NOT NULL,
    issue_date date,
    sender_name text,
    password text NOT NULL,
    buyer_name text,
    amount_payable decimal(20, 2),
    tax_payable decimal(20, 2),
    goods_payable decimal(20, 2),
    UNIQUE (File_Name, Password)
);