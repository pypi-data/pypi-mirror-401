import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from alembic import command
from dataclasses import dataclass
from unittest import TestCase, main
from typing import Any
from multiprocessing import cpu_count
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lilota.core import LilotaScheduler
from lilota.models import Node, NodeType, NodeStatus, Task, TaskStatus, TaskProgress
from lilota.db.alembic import get_alembic_config


@dataclass
class AddInput():
    a: int
    b: int


@dataclass
class AddOutput():
  sum: int


def add(data: AddInput) -> AddOutput:
  return AddOutput(sum=data.a + data.b)


def hello_world():
  print("Hello Word")



class LilotaSchedulerTestCase(TestCase):

  DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5433/lilota_test"

  @classmethod
  def setUpClass(cls):
    super().setUpClass()

    # Apply the migrations
    cfg = get_alembic_config(db_url=LilotaSchedulerTestCase.DB_URL)
    try:
      command.upgrade(cfg, "head")
    except Exception as ex:
      raise Exception(f"Could not update the database: {str(ex)}")
    
    # Create SQLAlchemy engine and session
    engine = create_engine(cls.DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete all tasks and nodes
    session.query(Task).delete()
    session.query(Node).delete()
    session.commit()
    session.close()


  def setUp(self):
    pass


  def test_initialize___should_create_node(self):
    # Act
    lilota = LilotaScheduler(LilotaSchedulerTestCase.DB_URL)

    # Assert
    node: Node = lilota.get_node_by_id(lilota.node_id)
    self.assertEqual(node.id, lilota.node_id)
    self.assertEqual(node.type, NodeType.SCHEDULER)
    self.assertEqual(node.status, NodeStatus.RUNNING)
    self.assertIsNotNone(node.created_at)
    self.assertIsNotNone(node.last_seen_at)


  def test_schedule___should_create_task(self):
    # Arrange
    lilota = LilotaScheduler(LilotaSchedulerTestCase.DB_URL)

    # Act
    task_id = lilota.schedule("add", AddInput(2, 3))

    # Assert
    task: Task = lilota.get_task_by_id(task_id)
    self.assertEqual(task.name, "add")
    self.assertEqual(task.status, TaskStatus.PENDING)
    self.assertIsNone(task.exception)
    self.assertEqual(task.progress_percentage, 0)
    self.assertEqual(task.input['a'], 2)
    self.assertEqual(task.input['b'], 3)
    self.assertIsNone(task.output)
    self.assertIsNone(task.locked_at)
    self.assertIsNone(task.locked_by)


if __name__ == '__main__':
  main()