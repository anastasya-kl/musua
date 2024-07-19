-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2024 at 08:01 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `muzua`
--

-- --------------------------------------------------------

--
-- Table structure for table `artist_genres`
--

CREATE TABLE `artist_genres` (
  `id_artist` bigint(20) UNSIGNED NOT NULL,
  `id_genre` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `artist_genres`
--

INSERT INTO `artist_genres` (`id_artist`, `id_genre`) VALUES
(1, 1),
(2, 1),
(2, 2),
(3, 3),
(4, 1),
(4, 2),
(5, 3),
(6, 3),
(7, 4),
(7, 5),
(8, 1),
(8, 2),
(9, 4),
(9, 5),
(10, 3),
(10, 4),
(11, 1),
(11, 2),
(12, 1),
(12, 2),
(13, 1),
(13, 2),
(14, 3),
(15, 1),
(15, 2),
(16, 3),
(16, 4),
(17, 1),
(17, 2),
(18, 1),
(18, 2),
(19, 1),
(19, 2),
(20, 6),
(20, 7),
(21, 3),
(21, 4),
(22, 3),
(22, 4),
(23, 1),
(23, 2),
(24, 1),
(24, 2),
(25, 1),
(25, 2),
(26, 4),
(26, 5),
(27, 6),
(27, 7),
(27, 1),
(28, 3),
(29, 1),
(29, 2),
(30, 1),
(30, 2),
(31, 3),
(32, 3),
(33, 1),
(33, 2),
(34, 3),
(34, 8),
(35, 3),
(36, 1),
(36, 2),
(37, 3),
(37, 4),
(38, 1),
(38, 2),
(39, 1),
(39, 2),
(40, 1),
(40, 2),
(41, 4),
(41, 5),
(42, 3),
(42, 4),
(43, 1),
(43, 2),
(44, 1),
(44, 2),
(45, 3),
(45, 4),
(46, 1),
(46, 2),
(47, 1),
(47, 2),
(48, 4),
(48, 5),
(49, 1),
(49, 2),
(50, 1),
(50, 2),
(51, 1),
(51, 2),
(52, 1),
(52, 2),
(53, 3),
(53, 9),
(54, 9),
(54, 3),
(55, 4),
(55, 3),
(55, 9),
(56, 3),
(57, 1),
(57, 2),
(58, 1),
(58, 2),
(59, 3),
(60, 3),
(61, 1),
(61, 2),
(62, 1),
(62, 2),
(63, 3),
(64, 3),
(65, 1),
(65, 2),
(66, 1),
(66, 2),
(67, 1),
(67, 2),
(68, 1),
(68, 2),
(69, 1),
(69, 2),
(70, 1),
(70, 2),
(71, 3),
(72, 4),
(73, 3),
(74, 7),
(74, 3),
(75, 4),
(75, 5),
(76, 4),
(76, 5),
(77, 1),
(77, 2),
(78, 3),
(79, 3),
(80, 4),
(81, 4),
(81, 5),
(82, 1),
(82, 2),
(83, 1),
(83, 2),
(84, 1),
(84, 2),
(85, 3),
(86, 4),
(86, 5),
(87, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `artist_genres`
--
ALTER TABLE `artist_genres`
  ADD KEY `id_artist` (`id_artist`),
  ADD KEY `id_genre` (`id_genre`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `artist_genres`
--
ALTER TABLE `artist_genres`
  ADD CONSTRAINT `artist_genres_ibfk_1` FOREIGN KEY (`id_artist`) REFERENCES `artists` (`id`),
  ADD CONSTRAINT `artist_genres_ibfk_2` FOREIGN KEY (`id_genre`) REFERENCES `genres` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
