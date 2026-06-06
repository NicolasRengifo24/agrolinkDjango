-- MySQL dump 10.13  Distrib 9.2.0, for Win64 (x86_64)
--
-- Host: localhost    Database: db_agrolink
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add calificacion',7,'add_calificacion'),(26,'Can change calificacion',7,'change_calificacion'),(27,'Can delete calificacion',7,'delete_calificacion'),(28,'Can view calificacion',7,'view_calificacion'),(29,'Can add vehiculo',8,'add_vehiculo'),(30,'Can change vehiculo',8,'change_vehiculo'),(31,'Can delete vehiculo',8,'delete_vehiculo'),(32,'Can view vehiculo',8,'view_vehiculo'),(33,'Can add envio',9,'add_envio'),(34,'Can change envio',9,'change_envio'),(35,'Can delete envio',9,'delete_envio'),(36,'Can view envio',9,'view_envio'),(37,'Can add categoria producto',10,'add_categoriaproducto'),(38,'Can change categoria producto',10,'change_categoriaproducto'),(39,'Can delete categoria producto',10,'delete_categoriaproducto'),(40,'Can view categoria producto',10,'view_categoriaproducto'),(41,'Can add finca',11,'add_finca'),(42,'Can change finca',11,'change_finca'),(43,'Can delete finca',11,'delete_finca'),(44,'Can view finca',11,'view_finca'),(45,'Can add producto',12,'add_producto'),(46,'Can change producto',12,'change_producto'),(47,'Can delete producto',12,'delete_producto'),(48,'Can view producto',12,'view_producto'),(49,'Can add imagenes producto',13,'add_imagenesproducto'),(50,'Can change imagenes producto',13,'change_imagenesproducto'),(51,'Can delete imagenes producto',13,'delete_imagenesproducto'),(52,'Can view imagenes producto',13,'view_imagenesproducto'),(53,'Can add producto finca',14,'add_productofinca'),(54,'Can change producto finca',14,'change_productofinca'),(55,'Can delete producto finca',14,'delete_productofinca'),(56,'Can view producto finca',14,'view_productofinca'),(57,'Can add certificados',15,'add_certificados'),(58,'Can change certificados',15,'change_certificados'),(59,'Can delete certificados',15,'delete_certificados'),(60,'Can view certificados',15,'view_certificados'),(61,'Can add maquinas',16,'add_maquinas'),(62,'Can change maquinas',16,'change_maquinas'),(63,'Can delete maquinas',16,'delete_maquinas'),(64,'Can view maquinas',16,'view_maquinas'),(65,'Can add servicio',17,'add_servicio'),(66,'Can change servicio',17,'change_servicio'),(67,'Can delete servicio',17,'delete_servicio'),(68,'Can view servicio',17,'view_servicio'),(69,'Can add usuario',18,'add_usuario'),(70,'Can change usuario',18,'change_usuario'),(71,'Can delete usuario',18,'delete_usuario'),(72,'Can view usuario',18,'view_usuario'),(73,'Can add administrador',19,'add_administrador'),(74,'Can change administrador',19,'change_administrador'),(75,'Can delete administrador',19,'delete_administrador'),(76,'Can view administrador',19,'view_administrador'),(77,'Can add asesor',20,'add_asesor'),(78,'Can change asesor',20,'change_asesor'),(79,'Can delete asesor',20,'delete_asesor'),(80,'Can view asesor',20,'view_asesor'),(81,'Can add cliente',21,'add_cliente'),(82,'Can change cliente',21,'change_cliente'),(83,'Can delete cliente',21,'delete_cliente'),(84,'Can view cliente',21,'view_cliente'),(85,'Can add productor',22,'add_productor'),(86,'Can change productor',22,'change_productor'),(87,'Can delete productor',22,'delete_productor'),(88,'Can view productor',22,'view_productor'),(89,'Can add transportista',23,'add_transportista'),(90,'Can change transportista',23,'change_transportista'),(91,'Can delete transportista',23,'delete_transportista'),(92,'Can view transportista',23,'view_transportista'),(93,'Can add compra',24,'add_compra'),(94,'Can change compra',24,'change_compra'),(95,'Can delete compra',24,'delete_compra'),(96,'Can view compra',24,'view_compra'),(97,'Can add detalles compra',25,'add_detallescompra'),(98,'Can change detalles compra',25,'change_detallescompra'),(99,'Can delete detalles compra',25,'delete_detallescompra'),(100,'Can view detalles compra',25,'view_detallescompra'),(101,'Can add pago',26,'add_pago'),(102,'Can change pago',26,'change_pago'),(103,'Can delete pago',26,'delete_pago'),(104,'Can view pago',26,'view_pago');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$nSi3M8LqGOtf1BvcSwvzsH$1dte7nxqqtfhQK3Qfv1TRWpZ3222c3yszgIiPZyOXkA=',NULL,0,'Jeison03','Jeison','leon','jeisonandres117.03@gmail.com',0,1,'2026-03-28 00:36:00.945962'),(2,'pbkdf2_sha256$720000$LrfExmBgzpsiWnf26FAbNt$Ubftkl7ZHYiaXfezcZzDPR6oPtnv7NwQ294lssCaRsQ=','2026-03-30 00:25:50.472354',0,'santiago117','santiago','leon','santiago@gmail.com',0,1,'2026-03-29 23:48:40.754123'),(4,'pbkdf2_sha256$720000$YIYowdsEmV5LJMCP1nz2A0$53hJnQ1zd3NKMHAirN4RIMsFQEaO1Y/BmaOGnOOra70=','2026-04-02 01:11:41.087349',0,'admin','','','jeisonandres117.03@gmail.com',0,0,'2026-04-02 00:52:22.433299'),(5,'pbkdf2_sha256$720000$phU3dweknls67nAfKHz1Lc$XwwWwkz5MAPML/EZRm9CDsQpVxpjdJwZVmwTeGn04nk=','2026-04-17 03:17:15.583661',0,'Alejo2003','Alejo','Leon','alejo2026@gmail.com',0,1,'2026-04-02 01:19:16.076686'),(6,'pbkdf2_sha256$720000$vmdDxZ4xEQYoJGNDu08A4l$co01mq/KbbNk0RnRPyfPfcD1P3uB4fseOY0Bq771lto=','2026-04-18 22:48:54.398703',0,'nico2026','Nicolas','Garzon','nico26@gmail.com',0,1,'2026-04-04 01:58:44.814624'),(7,'pbkdf2_sha256$720000$pOaTud1Qh6Wg6XGQE0Gjp4$LuWb6eeNqC4noo8ThAD33tnDlh41njb7EC6vLdwi6b4=','2026-04-17 03:28:31.466284',0,'pablo2026','pablo','perez','pablo1@gmail.com',0,1,'2026-04-07 02:27:35.196386'),(8,'pbkdf2_sha256$720000$3qyPEAOGZcb4NVHOOjGTXd$qpV/dncihXy+TU2q7KMY5lnhQGhGlUHdWV8H5zw4Upw=','2026-04-18 22:46:15.521705',0,'camilo','camilo','sanchez','camilito@gmail.com',0,1,'2026-04-07 05:04:21.644210'),(9,'pbkdf2_sha256$720000$yX7rp2jBSJOTdCqaxBvuKj$5ngEc+FzVSw3qTYZc2PEJuokmT2YAZTxxSpdXMvmC+E=','2026-04-08 05:27:21.564219',0,'alfredo','alfredo','Perez','alfred@gmail.com',0,1,'2026-04-08 05:26:45.768959'),(10,'pbkdf2_sha256$720000$uJcjwHACOySy0QFlYCf6E5$pAHvrlelkdR9PSnnIJA3hjfVRL+e+HBbn+BbzMbHeXI=','2026-04-17 02:52:08.668633',0,'Admin2026','Pedro','Rivera','admin7@gmail.com',0,1,'2026-04-08 06:55:53.441131'),(11,'pbkdf2_sha256$720000$Ij8VcDUTD83fAL4ox3n7DM$+t/5c4cgutv5Xarrs6ecvSywevZpfFyTtE/tZ9Sjw2M=','2026-04-15 21:42:49.379999',0,'jose','jose','rodriguez','jose3@gmail.com',0,1,'2026-04-08 11:44:10.697149'),(12,'pbkdf2_sha256$720000$nwNwPtCKprJocY5nw2KegC$GaZzQwyw6jP9PSlrICWRgIZ6dWXg8fcATWCwpxl0ad4=','2026-04-08 13:01:54.864871',0,'danielcliente','daniel','lopez','daniel@gmail.com',0,1,'2026-04-08 13:01:36.755046'),(13,'pbkdf2_sha256$720000$QZACF9RlCSxj7fb1SfSjVx$6qgrAes4QdjxSmVfVY4ETtxJDOoQytcFxW6lW4MkDA8=','2026-04-17 01:55:30.788128',0,'Armando2020','Armando','Mendosa','armando20@gmail.com',0,1,'2026-04-15 22:06:47.192262');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'calificaciones','calificacion'),(5,'contenttypes','contenttype'),(9,'envios','envio'),(8,'envios','vehiculo'),(24,'pedidos','compra'),(25,'pedidos','detallescompra'),(26,'pedidos','pago'),(10,'productos','categoriaproducto'),(11,'productos','finca'),(13,'productos','imagenesproducto'),(12,'productos','producto'),(14,'productos','productofinca'),(15,'servicios','certificados'),(16,'servicios','maquinas'),(17,'servicios','servicio'),(6,'sessions','session'),(19,'usuarios','administrador'),(20,'usuarios','asesor'),(21,'usuarios','cliente'),(22,'usuarios','productor'),(23,'usuarios','transportista'),(18,'usuarios','usuario');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-24 21:50:18.902706'),(2,'auth','0001_initial','2026-03-24 21:50:19.772700'),(3,'admin','0001_initial','2026-03-24 21:50:20.006461'),(4,'admin','0002_logentry_remove_auto_add','2026-03-24 21:50:20.016627'),(5,'admin','0003_logentry_add_action_flag_choices','2026-03-24 21:50:20.030667'),(6,'contenttypes','0002_remove_content_type_name','2026-03-24 21:50:20.135037'),(7,'auth','0002_alter_permission_name_max_length','2026-03-24 21:50:20.227438'),(8,'auth','0003_alter_user_email_max_length','2026-03-24 21:50:20.250527'),(9,'auth','0004_alter_user_username_opts','2026-03-24 21:50:20.271928'),(10,'auth','0005_alter_user_last_login_null','2026-03-24 21:50:20.345450'),(11,'auth','0006_require_contenttypes_0002','2026-03-24 21:50:20.348838'),(12,'auth','0007_alter_validators_add_error_messages','2026-03-24 21:50:20.357708'),(13,'auth','0008_alter_user_username_max_length','2026-03-24 21:50:20.381820'),(14,'auth','0009_alter_user_last_name_max_length','2026-03-24 21:50:20.414555'),(15,'auth','0010_alter_group_name_max_length','2026-03-24 21:50:20.442514'),(16,'auth','0011_update_proxy_permissions','2026-03-24 21:50:20.454109'),(17,'auth','0012_alter_user_first_name_max_length','2026-03-24 21:50:20.479114'),(19,'usuarios','0001_initial','2026-03-24 21:50:21.378108'),(20,'productos','0001_initial','2026-03-24 21:50:22.143316'),(21,'pedidos','0001_initial','2026-03-24 21:50:22.470178'),(22,'envios','0001_initial','2026-03-24 21:50:22.950374'),(23,'servicios','0001_initial','2026-03-24 21:50:23.308993'),(24,'sessions','0001_initial','2026-03-24 21:50:23.361691'),(25,'usuarios','0002_usuario_estado','2026-03-25 04:30:15.104125'),(26,'servicios','0002_servicio_categoria','2026-03-25 23:04:42.611261'),(27,'usuarios','0003_usuario_user','2026-03-27 13:31:42.212542'),(28,'usuarios','0004_remove_usuario_contrasena_usuario','2026-03-27 13:31:42.331176'),(29,'productos','0002_alter_imagenesproducto_id_producto','2026-03-30 20:00:00.501998'),(30,'usuarios','0005_add_user_field','2026-03-30 20:01:49.842128'),(31,'productos','0003_alter_productofinca_id_finca_and_more','2026-03-30 20:06:52.655048'),(32,'pedidos','0002_compra_estado','2026-04-01 02:23:35.005738'),(33,'pedidos','0003_alter_compra_fecha_hora_compra','2026-04-01 03:15:40.482303'),(34,'pedidos','0004_alter_compra_estado_pago','2026-04-04 18:37:05.955274'),(35,'pedidos','0005_delete_pago','2026-04-05 00:50:43.991349'),(36,'envios','0002_vehiculo_estado','2026-04-05 03:52:07.978893'),(37,'pedidos','0006_alter_compra_estado','2026-04-05 03:52:07.990299'),(38,'calificaciones','0002_initial','2026-04-07 04:14:36.297909'),(39,'envios','0002_initial','2026-04-07 04:17:55.875230'),(40,'envios','0003_merge_0002_initial_0002_vehiculo_estado','2026-04-07 04:17:55.911108'),(41,'pedidos','0006_compra_latitud_destino_compra_longitud_destino_and_more','2026-04-07 04:18:14.267765'),(42,'calificaciones','0003_calificacion_comentario_calificacion_fecha','2026-04-07 04:26:14.120424'),(43,'productos','0004_remove_producto_id_calificacion','2026-04-07 04:26:16.642641'),(44,'usuarios','0006_remove_administrador_privilegios_admin_and_more','2026-04-08 06:20:24.936274'),(46,'calificaciones','0002_alter_calificacion_id_compra','2026-04-15 04:43:06.925182'),(47,'calificaciones','0001_initial','2026-04-15 05:19:48.759146');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2x746fz284trelc36zdtxs7b0b9lpetp','e30:1wAMpy:OKlaOSLsZ380t2pmZ2fd9yOl8-TtzMK0hh6jXDi6f8I','2026-04-22 06:56:30.425689'),('zwhc35wz87t3g349kak8jsckcxjb895b','.eJxVjMsOwiAQAP9lz4a0IK8evfcbyO4CUjWQlPZk_HfTpAe9zkzmDQH3rYS9pzUsESawcPllhPxM9RDxgfXeBLe6rQuJIxGn7WJuMb1uZ_s3KNgLTMAWBzLGe5XRMWbtmd2ImrLNirQZrsqyMhqdHr2SWjKnSCTJZK8sO_h8AfiLOEY:1wDZsd:wn3CGNl9nYO7g_0tZiF78Jc1qftyI7N_8oWHkpdUsdE','2026-05-01 03:28:31.475428');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_administradores`
--

DROP TABLE IF EXISTS `tb_administradores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_administradores` (
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  CONSTRAINT `tb_administradores_id_usuario_d63f3388_fk_tb_usuarios_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_administradores`
--

LOCK TABLES `tb_administradores` WRITE;
/*!40000 ALTER TABLE `tb_administradores` DISABLE KEYS */;
INSERT INTO `tb_administradores` VALUES (22);
/*!40000 ALTER TABLE `tb_administradores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_asesores`
--

DROP TABLE IF EXISTS `tb_asesores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_asesores` (
  `id_usuario` int(11) NOT NULL,
  `tipo_asesoria` varchar(50) DEFAULT NULL,
  `id_calificacion` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `tb_asesores_id_calificacion_a82b862f_fk_tb_califi` (`id_calificacion`),
  CONSTRAINT `tb_asesores_id_calificacion_a82b862f_fk_tb_califi` FOREIGN KEY (`id_calificacion`) REFERENCES `tb_calificacion` (`id_calificacion`),
  CONSTRAINT `tb_asesores_id_usuario_23679f71_fk_tb_usuarios_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_asesores`
--

LOCK TABLES `tb_asesores` WRITE;
/*!40000 ALTER TABLE `tb_asesores` DISABLE KEYS */;
INSERT INTO `tb_asesores` VALUES (4,'gestion cultivo',NULL),(6,'gestion ganado',NULL),(19,NULL,NULL);
/*!40000 ALTER TABLE `tb_asesores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_calificacion`
--

DROP TABLE IF EXISTS `tb_calificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_calificacion` (
  `id_calificacion` int(11) NOT NULL AUTO_INCREMENT,
  `puntaje_producto` int(11) DEFAULT NULL,
  `puntaje_productor` int(11) DEFAULT NULL,
  `puntaje_transportista` int(11) DEFAULT NULL,
  `comentario` longtext DEFAULT NULL,
  `fecha` datetime(6) NOT NULL,
  `id_compra_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_calificacion`),
  KEY `tb_calificacion_id_compra_id_e8d13e23_fk_tb_compras_id_compra` (`id_compra_id`),
  CONSTRAINT `tb_calificacion_id_compra_id_e8d13e23_fk_tb_compras_id_compra` FOREIGN KEY (`id_compra_id`) REFERENCES `tb_compras` (`id_compra`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_calificacion`
