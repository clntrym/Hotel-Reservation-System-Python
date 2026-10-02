-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2026 at 04:13 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `rev_id` int(11) NOT NULL,
  `room_id` int(11) DEFAULT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `type_id` varchar(255) DEFAULT NULL,
  `num_id` varchar(255) DEFAULT NULL,
  `checkin` date DEFAULT NULL,
  `checkout` date DEFAULT NULL,
  `payment_method` varchar(255) DEFAULT NULL,
  `payment_amount` decimal(10,2) NOT NULL,
  `status` enum('Confirmed','Checked-in','Checked-out','Cancelled') DEFAULT 'Confirmed',
  `created_at` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`rev_id`, `room_id`, `firstname`, `lastname`, `email`, `phone`, `type_id`, `num_id`, `checkin`, `checkout`, `payment_method`, `payment_amount`, `status`, `created_at`) VALUES
(3, 6, 'cleint', 'salarda', 'cleint@gmail.com', '09123456789', 'Passport ID', '987324', '2026-03-26', '2026-03-28', 'Cash', 6000.00, 'Cancelled', '2026-03-25'),
(4, 4, 'theo', 'taran', 'taran@gmail.com', '09123456789', 'Driving Lisence ID', '4314354234', '2026-03-26', '2026-03-29', 'Cash', 4500.00, 'Checked-out', '2026-03-25'),
(5, 2, 'james', 'pavia', 'pavia@gmail.com', '09123456789', 'National ID', '087743', '2026-03-26', '2026-03-29', 'Cash', 6000.00, 'Checked-out', '2026-03-25'),
(6, 5, 'jayvee', 'joson', 'joson@gmail.com', '09123456789', 'Passport ID', '87768423', '2026-03-28', '2026-03-29', 'Gcash', 1500.00, 'Checked-out', '2026-03-26'),
(7, 11, 'emar', 'andaya', 'andaya@gmail.come', '09123456789', 'Driving Lisence ID', '9848782', '2026-03-28', '2026-03-31', 'Bank', 4500.00, 'Checked-out', '2026-03-26'),
(8, 10, 'steve', 'tev', 'tev@gmail.com', '09123456789', 'National ID', '9849832', '2026-03-29', '2026-03-30', 'Cash', 1500.00, 'Cancelled', '2026-03-26'),
(9, 4, 'cleint', 'salarda', 'salarda@gmail.com', '09123456789', 'National ID', '43432432', '2026-03-27', '2026-03-29', 'Cash', 3000.00, 'Checked-in', '2026-03-27'),
(10, 10, 'dsa', 'dsa', 'dsa@gmail.com', '09123456789', 'Passport ID', '32718471', '2026-03-27', '2026-03-28', 'Cash', 1500.00, 'Confirmed', '2026-03-27'),
(11, 2, 'cleint', 'salarda', 'cleint@gmail.com', '09123456789', 'National ID', '', '2026-03-27', '2026-03-28', 'Cash', 2000.00, 'Checked-in', '2026-03-27'),
(12, 11, 'james', 'pavia', 'james@gmail.com', '09123456789', 'Passport ID', '97378431', '2026-03-28', '2026-03-30', 'Cash', 3000.00, 'Checked-in', '2026-03-28'),
(13, 12, 'carvine', 'movido', 'movido@gmail.com', '09123456789', 'Passport ID', '42431433', '2026-03-28', '2026-03-29', 'Gcash', 2000.00, 'Checked-out', '2026-03-28'),
(14, 12, 'theo', 'taran', 'taran@gmail.com', '09123456789', 'Driving Lisence ID', '98783874', '2026-03-28', '2026-03-30', 'Gcash', 4000.00, 'Cancelled', '2026-03-28');

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `room_id` int(11) NOT NULL,
  `room_number` varchar(255) DEFAULT NULL,
  `room_floor` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `price` int(255) DEFAULT NULL,
  `capacity` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`room_id`, `room_number`, `room_floor`, `category`, `status`, `price`, `capacity`) VALUES
(2, '202', '2', 'Deluxe', 'Occupied', 2000, 2),
(3, '203', '2', 'Deluxe', 'Occupied', 2000, 2),
(4, '102', '1', 'Standard', 'Occupied', 1500, 2),
(5, '103', '1', 'Standard', 'Available', 1500, 2),
(6, '302', '3', 'Suite', 'Available', 3000, 2),
(10, '101', '1', 'Standard', 'Occupied', 1500, 2),
(11, '104', '1', 'Standard', 'Occupied', 1500, 2),
(12, '201', '2', 'Deluxe', 'Available', 2000, 2),
(13, '304', '3', 'Suite', 'Available', 3000, 5);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `gmail` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `firstname`, `lastname`, `gmail`, `role`, `username`, `password`, `status`) VALUES
(1, 'cleint raymund', 'salarda', 'cleint@gmail.com', 'Admin', 'admin', '$2b$12$NMz7wUAAwJAEbBukvMTeSu9oblTlSKvv854kMN5.lTOjo1sAVWkFy', 'Active'),
(2, 'cleint', 'salarda', 'cleint@gmail.com', 'Admin', 'cleint', 'admin123', 'Active'),
(3, 'cleint', 'salarda', 'cleintraymundsalarda@gmail.com', 'Admin', 'admin123', '$2b$12$1nC8b9vtQqP2KabKw2eq0.t1U1pKa0s9sea8yBKR1BEDZ6wGdbWzC', 'Active'),
(4, 'theo james', 'taran', 'theo@gmail.com', 'Front Desk', 'theo12', '$2b$12$Sa9KfxjPUXaDP2TMks3s2O/kgQkh02Jarkn4exgg8HR0JKjj0yA2i', 'Active'),
(5, 'james', 'pavia', 'pavia@gmail.com', 'Front Desk', 'pavia', '$2b$12$gIo/yivZANCOLD0ABMfV5eeG33AQdkxe2zAETlgUm7yw2n6iIscLG', 'Active'),
(6, 'jayvee', 'joson', 'sukal@gmail.com', 'Front Desk', 'sukal', '$2b$12$cVPt28drZ5wOWxMG6AmoP.RyFIS00XF.jkDEPV4wopyZTuRpvcbM2', 'Active'),
(7, 'emar', 'andaya', 'andaya@gmail.com', 'Admin', 'emar', '$2b$12$1VP64cfKMMf5k6Mq43UWW.S.vt/KYqpG3jj.ZumBu1aRPi/ePynNW', 'Inactive'),
(8, 'carvine', 'movido', 'carvinemovido@gmail.com', 'Front Desk', 'wreck', '$2b$12$aOg/D3ETWadS24EZp/Zzi.fodUcjQ3bWck6GqcfN.fVQ7nPd.n49y', 'Active'),
(14, 'arron', 'navarro', 'ron@gmail.com', 'Front Desk', 'ron', '$2b$12$NVM6OdmbIUyh3URynDbTjeucQx2TQOkI0cZaTQ4ZHHmfcj8viz/ja', 'Inactive'),
(15, 'ambin', 'movido', 'movido@gmail.com', 'Admin', 'ambin', '$2b$12$T19ml9pSKImpgH3TM/8HzOtPcYOHdJmN41vaAMGLj/R/BkQr2au2y', 'Active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`rev_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`room_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reservation`
--
ALTER TABLE `reservation`
  MODIFY `rev_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `room`
--
ALTER TABLE `room`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `room_id` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
