-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: digigirls_db
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.23.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `course_image_url` varchar(255) DEFAULT NULL,
  `course_description` text,
  `course_duration` varchar(100) DEFAULT NULL,
  `prerequisites` text,
  `lesson_1_title` varchar(255) DEFAULT NULL,
  `lesson_1_content` text,
  `lesson_1_duration` varchar(50) DEFAULT NULL,
  `lesson_1_instructor` varchar(255) DEFAULT NULL,
  `lesson_2_title` varchar(255) DEFAULT NULL,
  `lesson_2_content` text,
  `lesson_2_duration` varchar(50) DEFAULT NULL,
  `lesson_2_instructor` varchar(255) DEFAULT NULL,
  `lesson_3_title` varchar(255) DEFAULT NULL,
  `lesson_3_content` text,
  `lesson_3_duration` varchar(50) DEFAULT NULL,
  `lesson_3_instructor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Introduction to HTML and CSS','path-to-course-image.jpg','Learn the basics of HTML and CSS to create simple and beautiful web pages.','4 weeks','None','Introduction to HTML','Learn the basics of HTML...','1 week','John Doe','Introduction to CSS','Learn the basics of CSS...','1 week','Jane Smith','Building Web Pages','Create simple and beautiful web pages...','2 weeks','Bob Johnson'),(2,'JavaScript Fundamentals','path-to-course-image.jpg','Master the fundamentals of JavaScript to add interactivity to your web pages.','6 weeks','Basic knowledge of HTML/CSS','Introduction to JavaScript','Master the fundamentals of JavaScript...','2 weeks','Alice Roberts','JavaScript Variables and Functions','Learn about variables and functions in JavaScript...','2 weeks','David Williams','JavaScript Events and DOM Manipulation','Explore events and manipulate the DOM with JavaScript...','2 weeks','Eva Lee'),(3,'Front-End Web Development','path-to-course-image.jpg','Learn the essentials of front-end web development and create responsive websites.','10 weeks','HTML, CSS, JavaScript','HTML Fundamentals','Learn the essentials of HTML...','2 weeks','Mark Thompson','CSS Basics and Styling','Master CSS basics and apply styles...','2 weeks','Julia Martinez','JavaScript Basics','Get started with JavaScript...','2 weeks','Michael Scott'),(4,'Data Science with R','path-to-course-image.jpg','Explore data science concepts using R programming language and statistical analysis.','12 weeks','Basic programming knowledge','Introduction to Data Science','Explore the field of Data Science...','2 weeks','Sarah Johnson','R Programming Basics','Get started with R programming...','2 weeks','Michael Brown','Statistical Analysis with R','Learn statistical analysis with R...','2 weeks','Emily Davis'),(5,'Machine Learning Essentials','path-to-course-image.jpg','Discover the basics of machine learning and its applications in real-world scenarios.','12 weeks','Python, Data Analysis','Introduction to Machine Learning','Discover the basics of Machine Learning...','2 weeks','James Wilson','Supervised Learning','Learn about supervised learning techniques...','2 weeks','Olivia Lee','Unsupervised Learning','Explore unsupervised learning methods...','2 weeks','Sophia White'),(6,'Artificial Intelligence Basics','path-to-course-image.jpg','Explore the world of artificial intelligence and its impact on various industries.','10 weeks','Python, Mathematics','Introduction to Artificial Intelligence','Get an overview of Artificial Intelligence...','2 weeks','Daniel Johnson','Machine Learning Algorithms','Learn about various ML algorithms...','2 weeks','Ava Anderson','AI Ethics and Implications','Discuss AI ethics and its impact on society...','2 weeks','Liam Martinez'),(7,'Mobile App Development with React Native','path-to-course-image.jpg','Build cross-platform mobile apps with React Native framework.','10 weeks','JavaScript, React.js','Introduction to React Native','Learn the basics of React Native...','2 weeks','Oliver Taylor','React Native Components','Explore React Native components...','2 weeks','Emma Green','Building Mobile Apps','Build cross-platform mobile apps with React Native...','2 weeks','Noah Adams'),(8,'Android App Development','path-to-course-image.jpg','Learn how to develop Android applications using Java and Android Studio.','8 weeks','Java Programming','Introduction to Android App Development','Get started with Android App Development...','2 weeks','Aiden Wilson','Android User Interface Design','Design user interfaces for Android apps...','2 weeks','Abigail Martinez','Android App Publishing','Learn how to publish Android apps...','2 weeks','Ethan Johnson'),(9,'iOS App Development','path-to-course-image.jpg','Develop iOS applications using Swift programming language and Xcode.','8 weeks','Swift Programming','Introduction to iOS App Development','Get started with iOS App Development...','2 weeks','Isabella Davis','Swift Programming Basics','Learn the basics of Swift programming...','2 weeks','William Lee','iOS App Design and User Experience','Design iOS apps with a focus on user experience...','2 weeks','Sophie Johnson');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  `enrollment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollments`
--

LOCK TABLES `enrollments` WRITE;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_reset_tokens`
--

DROP TABLE IF EXISTS `password_reset_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expiration` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`,`token`),
  CONSTRAINT `password_reset_tokens_ibfk_1` FOREIGN KEY (`email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_reset_tokens`
--

LOCK TABLES `password_reset_tokens` WRITE;
/*!40000 ALTER TABLE `password_reset_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_reset_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(10) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `age` int NOT NULL,
  `gender` varchar(10) NOT NULL,
  `country` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (17,'Mr','John','Obodai',23,'male','SA','johnodaiobodai@gmail.com','$2b$12$U3f/TMRz5EXwyMz2Erjoe.YZpKl7b0GP7ZeBZRzR0paAB1zIb4bfa'),(18,'Miss','cherish','ankomah',20,'female','Ghana','cherishak@gmail.com','$2b$12$cE0gtGc49zheEJFbACzWgu4iZ/FQLznfWMl7wKPru4DEKtjxQDaai');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-01  7:53:48
