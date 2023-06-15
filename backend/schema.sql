DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS personality;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );

CREATE TABLE chat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  personality_id INTEGER NOT NULL,
  messages TEXT NOT NULL,
  UNIQUE (user_id, personality_id),
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (personality_id) REFERENCES personality (id)
);

CREATE TABLE personality (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT NOT NULL,
  system_prompt TEXT
);