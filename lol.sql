DROP TABLE IF EXISTS `summoner_spell`;
CREATE TABLE `summoner_spell` (
  `id` integer NOT NULL,
  `name` text(128),
  PRIMARY KEY (`id`)
);

INSERT INTO `summoner_spell` (`id`,`name`) VALUES (0,'Barrier');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (1,'Clarity');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (2,'Cleanse');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (3,'Disabled Summoner Spells');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (4,'Disabled Summoner Spells');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (5,'Exhaust');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (6,'Flash');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (7,'Ghost');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (8,'Heal');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (9,'Ignite');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (10,'Mark');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (11,'Nexus Siege: Siege Weapon Slot');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (12,'Nexus Siege: Siege Weapon Slot');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (13,'Poro Toss');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (14,'Smite');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (15,'Teleport');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (16,'To the King!');
INSERT INTO `summoner_spell` (`id`,`name`) VALUES (17,'Ultra (Rapidly Flung) Mark');