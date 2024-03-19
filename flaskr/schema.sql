DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_message;
DROP TABLE IF EXISTS app_conversation;
DROP TABLE IF EXISTS user_conversation_membership;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE app_conversation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  is_group BOOLEAN DEFAULT FALSE
);

CREATE TABLE user_conversation_membership (
  conversation_id INTEGER,
  user_id INTEGER,
  PRIMARY KEY (conversation_id, user_id),
  FOREIGN KEY (conversation_id) REFERENCES app_conversation (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE user_message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  conversation_id INTEGER NOT NULL,
  message_sent_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  message_sent_bool BOOLEAN DEFAULT FALSE,
  message_delivered_bool BOOLEAN DEFAULT FALSE,
  message_read_bool BOOLEAN DEFAULT FALSE,
  body TEXT NOT NULL,
  FOREIGN KEY (sender_id) REFERENCES user (id),
  FOREIGN KEY (conversation_id) REFERENCES app_conversation (id)
);