--

LOCK TABLES `tb_calificacion` WRITE;
/*!40000 ALTER TABLE `tb_calificacion` DISABLE KEYS */;
INSERT INTO `tb_calificacion` VALUES (1,4,NULL,NULL,'Producto fresco y en buen estado recomiendo','2026-04-15 20:13:30.253195',17),(2,5,NULL,NULL,'Buen producto me encanto','2026-04-16 00:16:18.396896',16),(3,5,NULL,NULL,'excelente servicio me encanto, recomiendo ','2026-04-16 02:58:35.891953',21),(4,3,NULL,NULL,'buen producto ','2026-04-16 20:05:28.675893',22);
/*!40000 ALTER TABLE `tb_calificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_categorias_productos`
--

DROP TABLE IF EXISTS `tb_categorias_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_categorias_productos` (
  `id_categoria` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(50) NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_categorias_productos`
--

LOCK TABLES `tb_categorias_productos` WRITE;
/*!40000 ALTER TABLE `tb_categorias_productos` DISABLE KEYS */;
INSERT INTO `tb_categorias_productos` VALUES (1,'Frutas'),(2,'Verduras'),(3,'Granos y cereales'),(4,'Miel'),(5,'Hierbas'),(6,'Tuberculos y raíces'),(7,'café'),(8,'Carnicos'),(9,'Lacteos');
/*!40000 ALTER TABLE `tb_categorias_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_certificados`
--

DROP TABLE IF EXISTS `tb_certificados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_certificados` (
  `id_certificado` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_certificado` varchar(100) NOT NULL,
  `descripcion_cert` varchar(255) NOT NULL,
  `fecha_expedicion` date NOT NULL,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id_certificado`),
  KEY `tb_certificados_id_usuario_5eade2b3_fk_tb_asesores_id_usuario` (`id_usuario`),
  CONSTRAINT `tb_certificados_id_usuario_5eade2b3_fk_tb_asesores_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_asesores` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_certificados`
--

LOCK TABLES `tb_certificados` WRITE;
/*!40000 ALTER TABLE `tb_certificados` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_certificados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_clientes`
--

DROP TABLE IF EXISTS `tb_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_clientes` (
  `id_usuario` int(11) NOT NULL,
  `preferencias` varchar(150) DEFAULT NULL,
  `id_calificacion` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `tb_clientes_id_calificacion_a99b345d_fk_tb_califi` (`id_calificacion`),
  CONSTRAINT `tb_clientes_id_calificacion_a99b345d_fk_tb_califi` FOREIGN KEY (`id_calificacion`) REFERENCES `tb_calificacion` (`id_calificacion`),
  CONSTRAINT `tb_clientes_id_usuario_f73af89a_fk_tb_usuarios_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_clientes`
--

LOCK TABLES `tb_clientes` WRITE;
/*!40000 ALTER TABLE `tb_clientes` DISABLE KEYS */;
INSERT INTO `tb_clientes` VALUES (2,'verduras',NULL),(14,'verduras, y frutas',NULL),(15,'frutas',NULL),(17,NULL,NULL),(21,NULL,NULL),(25,NULL,NULL);
/*!40000 ALTER TABLE `tb_clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_compras`
--

DROP TABLE IF EXISTS `tb_compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_compras` (
  `id_compra` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_hora_compra` datetime(6) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `impuestos` decimal(10,2) NOT NULL,
  `valor_envio` decimal(10,2) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `direccion_entrega` varchar(200) DEFAULT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `id_cliente` int(11) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `latitud_destino` double DEFAULT NULL,
  `longitud_destino` double DEFAULT NULL,
  PRIMARY KEY (`id_compra`),
  KEY `tb_compras_id_cliente_6e988304_fk_tb_clientes_id_usuario` (`id_cliente`),
  CONSTRAINT `tb_compras_id_cliente_6e988304_fk_tb_clientes_id_usuario` FOREIGN KEY (`id_cliente`) REFERENCES `tb_clientes` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_compras`
--

LOCK TABLES `tb_compras` WRITE;
/*!40000 ALTER TABLE `tb_compras` DISABLE KEYS */;
INSERT INTO `tb_compras` VALUES (1,'2026-08-10 12:52:00.000000',15000.00,300.00,2000.00,17300.00,'cr 1 Bis A #75 sur 14','Tarjeta',14,'carrito',NULL,NULL),(2,'2026-03-31 08:30:00.000000',20000.00,300.00,2000.00,22300.00,'cr 1 Bis A #75 sur 18','Tarjeta',15,'carrito',NULL,NULL),(3,'2026-04-01 03:16:19.743864',0.00,0.00,0.00,0.00,NULL,NULL,2,'carrito',NULL,NULL),(4,'2026-04-02 03:45:36.920319',22000.00,4180.00,NULL,26180.00,NULL,NULL,17,'pagado',NULL,NULL),(5,'2026-04-03 04:01:34.108775',37000.00,7030.00,NULL,44030.00,NULL,'epayco',17,'pagado',NULL,NULL),(6,'2026-04-03 19:28:50.896090',5500.00,1045.00,NULL,6545.00,NULL,'epayco',17,'pagado',NULL,NULL),(7,'2026-04-04 21:56:40.389803',15000.00,2850.00,NULL,17850.00,NULL,'epayco',17,'pagado',NULL,NULL),(8,'2026-04-04 22:29:03.755665',49500.00,9405.00,NULL,58905.00,NULL,'epayco',17,'pagado',NULL,NULL),(9,'2026-04-05 06:36:57.115579',100000.00,19000.00,NULL,119000.00,NULL,'epayco',17,'pagado',NULL,NULL),(10,'2026-04-05 06:59:00.328423',55000.00,10450.00,NULL,65450.00,NULL,NULL,17,'cancelado',NULL,NULL),(11,'2026-04-05 16:07:15.799197',11000.00,2090.00,NULL,13090.00,NULL,NULL,17,'cancelado',NULL,NULL),(12,'2026-04-05 16:18:27.826218',33000.00,6270.00,NULL,39270.00,NULL,NULL,17,'cancelado',NULL,NULL),(13,'2026-04-05 16:38:41.968178',11000.00,2090.00,NULL,13090.00,NULL,'epayco',17,'pagado',NULL,NULL),(14,'2026-04-05 16:51:05.913815',5500.00,1045.00,NULL,6545.00,NULL,'epayco',17,'pagado',NULL,NULL),(15,'2026-04-07 04:32:02.729799',37000.00,7030.00,NULL,44030.00,'Calle 75 Sur, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia','epayco',17,'pagado',4.516915812113139,-74.10567907993347),(16,'2026-04-08 01:26:04.404615',40000.00,7600.00,NULL,47600.00,'Calle 75 Bis Sur, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia','epayco',17,'pagado',4.516635990699617,-74.10552664683934),(17,'2026-04-08 01:33:23.744071',63000.00,11970.00,NULL,74970.00,'Calle 90B Sur, Charalá, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110541, Colombia','epayco',17,'pagado',4.500309567186345,-74.10744909362751),(18,'2026-04-08 08:57:35.187712',160000.00,30400.00,NULL,190400.00,'Carrera 1, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia','epayco',17,'pagado',4.519223933692581,-74.10498579617524),(19,'2026-04-12 22:43:53.904038',40000.00,7600.00,NULL,47600.00,'Calle 90C Sur, La Orquidea Usme, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110541, Colombia','epayco',17,'pagado',4.498984361536529,-74.10678497311561),(20,'2026-04-14 16:47:14.448069',120000.00,22800.00,NULL,142800.00,'Avenida Calle 53, Los Monjes, UPZs Localidad Engativá, Localidad Engativá, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 111071, Colombia','epayco',17,'pagado',4.679799583475691,-74.11300377036866),(21,'2026-04-15 22:08:14.433063',62500.00,11875.00,NULL,74375.00,'Calle 4, La Fragua, Universidades, Comuna Soacha Central, Soacha ciudad, Soacha, Cundinamarca, RAP (Especial) Central, 250052, Colombia','epayco',25,'pagado',4.579759424666169,-74.22295953878209),(22,'2026-04-16 19:50:23.444630',5500.00,1045.00,NULL,6545.00,'Carrera 1, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia','epayco',25,'pagado',4.519609546462377,-74.10441903457681),(23,'2026-04-17 03:20:10.442404',16500.00,3135.00,NULL,19635.00,NULL,NULL,17,'carrito',NULL,NULL);
/*!40000 ALTER TABLE `tb_compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_detalles_compra`
--

DROP TABLE IF EXISTS `tb_detalles_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_detalles_compra` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) DEFAULT NULL,
  `id_compra` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `distancia_km` double DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `tb_detalles_compra_id_compra_221648be_fk_tb_compras_id_compra` (`id_compra`),
  KEY `tb_detalles_compra_id_producto_faecafa1_fk_tb_produc` (`id_producto`),
  CONSTRAINT `tb_detalles_compra_id_compra_221648be_fk_tb_compras_id_compra` FOREIGN KEY (`id_compra`) REFERENCES `tb_compras` (`id_compra`),
  CONSTRAINT `tb_detalles_compra_id_producto_faecafa1_fk_tb_produc` FOREIGN KEY (`id_producto`) REFERENCES `tb_productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_detalles_compra`
--

LOCK TABLES `tb_detalles_compra` WRITE;
/*!40000 ALTER TABLE `tb_detalles_compra` DISABLE KEYS */;
INSERT INTO `tb_detalles_compra` VALUES (1,3,5000.00,15000.00,1,1,NULL),(2,4,3000.00,22000.00,2,2,NULL),(8,4,5500.00,22000.00,4,2,NULL),(11,3,5000.00,15000.00,5,1,NULL),(12,4,5500.00,22000.00,5,2,NULL),(19,1,5500.00,5500.00,6,2,NULL),(20,3,5000.00,15000.00,7,1,NULL),(21,9,5500.00,49500.00,8,2,NULL),(22,20,5000.00,100000.00,9,1,NULL),(23,11,5000.00,55000.00,10,1,NULL),(24,2,5500.00,11000.00,11,2,NULL),(26,6,5500.00,33000.00,12,2,NULL),(27,2,5500.00,11000.00,13,2,NULL),(28,1,5500.00,5500.00,14,2,NULL),(29,3,5000.00,15000.00,15,1,NULL),(30,4,5500.00,22000.00,15,2,NULL),(31,5,8000.00,40000.00,16,4,21.927537476682176),(32,5,500.00,2500.00,17,5,23.753057950198315),(33,11,5500.00,60500.00,17,2,NULL),(36,2,50000.00,100000.00,18,8,35.34757843058818),(37,3,20000.00,60000.00,18,7,35.34757843058818),(38,5,8000.00,40000.00,19,4,42.08048389370713),(39,5,12000.00,60000.00,20,6,22.230799101038592),(43,3,20000.00,60000.00,20,7,22.230799101038592),(44,5,12000.00,60000.00,21,6,36.809246400970885),(45,5,500.00,2500.00,21,5,36.809246400970885),(46,1,5500.00,5500.00,22,2,21.58100224554649),(47,3,5500.00,16500.00,23,2,NULL);
/*!40000 ALTER TABLE `tb_detalles_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_envios`
--

DROP TABLE IF EXISTS `tb_envios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_envios` (
  `id_envio` int(11) NOT NULL AUTO_INCREMENT,
  `estado_envio` varchar(50) DEFAULT NULL,
  `fecha_salida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `numero_seguimiento` varchar(50) DEFAULT NULL,
  `direccion_origen` varchar(300) DEFAULT NULL,
  `direccion_destino` varchar(300) DEFAULT NULL,
  `latitud_origen` double DEFAULT NULL,
  `longitud_origen` double DEFAULT NULL,
  `latitud_destino` double DEFAULT NULL,
  `longitud_destino` double DEFAULT NULL,
  `distancia_km` double DEFAULT NULL,
  `peso_total_kg` double DEFAULT NULL,
  `costo_base` decimal(10,2) DEFAULT NULL,
  `costo_peso` decimal(10,2) DEFAULT NULL,
  `costo_total` decimal(10,2) DEFAULT NULL,
  `tarifa_por_km` decimal(10,2) DEFAULT NULL,
  `tarifa_por_kg` decimal(10,2) DEFAULT NULL,
  `id_compra` int(11) DEFAULT NULL,
  `id_transportista` int(11) DEFAULT NULL,
  `id_vehiculo` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_envio`),
  KEY `tb_envios_id_compra_81dfdc10_fk_tb_compras_id_compra` (`id_compra`),
  KEY `tb_envios_id_transportista_8a8dd954_fk_tb_transp` (`id_transportista`),
  KEY `tb_envios_id_vehiculo_e55d1f2f_fk_tb_vehiculos_id_vehiculo` (`id_vehiculo`),
  CONSTRAINT `tb_envios_id_compra_81dfdc10_fk_tb_compras_id_compra` FOREIGN KEY (`id_compra`) REFERENCES `tb_compras` (`id_compra`),
  CONSTRAINT `tb_envios_id_transportista_8a8dd954_fk_tb_transp` FOREIGN KEY (`id_transportista`) REFERENCES `tb_transportistas` (`id_usuario`),
  CONSTRAINT `tb_envios_id_vehiculo_e55d1f2f_fk_tb_vehiculos_id_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `tb_vehiculos` (`id_vehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_envios`
--

LOCK TABLES `tb_envios` WRITE;
/*!40000 ALTER TABLE `tb_envios` DISABLE KEYS */;
INSERT INTO `tb_envios` VALUES (1,'1','0000-00-00',NULL,'1','calle 2 b #03 04','cr 1 Bis A #75 sur 14',4.8616,-74.0326,4.6097,-74.0817,12000,90,15000.00,17300.00,17300.00,1000.00,100.00,1,5,1),(2,'1','2026-02-03','2026-02-04','2','calle 2 b #03 04','cr 1 Bis A #75 sur 18',4.8616,-74.0326,5.0221,-74.0048,10000,30,20000.00,25000.00,25000.00,1000.00,100.00,2,5,2),(3,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,5,NULL,NULL),(4,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,6,NULL,NULL),(5,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,7,NULL,NULL),(6,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,8,NULL,NULL),(7,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,9,NULL,NULL),(8,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,13,NULL,NULL),(9,'pendiente',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,14,NULL,NULL),(10,'pendiente',NULL,NULL,NULL,NULL,'Calle 75 Sur, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,15,NULL,NULL),(11,'Entregado','2026-04-12','2026-04-16','AGRO-20260411-H4ZDU1','call 19 chia','Calle 75 Bis Sur, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia',4.876086397020851,-74.07489707560103,4.516635990699617,-74.10552664683934,21.927537476682176,10,65782.61,2000.00,67782.61,3000.00,200.00,16,18,7),(12,'Entregado','2026-04-08','2026-04-09','AGRO-20260408-4PVKR2','call 19 chia','Calle 90B Sur, Charalá, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110541, Colombia',4.876086397020851,-74.07489707560103,4.500309567186345,-74.10744909362751,23.753057950198315,70,71259.17,14000.00,85259.17,3000.00,200.00,17,18,6),(13,'pendiente',NULL,NULL,'AGRO-20260412-HZIENB','cll 8#5','Carrera 1, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia',4.73353728046653,-74.34053591281511,4.519223933692581,-74.10498579617524,35.34757843058818,100.5,106042.74,20100.00,126142.74,3000.00,200.00,18,NULL,NULL),(14,'pendiente',NULL,NULL,'AGRO-20260412-B4QO22','call 19 chia','Calle 90C Sur, La Orquidea Usme, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110541, Colombia',4.876086397020851,-74.07489707560103,4.498984361536529,-74.10678497311561,42.08048389370713,10,126241.45,2000.00,128241.45,3000.00,200.00,19,NULL,NULL),(15,'Entregado','2026-04-28','2026-05-01','AGRO-20260415-XSNO6V','calle 4 # 01-02','Calle 4 Sur, Hogares Soacha, Comuna Soacha Central, Soacha ciudad, Soacha, Cundinamarca, RAP (Especial) Central, 250051, Colombia',4.648990320378703,-74.44813370704652,4.594138032061742,-74.22790904422287,25.158772500172223,20,75476.32,4000.00,79476.32,3000.00,200.00,21,18,6),(16,'Entregado','2026-04-21','2026-04-24','AGRO-20260415-6L0SGX','calle 4 # 01-02','Calle 4 Sur, Hogares Soacha, Comuna Soacha Central, Soacha ciudad, Soacha, Cundinamarca, RAP (Especial) Central, 250051, Colombia',4.648990320378703,-74.44813370704652,4.594138032061742,-74.22790904422287,25.158772500172223,20,75476.32,4000.00,79476.32,3000.00,200.00,21,18,6),(17,'Entregado','2026-04-16','2026-04-19','AGRO-20260415-WM7IXH','calle 4 # 01-02','Calle 4 Sur, Hogares Soacha, Comuna Soacha Central, Soacha ciudad, Soacha, Cundinamarca, RAP (Especial) Central, 250051, Colombia',4.648990320378703,-74.44813370704652,4.594138032061742,-74.22790904422287,25.158772500172223,20,75476.32,4000.00,79476.32,3000.00,200.00,21,18,8),(18,'pendiente',NULL,NULL,'AGRO-20260415-A6IH7Q','call 19 chia','Avenida Calle 53, Los Monjes, UPZs Localidad Engativá, Localidad Engativá, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 111071, Colombia',4.876086397020851,-74.07489707560103,4.679799583475691,-74.11300377036866,22.230799101038592,12,66692.40,2400.00,69092.40,3000.00,200.00,20,NULL,NULL),(19,'Entregado','2026-05-01','2026-05-04','AGRO-20260416-AE4QTQ','vereda','Carrera 1, Los Olivares, UPZs de Bogotá, Localidad Usme, Bogotá, Bogotá, Distrito Capital, RAP (Especial) Central, 110521, Colombia',NULL,NULL,4.519609546462377,-74.10441903457681,21.58100224554649,5,64743.01,1000.00,65743.01,3000.00,200.00,22,18,8);
/*!40000 ALTER TABLE `tb_envios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_fincas`
--

DROP TABLE IF EXISTS `tb_fincas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_fincas` (
  `id_finca` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_finca` varchar(100) DEFAULT NULL,
  `direccion_finca` varchar(200) DEFAULT NULL,
  `certificado_BPA` varchar(200) DEFAULT NULL,
  `certificado_MIRFE` varchar(200) DEFAULT NULL,
  `certificado_MIPE` varchar(200) DEFAULT NULL,
  `registro_ICA` varchar(200) DEFAULT NULL,
  `latitud` double DEFAULT NULL,
  `longitud` double DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id_finca`),
  KEY `tb_fincas_id_usuario_818c5da7_fk_tb_productores_id_usuario` (`id_usuario`),
  CONSTRAINT `tb_fincas_id_usuario_818c5da7_fk_tb_productores_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_productores` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_fincas`
--

LOCK TABLES `tb_fincas` WRITE;
/*!40000 ALTER TABLE `tb_fincas` DISABLE KEYS */;
INSERT INTO `tb_fincas` VALUES (1,'finca santa isabel','vereda','',NULL,NULL,NULL,NULL,NULL,'chia','Cundinamarca',3),(2,'finca tuguatoque','call 19 chia',NULL,NULL,NULL,NULL,4.876086397020851,-74.07489707560103,'chia','cundinamarca',20),(3,'finca bojaca','cll 8#5',NULL,NULL,NULL,NULL,4.73353728046653,-74.34053591281511,NULL,NULL,24),(4,'Finca los robles','calle 4 # 01-02',NULL,NULL,NULL,NULL,4.648990320378703,-74.44813370704652,'La Mesa','Cundinamarca',23);
/*!40000 ALTER TABLE `tb_fincas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_imagenes_productos`
--

DROP TABLE IF EXISTS `tb_imagenes_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_imagenes_productos` (
  `id_imagen` int(11) NOT NULL AUTO_INCREMENT,
  `url_imagen` varchar(100) NOT NULL,
  `es_principal` int(11) DEFAULT NULL,
  `id_producto` int(11) NOT NULL,
  PRIMARY KEY (`id_imagen`),
  KEY `tb_imagenes_producto_id_producto_38ff632e_fk_tb_produc` (`id_producto`),
  CONSTRAINT `tb_imagenes_producto_id_producto_38ff632e_fk_tb_produc` FOREIGN KEY (`id_producto`) REFERENCES `tb_productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_imagenes_productos`
--

LOCK TABLES `tb_imagenes_productos` WRITE;
/*!40000 ALTER TABLE `tb_imagenes_productos` DISABLE KEYS */;
INSERT INTO `tb_imagenes_productos` VALUES (1,'productos/brocoli-ramas.jpg',1,1),(2,'productos/aguacate.avif',1,2),(4,'productos/images.jfif',1,4),(5,'productos/banana_from_maracaibo.webp',1,5),(6,'productos/cafe_Y5sla3u.jpg',1,6),(7,'productos/Pollo.jpg',1,7),(8,'productos/papa.jpg',1,8),(9,'productos/descarga.jfif',1,9),(10,'productos/yuca.jfif',1,10);
/*!40000 ALTER TABLE `tb_imagenes_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_maquinas`
--

DROP TABLE IF EXISTS `tb_maquinas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_maquinas` (
  `id_maquina` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_maquina` varchar(50) NOT NULL,
  `documento_propiedad` varchar(50) NOT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `registro_RNMA` varchar(200) DEFAULT NULL,
  `tarjeta_registro_maquinaria` varchar(300) DEFAULT NULL,
  `id_asesor` int(11) NOT NULL,
  PRIMARY KEY (`id_maquina`),
  KEY `tb_maquinas_id_asesor_6dbd1e39_fk_tb_asesores_id_usuario` (`id_asesor`),
  CONSTRAINT `tb_maquinas_id_asesor_6dbd1e39_fk_tb_asesores_id_usuario` FOREIGN KEY (`id_asesor`) REFERENCES `tb_asesores` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_maquinas`
--

LOCK TABLES `tb_maquinas` WRITE;
/*!40000 ALTER TABLE `tb_maquinas` DISABLE KEYS */;
INSERT INTO `tb_maquinas` VALUES (1,'tractor','1333325345435','Caterpillar 756','3eqeb3334','1000087644',19);
/*!40000 ALTER TABLE `tb_maquinas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_productores`
--

DROP TABLE IF EXISTS `tb_productores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_productores` (
  `id_usuario` int(11) NOT NULL,
  `tipo_cultivo` varchar(50) DEFAULT NULL,
  `id_calificacion` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `tb_productores_id_calificacion_c52f6dec_fk_tb_califi` (`id_calificacion`),
  CONSTRAINT `tb_productores_id_calificacion_c52f6dec_fk_tb_califi` FOREIGN KEY (`id_calificacion`) REFERENCES `tb_calificacion` (`id_calificacion`),
  CONSTRAINT `tb_productores_id_usuario_08e24303_fk_tb_usuarios_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_productores`
--

LOCK TABLES `tb_productores` WRITE;
/*!40000 ALTER TABLE `tb_productores` DISABLE KEYS */;
INSERT INTO `tb_productores` VALUES (3,'verduras',NULL),(20,'None',NULL),(23,NULL,NULL),(24,NULL,NULL);
/*!40000 ALTER TABLE `tb_productores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_productos`
--

DROP TABLE IF EXISTS `tb_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_productos` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `precio` decimal(12,0) DEFAULT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion_producto` varchar(255) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `peso_kg` decimal(10,2) DEFAULT NULL,
  `id_categoria` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `tb_productos_id_categoria_f0b6aa5a_fk_tb_catego` (`id_categoria`),
  KEY `tb_productos_id_usuario_c2cbfddf_fk_tb_productores_id_usuario` (`id_usuario`),
  CONSTRAINT `tb_productos_id_categoria_f0b6aa5a_fk_tb_catego` FOREIGN KEY (`id_categoria`) REFERENCES `tb_categorias_productos` (`id_categoria`),
  CONSTRAINT `tb_productos_id_usuario_c2cbfddf_fk_tb_productores_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_productores` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_productos`
--

LOCK TABLES `tb_productos` WRITE;
/*!40000 ALTER TABLE `tb_productos` DISABLE KEYS */;
INSERT INTO `tb_productos` VALUES (1,5000,'brócoli','fresco y delicioso',120,5.00,2,3),(2,5500,'aguacate','fresco y delicioso',39,5.00,2,3),(4,8000,'arandanos','producto fresco y de calidad',45,2.00,1,20),(5,500,'banano','fresco y frutosoo',20,3.00,1,20),(6,12000,'cafe','el mejor cafe de colombiaa',25,0.00,7,20),(7,20000,'pollo','pollito delicioso',32,3.50,8,3),(8,50000,'papa','papar12',98,30.00,6,24),(9,7100,'Mango','Fruta fresca y dulce',120,0.35,1,23),(10,3600,'Yuca','La mejor yuca de Cundinamarca',340,1.00,6,23);
/*!40000 ALTER TABLE `tb_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_productos_fincas`
--

DROP TABLE IF EXISTS `tb_productos_fincas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_productos_fincas` (
  `id_producto_finca` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad_produccion` decimal(10,2) DEFAULT NULL,
  `fecha_cosecha` date DEFAULT NULL,
  `id_finca` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  PRIMARY KEY (`id_producto_finca`),
  KEY `tb_productos_fincas_id_finca_26a1bc81_fk_tb_fincas_id_finca` (`id_finca`),
  KEY `tb_productos_fincas_id_producto_48f10913_fk_tb_produc` (`id_producto`),
  CONSTRAINT `tb_productos_fincas_id_finca_26a1bc81_fk_tb_fincas_id_finca` FOREIGN KEY (`id_finca`) REFERENCES `tb_fincas` (`id_finca`),
  CONSTRAINT `tb_productos_fincas_id_producto_48f10913_fk_tb_produc` FOREIGN KEY (`id_producto`) REFERENCES `tb_productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_productos_fincas`
--

LOCK TABLES `tb_productos_fincas` WRITE;
/*!40000 ALTER TABLE `tb_productos_fincas` DISABLE KEYS */;
INSERT INTO `tb_productos_fincas` VALUES (1,50.00,'2026-03-10',1,1),(2,40.00,'2026-03-12',1,2),(4,0.00,NULL,2,4),(5,0.00,NULL,2,5),(6,30.00,'2026-04-09',2,6),(7,35.00,'2026-04-06',1,7),(8,999.99,NULL,3,8),(9,0.00,NULL,4,9),(10,0.00,NULL,4,10);
/*!40000 ALTER TABLE `tb_productos_fincas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_servicios`
--

DROP TABLE IF EXISTS `tb_servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_servicios` (
  `id_servicio` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(250) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `id_asesor` int(11) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_servicio`),
  KEY `tb_servicios_id_asesor_8b54d9ea_fk_tb_asesores_id_usuario` (`id_asesor`),
  CONSTRAINT `tb_servicios_id_asesor_8b54d9ea_fk_tb_asesores_id_usuario` FOREIGN KEY (`id_asesor`) REFERENCES `tb_asesores` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_servicios`
--

LOCK TABLES `tb_servicios` WRITE;
/*!40000 ALTER TABLE `tb_servicios` DISABLE KEYS */;
INSERT INTO `tb_servicios` VALUES (1,'agricultura y produccion','activo',4,'servicio cultivo'),(4,'sevicio bueno','ACTIVO',19,'servicio de riego'),(5,'lindo servicio de riego','ACTIVO',19,'servicio de riego'),(6,'veterinaria de ganado','ACTIVO',19,'veterinaria'),(7,'Servicio que cuenta con todo un proceso de fertilización para cultivos somos profesionales en este ámbito un servicio para la satisfacción del cliente ','ACTIVO',19,'Servicio de fertilizante');
/*!40000 ALTER TABLE `tb_servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_transportistas`
--

DROP TABLE IF EXISTS `tb_transportistas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_transportistas` (
  `id_usuario` int(11) NOT NULL,
  `zonas_entrega` varchar(250) DEFAULT NULL,
  `id_calificacion` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `tb_transportistas_id_calificacion_2f642b2c_fk_tb_califi` (`id_calificacion`),
  CONSTRAINT `tb_transportistas_id_calificacion_2f642b2c_fk_tb_califi` FOREIGN KEY (`id_calificacion`) REFERENCES `tb_calificacion` (`id_calificacion`),
  CONSTRAINT `tb_transportistas_id_usuario_ebdfd2ce_fk_tb_usuarios_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_transportistas`
--

LOCK TABLES `tb_transportistas` WRITE;
/*!40000 ALTER TABLE `tb_transportistas` DISABLE KEYS */;
INSERT INTO `tb_transportistas` VALUES (5,'Cundinamarca',NULL),(18,'Bogota',NULL);
/*!40000 ALTER TABLE `tb_transportistas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_usuarios`
--

DROP TABLE IF EXISTS `tb_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `rol` varchar(50) NOT NULL,
  `latitud` double DEFAULT NULL,
  `longitud` double DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `tb_usuarios_user_id_980d4f70_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_usuarios`
--

LOCK TABLES `tb_usuarios` WRITE;
/*!40000 ALTER TABLE `tb_usuarios` DISABLE KEYS */;
INSERT INTO `tb_usuarios` VALUES (2,'Juanda','juan123','Perez','juan1@test.com','Bogotá','Cundinamarca','Calle 1','123456','3001234567','cliente',NULL,NULL,1,NULL),(3,'Jose','jose7','muños','jose@gmail.com','Chia','Cundinamarca','calle 2 b #03 04','1000665444','3004568932','productor',NULL,NULL,1,NULL),(4,'nicolas','nicolas777','rengifo','nicolas@gmail.com','Zipaquira','Cundinamarca','calle 15','144455668','3119876543','asesor',NULL,NULL,1,NULL),(5,'Felipe','perez117','perez','felipe2003@gmail.com','Granada','Cundinamarca','calle 14 sur #12 24','1000987456','3104567842','TRANSPORTISTA',NULL,NULL,1,NULL),(6,'camila','camila99','ramirez','cami11@gmail.com','Madrid','Cundinamarca','cr 117','8984774','3118763456','ASESOR',4.3556,-741550,1,NULL),(14,'Jeison','Jeison03','leon niño','jeisonandres117.03@gmail.com','Bogota','Cundinamarca','cr 1 Bis A #75 sur 14','1000694244','3128469052','CLIENTE',NULL,NULL,1,1),(15,'santiago','santiago117','leon','santiago@gmail.com','Granada','Cundinamarca','cr 1 Bis A #75 sur 18','10002026123','3104567857','CLIENTE',NULL,NULL,1,2),(17,'Alejo','Alejo2003','Niño','alejo2026@gmail.com','Bogotá','Cundinamarca','cr4b#12-90','9870098','3128469053','CLIENTE',4.3556,-741550,1,5),(18,'Nicolass','nico2026','Garzon','nico26@gmail.com','Chia','Cundinamarca','cr2b#12-13','8636403','310765890','TRANSPORTISTA',NULL,NULL,1,6),(19,'pablo','pablo2026','perez','pablo1@gmail.com','Bogotá','Cundinamarca','calle 100#100-7','8770097','31076588','ASESOR',NULL,NULL,1,7),(20,'camilo','camilo','sanchez','camilito@gmail.com','Chia','Cundinamarca','calle285 - norte','','3104567851','PRODUCTOR',NULL,NULL,1,8),(21,'alfredo','alfredo','Perez','alfred@gmail.com','Cajicá','Cundinamarca','cr2b#08-9','33757594975','3128469788','CLIENTE',NULL,NULL,1,9),(22,'Pedro','Admin2026','Rivera','admin7@gmail.com','Chía','Cundinamarca','calle 13','1000694577','3128469777','ADMINISTRADOR',NULL,NULL,1,10),(23,'jose','jose','rodriguez','jose3@gmail.com','Caparrapí','Cundinamarca','calle 14 sur #12 20','1334567800','3128469770','PRODUCTOR',NULL,NULL,1,11),(24,'daniel','danielcliente','lopez','daniel@gmail.com','Bojacá','Cundinamarca','cll 15#5-67','1994859677','3000000000','PRODUCTOR',NULL,NULL,1,12),(25,'Armando','Armando2020','Mendosa','armando20@gmail.com','Soacha','Cundinamarca','calle07#12-11','100567843','3128467021','CLIENTE',NULL,NULL,1,13);
/*!40000 ALTER TABLE `tb_usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_vehiculos`
--

DROP TABLE IF EXISTS `tb_vehiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_vehiculos` (
  `id_vehiculo` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_vehiculo` varchar(50) DEFAULT NULL,
  `capacidad_carga` decimal(10,2) DEFAULT NULL,
  `documento_propiedad` varchar(250) DEFAULT NULL,
  `placa_vehiculo` varchar(15) DEFAULT NULL,
  `id_transportista` int(11) NOT NULL,
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id_vehiculo`),
  KEY `tb_vehiculos_id_transportista_b1daa4c8_fk_tb_transp` (`id_transportista`),
  CONSTRAINT `tb_vehiculos_id_transportista_b1daa4c8_fk_tb_transp` FOREIGN KEY (`id_transportista`) REFERENCES `tb_transportistas` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_vehiculos`
--

LOCK TABLES `tb_vehiculos` WRITE;
/*!40000 ALTER TABLE `tb_vehiculos` DISABLE KEYS */;
INSERT INTO `tb_vehiculos` VALUES (1,'camion',500.00,'1004884','134-ujh',5,'ACTIVO'),(2,'furgon',3000.00,'1239040','777-jhf',5,'ACTIVO'),(6,'Camioneta',15000.00,NULL,'ABC905',18,'ACTIVO'),(7,'Camioneta',1000.00,NULL,'BCD234',18,'ACTIVO'),(8,'Van',3000.00,NULL,'FGH-023',18,'ACTIVO');
/*!40000 ALTER TABLE `tb_vehiculos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-20 18:42:25
