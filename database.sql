SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `student_id` int() NOT NULL,
  `name` char(100) NOT NULL,
  `dob` date NOT NULL,
  `contact_info` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `students` (`id`,`user_id`,`name`, `dob`, `contact_info`) VALUES
(23, '1000','motech noel', '2002-02-01', '+255752541568'),
(24,'1001' ,'Thiago Moses', '2002-02-03', '0712541669'),
(25, '1002','Saratex Marie', '2002-02-08', '0712541669'),
(26, '1003','Kamonyo Kiiza', '2002-02-07', '+255752541568');

ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;
COMMIT;
