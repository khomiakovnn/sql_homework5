-- Create table for clients
CREATE TABLE client(id serial PRIMARY KEY, cl_name varchar(50) NOT NULL, surname varchar(50) NOT NULL, email varchar(100) NOT NULL);

-- Create table for phone numbers
CREATE TABLE phone(phone_number int PRIMARY KEY, client int REFERENCES client(id));

-- Create new client
INSERT INTO client(cl_name, surname, email)
VALUES ('John', 'Doe', 'john.doe@mail.com');

-- Add phone number for existing client
INSERT INTO phone(phone_number, client)
VALUES (1234567, 1);

-- Change client info
UPDATE client
SET cl_name = 'new name', surname = 'new surname', email = 'new email'
WHERE id = 1;

-- Delete existing phone number
DELETE FROM phone WHERE phone_number = 1234567;

-- Delete existing client
DELETE FROM client WHERE id = 1;

-- Finde client
SELECT cl_name FROM client WHERE id = 1;

-- Delete tables (clear)
DROP TABLE phone, client;