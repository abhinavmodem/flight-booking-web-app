-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 21, 2024 at 04:44 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flight`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `flight_id` int(11) NOT NULL,
  `booking_time` datetime NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `username`, `flight_id`, `booking_time`, `name`, `email`, `phone`, `seats`) VALUES
(3, '21071A1298', 2, '2024-02-20 20:14:46', 'abhinav', 'abhinavmodem@gmail.com', '09154224668', 8),
(5, '21071A1298', 20, '2024-02-21 08:46:23', 'abhinav', 'abhinavmodem@outlook.com', '09154224668', 8);

-- --------------------------------------------------------

--
-- Table structure for table `flights`
--

CREATE TABLE `flights` (
  `flight_id` int(11) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_city` varchar(50) NOT NULL,
  `arrival_city` varchar(50) NOT NULL,
  `departure_time` datetime NOT NULL,
  `available_seats` int(11) DEFAULT 60
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flights`
--

INSERT INTO `flights` (`flight_id`, `flight_number`, `departure_city`, `arrival_city`, `departure_time`, `available_seats`) VALUES
(1, '1234', 'hyderabad', 'hyderabad', '2024-02-21 17:08:46', 43),
(2, '456', 'chennai', 'hyderabad', '2024-02-21 15:41:41', 52),
(18, '82', 'blr', 'blr', '2024-02-22 08:15:00', 60),
(20, '1234', 'kkp', 'kkp', '2024-02-22 08:45:00', 52);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`) VALUES
(1, 'abhinav', 'abhinav1'),
(3, 'abhinav1', 'abhinav1'),
(4, '21071A1298', 'pbkdf2:sha256:600000$hy5iIMAYpc2cRrOZ$66f8b5832add48cbbd789d94d39b678e39792cb7b81eeaa3448ceaf5e54c7823');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`username`(20));

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `username` (`username`),
  ADD KEY `flight_id` (`flight_id`);

--
-- Indexes for table `flights`
--
ALTER TABLE `flights`
  ADD PRIMARY KEY (`flight_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `flights`
--
ALTER TABLE `flights`
  MODIFY `flight_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
