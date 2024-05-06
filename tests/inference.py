import pytest

from ai_server.database.database import Database

def test_add_role():
	db = Database()
	db.add_role("test_role")

	db.cursor.execute("SELECT * FROM roles WHERE name='test_role'")
	result = db.cursor.fetchone()

	assert result is not None

def test_add_user():
	db = Database()
	db.add_user("test_user", "test_role")

	db.cursor.execute("SELECT * FROM users WHERE username='test_user'")
	result = db.cursor.fetchone()

	assert result is not None

def test_get_user():
	db = Database()
	result = db.get_user("test_user")

	assert result['username'] == "test_user"
	assert result['role'] == "test_role"


def test_add_task():
	db = Database()
	db.add_task("test_task")

	db.cursor.execute("SELECT * FROM tasks WHERE name='test_task'")
	result = db.cursor.fetchone()

	assert result is not None

def test_add_model():
	db = Database()
	db.add_model("test_model", "test_task")

	db.cursor.execute("SELECT * FROM models WHERE name='test_model'")
	result = db.cursor.fetchone()

	assert result is not None

def test_add_model_version():
	db = Database()
	foo = db.add_model_version("test_model", "test_version", "test_user")

	db.cursor.execute("SELECT * FROM model_versions WHERE version='test_version'")
	result = db.cursor.fetchone()

	assert result is not None

def test_get_model():
	db = Database()
	result = db.get_model("test_model", "test_version")

	print(result)

	assert result['model'] == "test_model"
	assert result['task'] == "test_task"
	assert result['version'] == "test_version"

# def test_get_task():
# 	db = Database()
# 	result = db.get_task("test_task")

# 	assert result['task_name'] == "test_task"