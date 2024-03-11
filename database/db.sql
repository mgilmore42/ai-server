CREATE TABLE [models] (
  [id] integer PRIMARY KEY,
  [name] nvarchar(255),
  [task_id] integer
)
GO

CREATE TABLE [users] (
  [id] integer PRIMARY KEY,
  [username] nvarchar(255),
  [role_id] integer,
  [creation] timestamp
)
GO

CREATE TABLE [roles] (
  [id] integer PRIMARY KEY,
  [name] nvarchar(255)
)
GO

CREATE TABLE [user_log] (
  [id] integer PRIMARY KEY,
  [user_id] integer,
  [event_id] integer,
  [time] timestamp
)
GO

CREATE TABLE [model_versions] (
  [id] integer PRIMARY KEY,
  [model_id] integer,
  [creator_id] integer,
  [version] nvarchar(255),
  [creation] timestamp
)
GO

CREATE TABLE [events] (
  [id] integer PRIMARY KEY,
  [name] nvarchar(255)
)
GO

CREATE TABLE [tasks] (
  [id] integer PRIMARY KEY,
  [name] nvarchar(255)
)
GO

ALTER TABLE [model_versions] ADD FOREIGN KEY ([model_id]) REFERENCES [models] ([id])
GO

ALTER TABLE [model_versions] ADD FOREIGN KEY ([creator_id]) REFERENCES [users] ([id])
GO

ALTER TABLE [user_log] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([id])
GO

ALTER TABLE [users] ADD FOREIGN KEY ([role_id]) REFERENCES [roles] ([id])
GO

ALTER TABLE [user_log] ADD FOREIGN KEY ([event_id]) REFERENCES [events] ([id])
GO

ALTER TABLE [models] ADD FOREIGN KEY ([task_id]) REFERENCES [tasks] ([id])
GO
