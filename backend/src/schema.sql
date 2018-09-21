CREATE DATABASE IF NOT EXISTS `onthelinedb`;

USE `onthelinedb`;

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `groupid` int(5) NOT NULL,
  `groupname` varchar(20) NOT NULL,
  PRIMARY KEY (`groupid`)
);

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(300) NOT NULL,
  `groupid` int(5) NOT NULL,
  `token` varchar(500) NOT NULL,
  FOREIGN KEY (`groupid`) REFERENCES `group`(`groupid`) ON DELETE CASCADE,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `displayname` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `thread`;
CREATE TABLE `thread` (
  `id` int NOT NULL AUTO_INCREMENT,
  `threadname` varchar(30) NOT NULL,
  `categoryid` INT NOT NULL,
  FOREIGN KEY (`categoryid`) REFERENCES `category` (`id`) ON DELETE CASCADE,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `content` text NOT NULL,
  `timestamp` varchar(50) NOT NULL,
  `userid` int NOT NULL,
  `threadid` int NOT NULL,
  FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`threadid`) REFERENCES `thread` (`id`) ON DELETE CASCADE,
  PRIMARY KEY (`id`)
);
INSERT INTO `thread` (`threadname`, `categoryid`) VALUES ("Trump", "1"), ("Obama", "1"), ("Red-team", "2"), ("Blue team", "2");
INSERT INTO `category` (`displayname`) VALUES ("Politics"), ("Haking"), ("Cars"), ("Raid");
INSERT INTO `group` VALUES (1000, "admin"), (6969, "user");
INSERT INTO `user` (`username`, `password`, `salt`, `groupid`) VALUES ("AdminUser", "tmppassword", "2FGJM6GSDS", 1000);
