CREATE TABLE merkletree (
  mid int NOT NULL,
  tree_data      text(40000) NOT NULL,
  blockNumber      int NOT NULL,
  last_modified_date  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_date        TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
)ENGINE = InnoDB;

CREATE TABLE contract (
  conName char(20) NOT NULL,
  conType  char(20) NOT NULL,
  conAddr text(500) NOT NULL,
  owner text(500) NOT NULL,
  totalAmount bigint NOT NULL,
  shortName char(20) NOT NULL,
  last_modified_date  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_date        TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
)ENGINE = InnoDB;

CREATE TABLE transactions (
  traType char(20) NOT NULL,
  username  char(20) NOT NULL,
  vin int NOT NULL,
  vout int NOT NULL,
  input_notes char(40),
  output_specs text(2000),
  last_modified_date  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_date        TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
)ENGINE = InnoDB;
