CREATE DATABASE onthelinedb;

USE `onthelinedb`;


DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `customerNumber` int(11) NOT NULL,
  `customerName` varchar(50) NOT NULL,
  `contactLastName` varchar(50) NOT NULL,
  `contactFirstName` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `addressLine1` varchar(50) NOT NULL,
  `addressLine2` varchar(50) default NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) default NULL,
  `postalCode` varchar(15) default NULL,
  `country` varchar(50) NOT NULL,
  `salesRepEmployeeNumber` int(11) default NULL,
  `creditLimit` double default NULL,
  PRIMARY KEY  (`customerNumber`)
);
