CREATE TABLE "servers" (
    "server_id"	INTEGER NOT NULL,
    "server_name"	TEXT NOT NULL,
    PRIMARY KEY("server_id")
);

CREATE TABLE "users" (
    "user_id"	INTEGER NOT NULL,
    "user_name"	TEXT NOT NULL,
    PRIMARY KEY("user_id")
);

CREATE TABLE "user_servers" (
    "user_id"	INTEGER NOT NULL,
    "server_id"	INTEGER NOT NULL,
    FOREIGN KEY("server_id") REFERENCES "servers"("server_id"),
    FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);

CREATE TABLE "violations" (
    "violation_id"	INTEGER,
    "violation_desc"	TEXT NOT NULL,
    PRIMARY KEY("violation_id")
);

CREATE TABLE "user_violations" (
    "user_id"	INTEGER,
    "violation_id"	INTEGER,
    "reason"	TEXT NOT NULL,
    FOREIGN KEY("violation_id") REFERENCES "violations"("violation_id"),
    FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);
