CREATE TABLE Customer
(
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Age INT
);

CREATE TABLE Policy
(
    PolicyID INT PRIMARY KEY,
    CustomerID INT,
    PolicyNumber VARCHAR(50),

    FOREIGN KEY(CustomerID)
        REFERENCES Customer(CustomerID)
);