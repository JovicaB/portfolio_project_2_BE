CREATE TABLE `p2_credit_portfolio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `debtor_name` varchar(45) DEFAULT NULL,
  `credit_value` float DEFAULT NULL,
  `interest_rate` float DEFAULT NULL,
  `credit_life` int DEFAULT NULL,
  `credit_approval_year` int DEFAULT NULL,
  `collateral_name` varchar(45) DEFAULT NULL,
  `collateral_value` float DEFAULT NULL,
  `collateral_cat` varchar(1) DEFAULT NULL,
  `risk` float DEFAULT NULL,
  `risk_status` varchar(45) DEFAULT NULL,
  `ponder_status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
