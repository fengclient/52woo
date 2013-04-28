/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `wp_users` (
--   `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
--   `user_login` varchar(60) NOT NULL DEFAULT '',
--   `user_pass` varchar(64) NOT NULL DEFAULT '',
--   `user_nicename` varchar(50) NOT NULL DEFAULT '',
--   `user_email` varchar(100) NOT NULL DEFAULT '',
--   `user_url` varchar(100) NOT NULL DEFAULT '',
--   `user_registered` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
--   `user_activation_key` varchar(60) NOT NULL DEFAULT '',
--   `user_status` int(11) NOT NULL DEFAULT '0',
--   `display_name` varchar(250) NOT NULL DEFAULT '',
--   PRIMARY KEY (`ID`),
--   KEY `user_login_key` (`user_login`),
--   KEY `user_nicename` (`user_nicename`)
-- ) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

-- accounts = {'shuaymm':u'爱刷牙的猫猫', 'cocoyang':u'Co0O~吐泡比较帅',
-- 'huanhuan001':u'美娘子欢欢', 'lyl1990':u'娜娜爱暹罗猫', 'fiwal000':u'Dogge伯爵', 'ysy0904':u'折耳澈'}
USE xiaofeng_wp323;
-- INSERT INTO `wp_users` VALUES (1,'admin','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','admin','admin@52woo.com','','2013-03-13 04:57:02','',0,'admin');
INSERT INTO `wp_users` VALUES (2,'shuaymm','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','爱刷牙的猫猫','admin@52woo.com','','2013-03-13 04:57:02','',0,'爱刷牙的猫猫');
INSERT INTO `wp_users` VALUES (3,'cocoyang','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','Co0O~吐泡比较帅','admin@52woo.com','','2013-03-13 04:57:02','',0,'Co0O~吐泡比较帅');
INSERT INTO `wp_users` VALUES (4,'huanhuan001','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','美娘子欢欢','admin@52woo.com','','2013-03-13 04:57:02','',0,'美娘子欢欢');
INSERT INTO `wp_users` VALUES (5,'lyl1990','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','娜娜爱暹罗猫','admin@52woo.com','','2013-03-13 04:57:02','',0,'娜娜爱暹罗猫');
INSERT INTO `wp_users` VALUES (6,'fiwal000','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','Dogge伯爵','admin@52woo.com','','2013-03-13 04:57:02','',0,'Dogge伯爵');
INSERT INTO `wp_users` VALUES (7,'ysy0904','$P$B0GGkBLQKDI4P9YiBX67AFjC7vGcjO1','折耳澈','admin@52woo.com','','2013-03-13 04:57:02','',0,'折耳澈');