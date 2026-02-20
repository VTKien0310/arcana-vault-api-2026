CREATE TABLE IF NOT EXISTS "keys"
(
    "id"               UUID          NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    "user_id"          UUID          NOT NULL UNIQUE,
    "value"            VARCHAR(255)  NOT NULL,
    "channels"         INTEGER ARRAY NOT NULL,
    "expiration"       TIMESTAMPTZ   NOT NULL,
    "email"            VARCHAR(255),
    "telegram_chat_id" VARCHAR(255),
    "phone"            VARCHAR(255),
    "created_at"       TIMESTAMPTZ   NOT NULL        DEFAULT now(),
    "updated_at"       TIMESTAMPTZ   NOT NULL        DEFAULT now(),
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "collections"
(
    "id"         UUID         NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    "user_id"    UUID         NOT NULL,
    "name"       VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ  NOT NULL        DEFAULT now(),
    PRIMARY KEY ("id")
);

CREATE INDEX "collections_index_0"
    ON "collections" ("user_id");