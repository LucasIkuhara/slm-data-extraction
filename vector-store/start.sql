CREATE EXTENSION IF NOT EXISTS VECTOR;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS EMBEDDING (
	ID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	SOURCE_FILE VARCHAR(100) NOT NULL,
	PAGE_NUM INT NOT NULL,
	EMBEDDING VECTOR(4096) NOT NULL
)
