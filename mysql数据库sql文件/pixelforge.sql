/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80043 (8.0.43)
 Source Host           : localhost:3306
 Source Schema         : pixelforge

 Target Server Type    : MySQL
 Target Server Version : 80043 (8.0.43)
 File Encoding         : 65001

 Date: 25/05/2026
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for generation_history
-- ----------------------------
DROP TABLE IF EXISTS `generation_history`;
CREATE TABLE `generation_history`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '数据库自增ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `task_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '唯一任务ID',
  `asset_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '素材类型',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户输入的描述',
  `style` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '像素风' COMMENT '艺术风格',
  `size` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '1024*1024' COMMENT '图片尺寸',
  `n` int NULL DEFAULT 1 COMMENT '生成数量',
  `watermark` int NULL DEFAULT 0 COMMENT '是否加水印: 0=无, 1=有',
  `model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '使用的AI模型',
  `prompt` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '实际发送给AI的完整提示词',
  `local_paths` json NULL COMMENT '生成的图片本地路径数组',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending' COMMENT '任务状态',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `error` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '错误信息',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `task_id`(`task_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_task_id`(`task_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `fk_history_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '生成历史记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of generation_history
-- ----------------------------
INSERT INTO `generation_history` VALUES (1, 1, 'gen_20260524160432_14e54b', 'character', '一个身穿银色盔甲的骑士，身骑披着银色盔甲的战马，手持长矛指向前方', '像素风', '1024*1024', 1, 0, 'wan2.5-t2i-preview', '一个身穿银色盔甲的骑士，身骑披着银色盔甲的战马，手持长矛指向前方, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[]', 'failed', '2026-05-24 16:04:32', NULL);
INSERT INTO `generation_history` VALUES (2, 1, 'gen_20260524160845_74d720', 'character', '一个身穿银色盔甲的骑士，身骑披着银色盔甲的战马，手持长矛指向前方', '像素风', '1024*1024', 1, 0, 'wan2.5-t2i-preview', '一个身穿银色盔甲的骑士，身骑披着银色盔甲的战马，手持长矛指向前方, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[\"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\character_20260524_160948_51444224.png\"]', 'completed', '2026-05-24 16:08:46', NULL);
INSERT INTO `generation_history` VALUES (3, 1, 'gen_20260524194539_574bcd', 'character', '像素风红发女战士', '像素风', '512x512', 1, 0, 'wan2.5-t2i-preview', '像素风红发女战士, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[]', 'failed', '2026-05-24 19:45:40', NULL);
INSERT INTO `generation_history` VALUES (4, 1, 'gen_20260524194642_7912ca', 'character', '像素风红发女战士', '像素风', '1024x1024', 1, 0, 'wan2.5-t2i-preview', '像素风红发女战士, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[]', 'failed', '2026-05-24 19:46:43', NULL);
INSERT INTO `generation_history` VALUES (5, 1, 'gen_20260524194730_f29fe7', 'character', '一个身穿铠甲的战士', '像素风', '1024*1024', 1, 0, 'wan2.5-t2i-preview', '一个身穿铠甲的战士, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[\"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\character_20260524_194752_81621dbf.png\"]', 'completed', '2026-05-24 19:47:31', NULL);
INSERT INTO `generation_history` VALUES (6, 1, 'gen_20260524195916_0df002', 'character', '像素风的骑士', '像素风', '512x512', 1, 0, 'wan2.5-t2i-preview', '像素风的骑士, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[]', 'failed', '2026-05-24 19:59:17', NULL);
INSERT INTO `generation_history` VALUES (7, 1, 'gen_20260524200702_3e012f', 'character', '女骑士', '像素风', '1024*1024', 1, 0, 'wan2.5-t2i-preview', '女骑士, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[\"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\character_20260524_200718_b4cd70e0.png\"]', 'completed', '2026-05-24 20:07:02', NULL);
INSERT INTO `generation_history` VALUES (8, 1, 'gen_20260524201304_a52baf', 'prop', '做一把寒冰剑', '像素风', '1024*1024', 4, 0, 'wan2.5-t2i-preview', '做一把寒冰剑, 2D game item/prop, icon, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art', '[\"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\prop_20260524_201326_48afd2f2.png\", \"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\prop_20260524_201346_b840a38b.png\", \"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\prop_20260524_201406_97739a2a.png\", \"D:\\\\新项目\\\\PixelForge-main\\\\PixelForge-main\\\\backend\\\\image\\\\prop_20260524_201419_1cf8dbb4.png\"]', 'completed', '2026-05-24 20:13:05', NULL);

SET FOREIGN_KEY_CHECKS = 1;
