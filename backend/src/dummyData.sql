INSERT INTO `category` (`displayname`) VALUES ("Politics"), ("Haking"), ("Cars"), ("Raid");
INSERT INTO `thread` (`threadname`, `categoryid`) VALUES ("Trump", 1), ("Obama", 1), ("Red-team", 2), ("Blue team", 2);
INSERT INTO `usergroups` VALUES (1000, "admin"), (6969, "user");
INSERT INTO `user` (`username`, `password`, `groupid`, `token`) VALUES ("AdminUser", "tmppassword", 1000, "6969testtoken6969");
INSERT INTO `user` (`username`, `password`, `groupid`, `token`) VALUES ("Ola Nordman", "easypass", 6969, "6969testtoken6969");
INSERT INTO `post` (`title`, `content`, `timestamp`, `userid`, `threadid`) VALUES ("Jeg elsker trump", "Dette er en lang tekst hvor jeg skriver om hvor mye jeg liker trump", "insert timestamp from python code", 1, 1);
