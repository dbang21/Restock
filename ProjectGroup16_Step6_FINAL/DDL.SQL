SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

DROP TABLES IF EXISTS Households, Households_Members, Households_Inventories, Households_Items, Items_Types, Stores_Inventories, Stores;
--
-- Table structure for table `Households`
--
CREATE TABLE IF NOT EXISTS `Households` (
  `id_household` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `address` varchar(145) NOT NULL,
  PRIMARY KEY (`id_household`)
);

--
-- Table structure for table `Households_Members`
--
CREATE TABLE IF NOT EXISTS `Households_Members` (
  `id_household_member` int(11) NOT NULL AUTO_INCREMENT,
  `id_household` int(11),
  `name` varchar(45) NOT NULL,
  `runner_status` TINYINT NOT NULL,
  PRIMARY KEY (`id_household_member`),
  FOREIGN KEY (`id_household`) REFERENCES Households(`id_household`) ON DELETE CASCADE
);

--
-- Table structure for table `Households_Inventories`
--
CREATE TABLE IF NOT EXISTS `Households_Inventories` (
  `id_household_inventory` int(11) NOT NULL AUTO_INCREMENT,
  `id_household` int(11) NOT NULL,
  `id_item` int(11) NOT NULL,
  `amount_left` varchar(45) NOT NULL,
  `restock_status` TINYINT NOT NULL,
  PRIMARY KEY (`id_household_inventory`),
  FOREIGN KEY (`id_household`) REFERENCES Households(`id_household`) ON DELETE CASCADE,
  FOREIGN KEY (`id_item`) REFERENCES Households_Items(`id_item`) ON DELETE NO ACTION
);

--
-- Table structure for table `Households_Items`
--
CREATE TABLE IF NOT EXISTS `Households_Items` (
  `id_item` int(11) NOT NULL AUTO_INCREMENT,
  `id_item_type` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `best_if_used_by` DATE NOT NULL,
  PRIMARY KEY (`id_item`),
  FOREIGN KEY (`id_item_type`) REFERENCES Items_Types(`id_item_type`) ON DELETE NO ACTION
);

