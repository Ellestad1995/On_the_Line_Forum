CREATE DATABASE IF NOT EXISTS `onthelinedb`;

USE `onthelinedb`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(250) NOT NULL,
  `groupid` int(5) NOT NULL
);

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `groupid` int(5) NOT NULL,
  `groupname` varchar(20) NOT NULL
);

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
);

DROP TABLE IF EXISTS `thread`;
CREATE TABLE `thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `threadname` varchar(30) NOT NULL
);

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `content` varchar(10000) NOT NULL,
  `timestamp` varchar(50) NOT NULL
);

ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);
  ADD CONSTRAINT `group_id_ref_group` FOREIGN KEY (`groupid`) REFERENCES
  `groupid` (`group`) ON UPDATE CASCADE;

ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `thread`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `post`
  ADD PRIMARY KEY (`id`);
