--
-- File generated with SQLiteStudio v3.2.1 on ÷‹“ª 4‘¬ 1 10:02:31 2019
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: keys
CREATE TABLE keys ("key" VARCHAR (500) PRIMARY KEY UNIQUE NOT NULL, name VARCHAR (50) NOT NULL, type VARCHAR (50) NOT NULL, unit VARCHAR (20), units VARCHAR (100), remark TEXT, creator VARCHAR (50), create_date DATETIME, updator VARCHAR (50), update_date DATETIME);

-- Table: ss
CREATE TABLE ss ("key" VARCHAR (500) PRIMARY KEY UNIQUE NOT NULL REFERENCES keys ("key"), name VARCHAR (500) NOT NULL, "explain" TEXT, remark TEXT, creator VARCHAR (50) NOT NULL, create_date DATETIME NOT NULL, updator VARCHAR (50), update_date DATETIME);

-- Table: ss_formulas
CREATE TABLE ss_formulas ("key" VARCHAR (500) PRIMARY KEY NOT NULL REFERENCES keys ("key") , ss_key VARCHAR (500) REFERENCES ss ("key") NOT NULL, js_formulas TEXT, remark TEXT, creator VARCHAR (50), create_date DATETIME, updator VARCHAR (50), update_date DATETIME);

-- Table: ss_items
CREATE TABLE ss_items ("key" VARCHAR (500) PRIMARY KEY NOT NULL REFERENCES keys ("key") , p_key VARCHAR (500) REFERENCES ss_items ("key") NOT NULL, ss_key VARCHAR (500) REFERENCES ss ("key") NOT NULL, remark TEXT, creator VARCHAR (50), create_date DATETIME, update_date DATETIME);

-- Table: ss_scores
CREATE TABLE ss_scores ("key" VARCHAR (500) PRIMARY KEY NOT NULL REFERENCES keys ("key"), ss_key VARCHAR (500) REFERENCES ss ("key"), value VARCHAR (500) NOT NULL, score DECIMAL, remark TEXT, creator VARCHAR (50), create_date DATETIME, updator VARCHAR (50), update_date DATETIME);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
