DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_message;
DROP TABLE IF EXISTS group_conversation;
DROP TABLE IF EXISTS user_conversation_membership;
DROP TABLE IF EXISTS direct_message;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE direct_conversation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_1 INTEGER,
  member_2 INTEGER,
  FOREIGN KEY (member_1) REFERENCES user (id),
  FOREIGN KEY (member_2) REFERENCES user (id)
);

CREATE TABLE group_conversation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  admin_id INTEGER,
  FOREIGN KEY (admin_id) REFERENCES user (id)
);

CREATE TABLE group_conversation_membership (
  conversation_id INTEGER,
  user_id INTEGER,
  PRIMARY KEY (conversation_id, user_id),
  FOREIGN KEY (conversation_id) REFERENCES group_conversation (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE direct_message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  conversation_id INTEGER NOT NULL,
  message_sent_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  message_sent_bool BOOLEAN DEFAULT FALSE,
  message_delivered_bool BOOLEAN DEFAULT FALSE,
  message_read_bool BOOLEAN DEFAULT FALSE,
  body TEXT NOT NULL,
  FOREIGN KEY (sender_id) REFERENCES user (id),
  FOREIGN KEY (conversation_id) REFERENCES direct_conversation (id)
);

CREATE TABLE group_message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  conversation_id INTEGER NOT NULL,
  message_sent_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (sender_id) REFERENCES user (id),
  FOREIGN KEY (conversation_id) REFERENCES group_conversation (id)
);