CREATE TABLE `birds_image_eggs` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image_id` integer NOT NULL,
    `egg_id` integer NOT NULL,
    UNIQUE (`image_id`, `egg_id`)
)
;
CREATE TABLE `birds_image_birds` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image_id` integer NOT NULL,
    `bird_id` integer NOT NULL,
    UNIQUE (`image_id`, `bird_id`)
)
;
CREATE TABLE `birds_image` (
    `image_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(255),
    `image` varchar(100) NOT NULL,
    `width` integer,
    `height` integer,
    `created` datetime NOT NULL,
    `thumbnail2` varchar(100),
    `thumbnail` varchar(100)
)
;
ALTER TABLE `birds_image_eggs` ADD CONSTRAINT `image_id_refs_image_id_89390f83` FOREIGN KEY (`image_id`) REFERENCES `birds_image` (`image_id`);
ALTER TABLE `birds_image_birds` ADD CONSTRAINT `image_id_refs_image_id_125b0ee6` FOREIGN KEY (`image_id`) REFERENCES `birds_image` (`image_id`);
