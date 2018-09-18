CREATE DATABASE IF NOT EXISTS `onthelinedb`;

USE `onthelinedb`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(250) NOT NULL,
  `salt` varchar(20) NOT NULL,
  `gid` int(5) NOT NULL
);

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `groupid` int(5) NOT NULL,
  `groupname` varchar(20) NOT NULL
);

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `displayname` varchar(30) NOT NULL
);

DROP TABLE IF EXISTS `thread`;
CREATE TABLE `thread` (
  `id` int(11) NOT NULL,
  `threadname` varchar(30) NOT NULL
);

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL,
  `title` varchar(30) NOT NULL,
  `content` varchar(10000) NOT NULL,
  `timestamp` varchar(50) NOT NULL
);

ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `thread`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `group`
  ADD PRIMARY KEY (`groupid`);

ALTER TABLE `post`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD CONSTRAINT `group_refers_id` FOREIGN KEY (`gid`) REFERENCES
  `groupid` (`group`) ON UPDATE CASCADE;

ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `thread`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `group`
  MODIFY `groupid` int(11) NOT NULL AUTO_INCREMENT;


INSERT INTO group (groupid, groupname)
  VALUES (1000, "admin"), (6969, "user");

INSERT INTO user (username, groupid)
  VALUES ("AdminUser", 1000), ("Normaluser", 6969);
