CREATE TABLE `qqmsg`.`group_msg` (
  `current_qq` bigint(20) NOT NULL,
  `from_nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `from_user_id` bigint(20) NOT NULL,
  `from_group_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `from_group_id` bigint(20) NOT NULL,
  `at_user_id` bigint(20) DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pics` text,
  `tips` text,
  `redbag_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `msg_time` bigint(20) NOT NULL,
  `msg_type` varchar(40) NOT NULL,
  `msg_seq` bigint(20) NOT NULL,
  `msg_random` bigint(20) NOT NULL
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE `qqmsg`.`group_msg`
  ADD PRIMARY KEY (`current_qq`, `from_user_id`, `from_group_id`, `msg_seq`);


CREATE TABLE `qqmsg`.`img` (
  `FileId` bigint(20) NOT NULL,
  `FileMd5` text NOT NULL,
  `FileSize` bigint(20) NOT NULL,
  `ForwordBuf` text DEFAULT NULL,
  `ForwordField` bigint(20) DEFAULT NULL,
  `Url` text NOT NULL,
  `Path` text DEFAULT NULL,
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE `qqmsg`.`img`
  ADD PRIMARY KEY (`FileId`);

ALTER TABLE `qqmsg`.`img`
  MODIFY `FileId` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;


CREATE TABLE `qqmsg`.`friend_msg` (
  `current_qq` bigint(20) NOT NULL,
  `from_user_id` bigint(20) NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ,
  `pics` text,
  `tips` text,
  `redbag_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `msg_time` bigint(20) NOT NULL,
  `msg_type` varchar(40) NOT NULL,
  `msg_seq` bigint(20) DEFAULT NULL
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE `qqmsg`.`friend_msg`
  ADD PRIMARY KEY (`current_qq`, `from_user_id`, `msg_seq`);
  
  
  
  