--
-- Table structure for table `Items_Types`
--
CREATE TABLE IF NOT EXISTS `Items_Types` (
  `id_item_type` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id_item_type`)
);

--
-- Table structure for table `Stores_Inventories`
--
CREATE TABLE IF NOT EXISTS `Stores_Inventories` (
  `id_item_type` int(11) NOT NULL,
  `id_store` int(11) NOT NULL,
  PRIMARY KEY (`id_item_type`, `id_store`)
);

--
-- Table structure for table `Stores`
--
CREATE TABLE IF NOT EXISTS `Stores` (
  `id_store` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `address` varchar(145) NOT NULL,
  `hours_open` varchar(45),
  PRIMARY KEY (`id_store`)
);


--
-- Data Insert into table `Households`
--
INSERT INTO Households(name, address)
VALUES ('Family', '101 Zip Blvd, New York City, New York, USA, 10010'),
    ('Couple', '102 Zip Blvd, Los Angeles, California, USA, 90210'),
    ('Roommates', '103 Zip Blvd, Chicago, Illinois, USA, 60018');
--
-- Data Insert into table `Items_Types`
--
INSERT INTO Items_Types(name)
VALUES ('Toiletries'),
    ('Cleaning Supplies'),
    ('Groceries'),
    ('Pharmacy'),
    ('Pet Supplies'),
    ('Gardening');
--
-- Data Insert into table `Stores`
--
INSERT INTO Stores(name, address, hours_open)
VALUES ('Amazonian', '101 Tesla Drive, Richland Hills, Texas, USA, 75890', '12am to 3am'),
    ('Home Depot', '123 Alphabet Rd, Someplace City, Texas, USA, 75891', '6am to 10am'),
    ('Get Tar', '10101 TopDown Ave, Psuedocode Woods, Texas, USA, 75892', '9am to 5pm'),
    ('Wallys Greens', '01010 BottomUp Blvd, Arrayville, Texas, USA, 75893', '2pm to 8pm; 10pm to 2am'),
    ('Costing Cocos', '2222 Dynamic St, Planning Valley, Texas, USA, 75894', 'Closed permanently'),
    ('Smartest Pets', '678 Backtracking Ln, Recursionton, Texas, USA, 75895', 'Open 24 hours');
--
-- Data Insert into table `Households_Members`
--
INSERT INTO Households_Members(id_household, name, runner_status)
VALUES ((select id_household from Households where name="Family"), 'Jane Doe', 1),
    ((select id_household from Households where name="Family"), 'John Doe', 0),
    ((select id_household from Households where name="Family"), 'Son Doe', 0),
    ((select id_household from Households where name="Family"), 'Daughter Doe', 0),
    ((select id_household from Households where name="Couple"), 'Maureen Lady', 1),
    ((select id_household from Households where name="Couple"), 'Barbara Waddingham', 0),
    ((select id_household from Households where name="Roommates"), 'Nathaniel Archibald', 1),
    ((select id_household from Households where name="Roommates"), 'Alex Lyndell', 0),
    ((select id_household from Households where name="Roommates"), 'Sasha Grace', 0);
--
-- Data Insert into table `Households_Items`
--
INSERT INTO Households_Items(name, id_item_type, best_if_used_by)
VALUES ('Toilet Paper', (select id_item_type from Items_Types where name="Toiletries"), "2022-11-26"),
    ('Toothpaste', (select id_item_type from Items_Types where name="Toiletries"), "2022-12-31"),
    ('Shampoo', (select id_item_type from Items_Types where name="Toiletries"), "2024-04-11"),
    ('Milk', (select id_item_type from Items_Types where name="Groceries"), "2022-05-07"),
    ('Coffee Beans', (select id_item_type from Items_Types where name="Groceries"), "2028-10-10"),
    ('Bananas', (select id_item_type from Items_Types where name="Groceries"), "2022-05-02"),
    ('Yogurt', (select id_item_type from Items_Types where name="Groceries"), "2022-05-12"),
    ('Dog Food', (select id_item_type from Items_Types where name="Pet Supplies"), "2022-07-15"),
    ('Doggy Bags', (select id_item_type from Items_Types where name="Pet Supplies"), "2029-02-25"),
    ('Paw Wipes', (select id_item_type from Items_Types where name="Pet Supplies"), "2021-08-17"),
    ('Chlorox', (select id_item_type from Items_Types where name="Cleaning Supplies"), "2014-06-05"),
    ('Windex', (select id_item_type from Items_Types where name="Cleaning Supplies"), "2018-12-12"),
    ('Laundry Detergent', (select id_item_type from Items_Types where name="Cleaning Supplies"), "2022-03-15"),
    ('Advil', (select id_item_type from Items_Types where name="Pharmacy"), "2023-01-30"),
    ('Bandaids', (select id_item_type from Items_Types where name="Pharmacy"), "2026-11-09"),
    ('Fertilizer', (select id_item_type from Items_Types where name="Gardening"), "2027-07-01"),
    ('Pesticide', (select id_item_type from Items_Types where name="Gardening"), "2022-03-30");
--
-- Data Insert into table `Households_Inventories`
--
INSERT INTO Households_Inventories(id_household, id_item, amount_left, restock_status)
VALUES ((select id_household from Households where name="Family"), (select id_item from Households_Items where name="Fertilizer"), 'Empty', 1),
    ((select id_household from Households where name="Family"), (select id_item from Households_Items where name="Toothpaste"), 'Fully Stocked', 0),
    ((select id_household from Households where name="Family"), (select id_item from Households_Items where name="Windex"), 'Empty', 1),
    ((select id_household from Households where name="Family"), (select id_item from Households_Items where name="Bandaids"), 'Empty', 1),
    ((select id_household from Households where name="Family"), (select id_item from Households_Items where name="Paw Wipes"), 'Running Low', 1),
    ((select id_household from Households where name="Couple"), (select id_item from Households_Items where name="Shampoo"), 'Still Plenty', 0),
    ((select id_household from Households where name="Couple"), (select id_item from Households_Items where name="Yogurt"), 'Running Low', 1),
    ((select id_household from Households where name="Couple"), (select id_item from Households_Items where name="Dog Food"), 'Empty', 1),
    ((select id_household from Households where name="Roommates"), (select id_item from Households_Items where name="Milk"), 'Still Plenty', 0),
    ((select id_household from Households where name="Roommates"), (select id_item from Households_Items where name="Detergent"), 'Running Low', 1),
    ((select id_household from Households where name="Roommates"), (select id_item from Households_Items where name="Coffee Beans"), 'Empty', 1),
    ((select id_household from Households where name="Roommates"), (select id_item from Households_Items where name="Toilet Paper"), 'Empty', 1);
--
-- Data Insert into table `Stores_Inventories`
--
INSERT INTO Stores_Inventories(id_item_type, id_store)
VALUES ((select id_item_type from Items_Types where name="Toiletries"), (select id_store from Stores where name="Amazonian")),
    ((select id_item_type from Items_Types where name="Toiletries"), (select id_store from Stores where name="Get Tar")),
    ((select id_item_type from Items_Types where name="Cleaning Supplies"), (select id_store from Stores where name="Get Tar")),
    ((select id_item_type from Items_Types where name="Groceries"), (select id_store from Stores where name="Get Tar")),
    ((select id_item_type from Items_Types where name="Groceries"), (select id_store from Stores where name="Costing Cocos")),
    ((select id_item_type from Items_Types where name="Pharmacy"), (select id_store from Stores where name="Wallys Greens")),
    ((select id_item_type from Items_Types where name="Pet Supplies"), (select id_store from Stores where name="Smartest Pets")),
    ((select id_item_type from Items_Types where name="Gardening"), (select id_store from Stores where name="Home Depot"));

SET FOREIGN_KEY_CHECKS=1;
COMMIT;