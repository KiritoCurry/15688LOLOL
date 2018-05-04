DROP TABLE IF EXISTS `Champion`;
CREATE TABLE `Champion` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `name` text(50) NOT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `Match`;
CREATE TABLE `Match` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `duration` integer(128) NOT NULL,
  `version` text(128) NOT NULL,
  `season` text(30) NOT NULL,
  `region` text(30) NOT NULL,
  `match_type` text(20) NOT NULL,
  `creation_time` integer(128) NOT NULL,
  `tier` text(128),
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `Participants`;
CREATE TABLE `Participants` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `summoner_id` integer(128) NOT NULL,
  `match_id` integer(128) NOT NULL,
  `champion_id` integer(128) NOT NULL,
  `team_id` integer(128) NOT NULL,
  `side` text(20) NOT NULL,
  `win` integer(1) NOT NULL,
  `role` text(30) NOT NULL,
  `lane` text(30) NOT NULL,
  `summoner_spell1` integer(5) NOT NULL,
  `summoner_spell2` integer(5) NOT NULL,
  `levels` integer(10) NOT NULL,
  `items` text(128) NOT NULL,
  `kills` integer(10) NOT NULL,
  `deaths` integer(10) NOT NULL,
  `assists` integer(10) NOT NULL,
  `kda` float(32) NOT NULL,
  `turret_kill` integer(10) NOT NULL,
  `first_tower_kill` integer(1) NOT NULL,
  `damage_dealt_to_turrets` float(32) NOT NULL,
  `first_blood_kill` integer(1) NOT NULL,
  `doublekills` integer(10) NOT NULL,
  `triplekills` integer(10) NOT NULL,
  `quadrakills` integer(10) NOT NULL,
  `pentakills` integer(10) NOT NULL,
  `killing_sprees` integer(10) NOT NULL,
  `inhibitor_kills` integer(10) NOT NULL,
  `gold_earned` float(32) NOT NULL,
  `gold_spent` float(32) NOT NULL,
  `largest_killing_spree` integer(10) NOT NULL,
  `largest_critical_strike` float(32) NOT NULL,
  `largest_multi_kill` integer(32) NOT NULL,
  `longest_time_spent_living` integer(128) NOT NULL,
  `magic_damage_dealt_to_champions` float(32) NOT NULL,
  `magical_damage_taken` float(32) NOT NULL,
  `neutral_minions_killed` integer(32) NOT NULL,
  `neutral_minions_killed_enemy_jungle` integer(32) NOT NULL,
  `physical_damage_dealt_to_champions` float(32) NOT NULL,
  `physical_damage_taken` float(32) NOT NULL,
  `sight_wards_bought_in_game` integer(32) NOT NULL,
  `total_damage_dealt_to_champions` float(32) NOT NULL,
  `total_damage_taken` float(32) NOT NULL,
  `total_heal` float(32) NOT NULL,
  `total_minions_killed` integer(32) NOT NULL,
  `true_damage_dealt_to_champions` float(32) NOT NULL,
  `true_damage_taken` float(32) NOT NULL,
  `vision_wards_bought_in_game` integer(20) NOT NULL,
  `wards_killed` integer(32) NOT NULL,
  `wards_placed` integer(32) NOT NULL,
  `time_CCing_others` integer(32) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (summoner_id) REFERENCES Summoner (id),FOREIGN KEY (match_id) REFERENCES "Match" (id),FOREIGN KEY (champion_id) REFERENCES Champion (id),FOREIGN KEY (team_id) REFERENCES Team (id),FOREIGN KEY (summoner_spell1) REFERENCES summoner_spell (id),FOREIGN KEY (summoner_spell2) REFERENCES summoner_spell (id)
);


DROP TABLE IF EXISTS `Summoner`;
CREATE TABLE `Summoner` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `name` text(128) NOT NULL,
  `region` text(25) NOT NULL,
  `level` integer(10) NOT NULL,
  `rank_last_season` char(20),
  `rank_this_season` char(20),
  `is_crawler` integer(1) NOT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `Team`;
CREATE TABLE `Team` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `match_id` integer(128) NOT NULL,
  `side` text(20) NOT NULL,
  `win` integer(1) NOT NULL,
  `dragon_kills` integer(10) NOT NULL,
  `baron_kills` integer(10) NOT NULL,
  `inhibitor_kills` integer(10) NOT NULL,
  `tower_kills` integer(10) NOT NULL,
  `first_blood` integer(1) NOT NULL,
  `first_dragon` integer(1) NOT NULL,
  `first_baron` integer(1) NOT NULL,
  `first_tower` integer(1) NOT NULL,
  `first_rift_herald` integer(1) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (match_id) REFERENCES "Match" (id) on delete set null
);


DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `name` text(50) NOT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `kil_champion_event`;
CREATE TABLE `kil_champion_event` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `match_id` char(128),
  `victim_id` integer(128),
  `killer_id` integer(128),
  `happen_time` integer(128),
  PRIMARY KEY (`id`),
  FOREIGN KEY (match_id) REFERENCES "Match" (id)
);


DROP TABLE IF EXISTS `kill_monster_event`;
CREATE TABLE `kill_monster_event` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `match_id` integer(128),
  `timestamp` integer(128),
  `killer_id` integer(128),
  `monster_type` text(50),
  PRIMARY KEY (`id`),
  FOREIGN KEY (match_id) REFERENCES "Match" (id)
);


DROP TABLE IF EXISTS `participant_timeline`;
CREATE TABLE `participant_timeline` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `summoner_id` integer(128) NOT NULL,
  `match_id` integer(128) NOT NULL,
  `creeps_per_min_deltas` float(32),
  `cs_diff_per_min_deltas` float(32),
  `damage_taken_diff_per_min_deltas` float(32),
  `gold_per_min_deltas` float(32),
  `damage_taken_per_min_deltas` float(32),
  `xp_diff_per_min_deltas` float(32),
  `xp_per_min_deltas` float(128),
  PRIMARY KEY (`id`),
  FOREIGN KEY (summoner_id) REFERENCES Summoner (id),FOREIGN KEY (match_id) REFERENCES "Match" (id)
);


DROP TABLE IF EXISTS `summoner_spell`;
CREATE TABLE `summoner_spell` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `name` text(128),
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `team_ban`;
CREATE TABLE `team_ban` (
  `id` integer NOT NULL AUTO_INCREMENT,
  `team_id` integer(128) NOT NULL,
  `match_id` integer(128) NOT NULL,
  `ban_champion` integer(128) NOT NULL,
  `ban_turn` integer(2),
  PRIMARY KEY (`id`),
  FOREIGN KEY (team_id) REFERENCES Team (id),FOREIGN KEY (match_id) REFERENCES "Match" (id),FOREIGN KEY (ban_champion) REFERENCES Champion (id)
);

