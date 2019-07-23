
-- 导出 region 的数据库结构
CREATE DATABASE IF NOT EXISTS `region` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `region`;

-- 导出  表 region.region 结构
CREATE TABLE IF NOT EXISTS `region` (
  `id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `region_code` varchar(255) NOT NULL DEFAULT '-1',
  `region_name` varchar(255) NOT NULL DEFAULT '-1',
  `parent_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `region_level` int(11) NOT NULL DEFAULT '-1',
  `create_time` int(11) NOT NULL DEFAULT '-1',
  `update_time` int(11) NOT NULL DEFAULT '-1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域信息表';

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
