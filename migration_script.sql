-- ----------------------------------------------------------------------------
-- MySQL Workbench Migration
-- Migrated Schemata: scoring_system
-- Source Schemata: scoring_system
-- Created: Sun Mar 31 23:15:42 2019
-- Workbench Version: 8.0.15
-- ----------------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------
-- Schema scoring_system
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `scoring_system` ;
CREATE SCHEMA IF NOT EXISTS `scoring_system` ;

-- ----------------------------------------------------------------------------
-- Table scoring_system.keys
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoring_system`.`keys` (
  `key` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `unit` VARCHAR(45) NULL DEFAULT NULL,
  `units` VARCHAR(45) NULL DEFAULT NULL,
  `type` VARCHAR(45) NULL DEFAULT NULL,
  `p_key` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `key_UNIQUE` (`key` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table scoring_system.ss
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoring_system`.`ss` (
  `key` INT(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `key_UNIQUE` (`key` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table scoring_system.ss_formulas
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoring_system`.`ss_formulas` (
  `key` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`key`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table scoring_system.ss_item_scores
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoring_system`.`ss_item_scores` (
  `key` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`key`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table scoring_system.ss_items
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoring_system`.`ss_items` (
  `key` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`key`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table scoring_system.ss_results
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoring_system`.`ss_results` (
  `key` VARCHAR(50) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`key`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
SET FOREIGN_KEY_CHECKS = 1;
