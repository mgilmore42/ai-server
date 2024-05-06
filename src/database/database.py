import sqlite3

from flask import current_app

from typing import Self

class Database:

	def __init__(self: Self) -> None:
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
	
	def get_user(self: Self, username: str) -> dict:
		"""Query the user registry for information on the selected user.

		Parameters
		----------
		username : str
			The username to get information on.

		Returns
		-------
		dict
			The response containing the user information.
		
		"""
		self.cursor.execute("SELECT username, roles.name FROM users INNER JOIN roles ON users.role_id = roles.id WHERE username = ?", (username,))

		if (result := self.cursor.fetchone()) is None:
			return {'message': f"User {username} does not exist."}
		else:
			return {
				'username': result[0],
				'role': result[1]
			}
	

	def get_model(self: Self, model_name: str, version: str) -> dict:
		"""Get information on a model.

		Parameters
		----------
		model : str
			The model to get information on.
		version : str
			The version of the model to get information on.

		Returns
		-------
		dict
			The response containing the model information.

		"""
		self.cursor.execute("SELECT models.name, tasks.name FROM models INNER JOIN tasks ON models.task_id = tasks.id WHERE models.name = ?", (model_name,))

		if (result := self.cursor.fetchone()) is None:
			return {'message': f"Model {model_name} does not exist."}
		
		self.cursor.execute("SELECT version FROM model_versions WHERE model_id = ? AND version = ?", (result[0], version))

		if (result := self.cursor.fetchone()) is None:
			return {'message': f"Model {model_name} does not have a version {version}."}
		else:
			return {
				'model': model_name,
				'task': result[1],
				'version': version
			}


	def add_role(self: Self, role: str) -> dict:
		"""Add a role to the database.
		
		Parameters
		----------
		role : str
			The role to add.
			
		Returns
		-------
		dict
			The response containing the role information.

		"""
		# Check if the role already exists
		self.cursor.execute("SELECT id FROM roles WHERE name=?", (role,))

		if (result := self.cursor.fetchone()) is None:
			self.cursor.execute("INSERT INTO roles (name) VALUES (?)", (role,))
			self.conn.commit()
			return {'message': f"Role {role} added successfully."}
		else:
			return {'message': f"Role {role} already exists."}

		
	def add_user(self: Self, username: str, role: str) -> dict:
		"""Add a user to the database.

		Parameters
		----------
		username : str
			The username to add.
		role : str
			The role of the user to add.

		Returns
		-------
		dict
			The response containing the user information.

		"""

		# Check if the user already exists
		self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
		existing_user = self.cursor.fetchone()

		# If the user doesn't exist, insert it into the database
		if existing_user is None:
			self.cursor.execute("SELECT id FROM roles WHERE name=?", (role,))
			role_id = self.cursor.fetchone()[0]
			self.cursor.execute("INSERT INTO users (username, role_id) VALUES (?, ?)", (username, role_id))
			self.conn.commit()
			return {'message': f"User {username} added successfully."}
		else:
			return {'message': f"User {username} already exists."}

	
	def add_model(self: Self, model_name: str, task_name: str) -> dict:
		"""Add a model to the database.

		Parameters
		----------
		model_name : str
			The name of the model to add.
		task_name : str
			The task the model is intended for.

		Returns
		-------
		dict
			The response containing the model information.

		"""
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

	
	def add_model_version(self: Self, model_name: str, version: str, creator: str) -> dict:
		"""Add a version to a model.

		Parameters
		----------
		model_name : str
			The name of the model to add the version to.
		version : str
			The version to add.
		creator : str
			The user creating the version.

		Returns
		-------
		dict
			The response containing the version information.

		"""
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

	def close(self: Self)-> None:
		"""Close the database connection."""

		self.conn.close()
