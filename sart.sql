-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 03, 2022 at 01:22 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sart`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `username` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `jabatan` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `name`, `password`, `jabatan`) VALUES
('Patrick', 'James Patrick Oentoro', '123', 'manager'),
('Noel', 'Noel Christevent Mandak', '123', 'sales_admin'),
('Tiff', 'Tiffany Sondakh', '123', 'finance_admin'),
('Ken', 'Khenny Fileo Suciady', '123', 'sales_admin');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `id_customer` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) DEFAULT NULL,
  `alamat` varchar(200) DEFAULT NULL,
  `no_telpon` varchar(20) DEFAULT NULL,
  `foto` text,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id_customer`, `nama`, `alamat`, `no_telpon`, `foto`, `status`) VALUES
(1, 'Elsa Nove Teresia', 'Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1720, lt. 8 ', '0812-2333-0000', 'images/elsa.png', 'active'),
(2, 'Audrey Josephine', 'Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1820, lt. 8 ', '0812-2333-0001', 'images/udey.png', 'non-active'),
(3, 'Evan Christopher', 'Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1926, lt. 8 ', '0812-2333-0002', 'images/evan.png', 'non-active'),
(4, 'Victor Chendra', 'Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1926, lt. 8 ', '0812-2333-0003', 'images/victor.png', 'active'),
(5, 'Grace Melissa Khoe Ping Ing', 'Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1705, lt. 8 ', '0812-2333-0004', 'images/ping.png', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `pelunasan`
--

DROP TABLE IF EXISTS `pelunasan`;
CREATE TABLE IF NOT EXISTS `pelunasan` (
  `id_pelunasan` int(11) NOT NULL AUTO_INCREMENT,
  `tgl_pelunasan` date DEFAULT NULL,
  `tot_pembayaran` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_pelunasan`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sale_invoice`
--

DROP TABLE IF EXISTS `sale_invoice`;
CREATE TABLE IF NOT EXISTS `sale_invoice` (
  `id_transaksi` int(11) NOT NULL AUTO_INCREMENT,
  `tgl_transaksi` date DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `id_customer` int(11) DEFAULT NULL,
  `id_pelunasan` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_transaksi`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sale_invoice`
--

INSERT INTO `sale_invoice` (`id_transaksi`, `tgl_transaksi`, `total`, `id_customer`, `id_pelunasan`) VALUES
(1, '2022-10-20', 123000, 2, NULL),
(2, '2022-10-20', 100000, 1, NULL),
(3, '2022-10-20', 21000, 5, NULL),
(4, '2022-10-20', 60000, 4, NULL),
(5, '2022-10-20', 200000, 3, NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
