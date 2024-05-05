import sqlite3
import logging

class Database:

	def __init__(self, logger = None):
		self.conn = sqlite3.connect('database.db')
		self.cursor = self.conn.cursor()

		if logger is None:
			self.logger = logging.getLogger(__name__)
		else:
			self.logger = logger

		# initialize the database
		self.cursor.executescript('''
				CREATE TABLE IF NOT EXISTS models (
				id INTEGER PRIMARY KEY,
				name TEXT,
				task_id INTEGER,
				FOREIGN KEY (task_id) REFERENCES tasks(id)
			);

			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY,
				username TEXT,
				role_id INTEGER,
				creation TIMESTAMP,
				FOREIGN KEY (role_id) REFERENCES roles(id)
			);

			CREATE TABLE IF NOT EXISTS roles (
				id INTEGER PRIMARY KEY,
				name TEXT
			);

			CREATE TABLE IF NOT EXISTS user_log (
				id INTEGER PRIMARY KEY,
				user_id INTEGER,
				event_id INTEGER,
				time TIMESTAMP,
				FOREIGN KEY (user_id) REFERENCES users(id),
				FOREIGN KEY (event_id) REFERENCES events(id)
			);

			CREATE TABLE IF NOT EXISTS model_versions (
				id INTEGER PRIMARY KEY,
				model_id INTEGER,
				creator_id INTEGER,
				version TEXT,
				creation TIMESTAMP,
				FOREIGN KEY (model_id) REFERENCES models(id),
				FOREIGN KEY (creator_id) REFERENCES users(id)
			);

			CREATE TABLE IF NOT EXISTS events (
				id INTEGER PRIMARY KEY,
				name TEXT
			);

			CREATE TABLE IF NOT EXISTS tasks (
				id INTEGER PRIMARY KEY,
				name TEXT
			);
		''')
	
	def get_user(self, username):
		self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
		return self.cursor.fetchone()
	
	def add_role(self, role):
		# Check if the role already exists
		self.cursor.execute("SELECT id FROM roles WHERE name=?", (role,))
		existing_role = self.cursor.fetchone()

		# If the role doesn't exist, insert it into the database
		if not existing_role:
			self.cursor.execute("INSERT INTO roles (name) VALUES (?)", (role,))
			self.conn.commit()
		else:
			print("Role already exists in the database.")
		
	def add_user(self, username, role) -> bool:

		# Check if the user already exists
		self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
		existing_user = self.cursor.fetchone()

		# If the user doesn't exist, insert it into the database
		if not existing_user:
			self.cursor.execute("SELECT id FROM roles WHERE name=?", (role,))
			role_id = self.cursor.fetchone()[0]
			self.cursor.execute("INSERT INTO users (username, role_id) VALUES (?, ?)", (username, role_id))
			self.conn.commit()
		else:
			print("User already exists in the database.")
	
	def add_model(self, model_name, task_name):
		# Check if the model already exists
		self.cursor.execute("SELECT id FROM models WHERE name=?", (model_name,))
		existing_model = self.cursor.fetchone()

		# If the model doesn't exist, insert it into the database
		if not existing_model:
			self.cursor.execute("SELECT id FROM tasks WHERE name=?", (task_name,))
			task_id = self.cursor.fetchone()[0]
			self.cursor.execute("INSERT INTO models (name, task_id) VALUES (?, ?)", (model_name, task_id))
			self.conn.commit()
		else:
			print("Model already exists in the database.")
	
	def add_model_version(self, model_name, version, creator):
		# Check if the model version already exists
		self.cursor.execute("SELECT id FROM models WHERE name=?", (model_name,))
		model_id = self.cursor.fetchone()[0]
		self.cursor.execute("SELECT id FROM users WHERE username=?", (creator,))
		creator_id = self.cursor.fetchone()[0]
		self.cursor.execute("INSERT INTO model_versions (model_id, creator_id, version, creation) VALUES (?, ?, ?, datetime('now'))", (model_id, creator_id, version))
		self.conn.commit()
	
	def add_event(self, event_name):
		# Check if the event already exists
		self.cursor.execute("SELECT id FROM events WHERE name=?", (event_name,))
		existing_event = self.cursor.fetchone()

		# If the event doesn't exist, insert it into the database
		if not existing_event:
			self.cursor.execute("INSERT INTO events (name) VALUES (?)", (event_name,))
			self.conn.commit()
		else:
			print("Event already exists in the database.")
	
	def add_task(self, task_name):
		# Check if the task already exists
		self.cursor.execute("SELECT id FROM tasks WHERE name=?", (task_name,))
		existing_task = self.cursor.fetchone()

		# If the task doesn't exist, insert it into the database
		if not existing_task:
			self.cursor.execute("INSERT INTO tasks (name) VALUES (?)", (task_name,))
			self.conn.commit()
		else:
			print("Task already exists in the database.")
	
	def add_user_log(self, username, event_name):
		# Get the user id
		self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
		user_id = self.cursor.fetchone()[0]

		# Get the event id
		self.cursor.execute("SELECT id FROM events WHERE name=?", (event_name,))
		event_id = self.cursor.fetchone()[0]

		self.cursor.execute("INSERT INTO user_log (user_id, event_id, time) VALUES (?, ?, datetime('now'))", (user_id, event_id))
		self.conn.commit()

	def close(self):
		self.conn.close()
		self.logger.info("Database connection closed.")

