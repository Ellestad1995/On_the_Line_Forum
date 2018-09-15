USE `onthelinedb`;
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `customerNumber` int NOT NULL,
  `name` VARCHAR(32) NOT NULL
);

INSERT INTO customers (customerNumber, name)
  VALUES (6969, "Hello world");
