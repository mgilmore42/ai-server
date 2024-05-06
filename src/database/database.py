import sqlite3

from flask import current_app

class Database:

	def __init__(self):
		self.conn = sqlite3.connect('database.db')
		self.cursor = self.conn.cursor()

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
		self.cursor.execute("SELECT username, roles.name FROM users INNER JOIN roles ON users.role_id = roles.id WHERE username = ?", (username,))

		if (result := self.cursor.fetchone()) is not None:
			return {
				'username': result[0],
				'role': result[1]
			}
	
	def get_model(self, model_name, version):
		self.cursor.execute("SELECT models.name, tasks.name FROM models INNER JOIN tasks ON models.task_id = tasks.id WHERE models.name = ?", (model_name,))

		if (result := self.cursor.fetchone()) is None:
			return {'message': f"Model {model_name} does not exist."}
		
		self.cursor.execute("SELECT version FROM model_versions WHERE model_id = ? AND version = ?", (result[0], version))

		if (result := self.cursor.fetchone()) is not None:
			return {
				'model': model_name,
				'task': result[1],
				'version': version
			}


	def add_role(self, role) -> dict:
		# Check if the role already exists
		self.cursor.execute("SELECT id FROM roles WHERE name=?", (role,))

		if (result := self.cursor.fetchone()) is None:
			self.cursor.execute("INSERT INTO roles (name) VALUES (?)", (role,))
			self.conn.commit()
			return {'message': f"Role {role} added successfully."}
		else:
			return {'message': f"Role {role} already exists."}

		
	def add_user(self, username, role) -> bool:

		# Check if the user already exists
		self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
		existing_user = self.cursor.fetchone()

		# If the user doesn't exist, insert it into the database
		if existing_user is None:
			self.cursor.execute("SELECT id FROM roles WHERE name=?", (role,))
			role_id = self.cursor.fetchone()[0]
			self.cursor.execute("INSERT INTO users (username, role_id) VALUES (?, ?)", (username, role_id))
			self.conn.commit()

	
	def add_model(self, model_name, task_name) -> dict:
		# Check if the model already exists
		self.cursor.execute("SELECT id FROM models WHERE name=?", (model_name,))
		existing_model = self.cursor.fetchone()

		# If the model doesn't exist, insert it into the database
		if existing_model is None:
			self.cursor.execute("SELECT id FROM tasks WHERE name=?", (task_name,))
			
			if (result := self.cursor.fetchone()) is None:
				return {'message': f"Task {task_name} does not exist."}

			self.cursor.execute("INSERT INTO models (name, task_id) VALUES (?, ?)", (model_name, result[0]))
			self.conn.commit()

			return {'message': f"Model {model_name} added successfully."}
		else:
			return {'message': f"Model {model_name} already exists."}

	
	def add_model_version(self, model_name, version, creator) -> dict:
		# Check if the model version already exists
		self.cursor.execute("SELECT id FROM models WHERE name=?", (model_name,))

		if (result := self.cursor.fetchone()) is None:
			current_app.logger.error(f"Model {model_name} does not exist.")
			return {'message': f"Model {model_name} does not exist. Cannot add version until the base model is created."}
		else:
			model_id = result[0]
		
		self.cursor.execute("SELECT id FROM users WHERE username=?", (creator,))

		# check it the version already exists
		self.cursor.execute("SELECT id FROM model_versions WHERE model_id = ? AND version = ?", (model_id, version))

		if self.cursor.fetchone() is None:
			self.cursor.execute("SELECT id FROM users WHERE username=?", (creator,))

			if (result := self.cursor.fetchone()) is None:
				current_app.logger.error(f"User {creator} does not exist.")
				return {'message': f"User {creator} does not exist."}

			creator_id = result[0]
			self.cursor.execute("INSERT INTO model_versions (model_id, creator_id, version, creation) VALUES (?, ?, ?, datetime('now'))", (model_id, creator_id, version))
			self.conn.commit()

			return {'message': f"Training version {version} added to model {model_name} successfully."}
		else:
			return {'message': f"Model {model_name} already has a version {version}."}


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
