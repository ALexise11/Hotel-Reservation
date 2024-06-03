-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 09, 2023 at 06:18 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crud`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  `role` enum('user','admin') DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `email`, `password`, `firstname`, `lastname`, `address`, `contact`, `role`) VALUES
(2, 'admin', 'admin@example.com', 'admin123', 'Admin User', 'admin', 'Admin Address', 'Admin Contact', 'admin'),
(24, 'prin', 'prin@gmail.com', 'prin123', 'johnray', 'merindo', 'cab', '09198811589', 'user'),
(25, 'john', 'john@gmail.com', '123', 'johnray', 'merindo', 'cab city', '09198811589', 'user'),
(26, 'merwin', 'mer@gmail.com', 'mer123', 'merwin', 'sividal', 'cab', '09090909090', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `id` int(11) NOT NULL,
  `room_number` int(11) NOT NULL,
  `check_in` date NOT NULL,
  `check_out` date NOT NULL,
  `guest_id` int(11) NOT NULL,
  `guest_firstname` varchar(100) DEFAULT NULL,
  `guest_lastname` varchar(100) DEFAULT NULL,
  `is_confirmed` tinyint(1) NOT NULL DEFAULT 0,
  `check_in_time` time DEFAULT NULL,
  `check_out_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`id`, `room_number`, `check_in`, `check_out`, `guest_id`, `guest_firstname`, `guest_lastname`, `is_confirmed`, `check_in_time`, `check_out_time`) VALUES
(56, 304, '2023-12-08', '2023-12-10', 3, NULL, NULL, 0, '03:00:00', '06:00:00'),
(57, 1, '2023-12-08', '2023-12-09', 3, NULL, NULL, 0, '09:09:00', '09:09:00'),
(58, 206, '2023-12-08', '2023-12-09', 3, NULL, NULL, 0, '20:00:00', '03:00:00'),
(59, 206, '2023-12-27', '2023-12-28', 3, 'RAY', NULL, 0, '03:33:00', '03:33:00'),
(60, 3, '2023-12-09', '2023-12-09', 0, NULL, NULL, 0, '06:06:00', '09:09:00'),
(62, 305, '2023-12-08', '2023-12-09', 0, NULL, NULL, 0, NULL, NULL),
(66, 3, '2023-12-16', '2023-12-17', 0, NULL, NULL, 0, '08:08:00', '08:08:00'),
(67, 1, '2023-12-30', '2023-12-30', 0, NULL, NULL, 0, '11:01:00', '13:33:00');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `room_number` int(11) NOT NULL,
  `room_name` varchar(255) NOT NULL,
  `room_type` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `is_available` tinyint(1) DEFAULT 1,
  `max_persons` int(11) DEFAULT NULL,
  `room_image_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_number`, `room_name`, `room_type`, `price`, `is_available`, `max_persons`, `room_image_path`) VALUES
(37, 1, 'RED ROOM', 'Single', 300, 1, 3, 'bg.jpg'),
(38, 2, 'ret', 'Double', 3333, 0, 2, 'bg.jpg'),
(39, 3, 'blue room', 'Double', 345, 1, 3, 'Sogo.png'),
(40, 89, 'eubert&crisden', 'Double', 123444, 1, 5, 'bg4.jpg'),
(43, 304, 'Tambio da great', 'Single', 30000, 1, 9, 'bg-med.jpg'),
(44, 305, 'SOGO', 'Single', 1200, 1, 3, 'register.jpg'),
(45, 206, 'Earth', 'Double', 1200, 1, 3, 'JODELL_R._BULACLAC_263.jpg'),
(46, 123, 'area', 'Single', 500, 1, 2, 'bg-med.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `id` int(10) UNSIGNED NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`id`, `full_name`, `email_address`, `password`, `city`, `country`, `created_at`) VALUES
(1, 'Inspector', 'inspector@gmail.com', 'inspector123', 'Gapan', 'Philippines', '0000-00-00 00:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `room_number` (`room_number`);

--
-- Indexes for table `user_details`
--
ALTER TABLE `user_details`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `user_details`
--
ALTER TABLE `user_details`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
