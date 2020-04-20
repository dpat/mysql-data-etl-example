DROP DATABASE IF EXISTS `ca_business`;
CREATE DATABASE `ca_business`;
USE `ca_business`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `yelp_user_id` VARCHAR(255) UNIQUE NOT NULL,
  `user_url` VARCHAR(255) UNIQUE NOT NULL,
  `created_at` TIMESTAMP DEFAULT NOW()
);

DROP TABLE IF EXISTS `locations`;
CREATE TABLE `locations` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `location` VARCHAR(255) UNIQUE NOT NULL,
  `created_at` TIMESTAMP DEFAULT NOW()
);

DROP TABLE IF EXISTS `businesses`;
CREATE TABLE `businesses` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) UNIQUE NOT NULL,
  `rating` FLOAT,
  `wiki_url` VARCHAR(255),
  `parking` BOOLEAN NOT NULL,
  `open_weekends` BOOLEAN NOT NULL,
  `location_id` INTEGER NOT NULL,
  `most_recent_review_id` INTEGER,
  `created_at` TIMESTAMP DEFAULT NOW(),
  CONSTRAINT FOREIGN KEY(`location_id`) REFERENCES `locations` (`id`),
  CONSTRAINT FOREIGN KEY(`most_recent_review_id`) REFERENCES `users` (`id`)
);
