import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataclasses import dataclass
from lilota.core import LilotaScheduler, LilotaWorker
from lilota.models import Node, Task


scheduler = LilotaScheduler(
  db_url="postgresql+psycopg://postgres:postgres@localhost:5432/lilota_sample"
)

worker = LilotaWorker(
  db_url="postgresql+psycopg://postgres:postgres@localhost:5432/lilota_sample", 
  number_of_processes=1
)


@dataclass
class AddInput():
    a: int
    b: int


@dataclass
class AddOutput():
  sum: int


@worker.register("add", input_model=AddInput, output_model=AddOutput)
def add(input: AddInput) -> AddOutput:
   return AddOutput(input.a + input.b)


def main():
  node: Node = worker.get_node_by_id(worker.node_id)
  print(f"Scheduler ID: {node.id}")

  task_id = scheduler.schedule("add", AddInput(a=2, b=3))
  task: Task = scheduler.get_task_by_id(task_id)
  print(f"Task ID: {task.id}")

  worker.start()
  node: Node = worker.get_node_by_id(worker.node_id)
  print(f"Worker ID: {node.id}")


if __name__ == "__main__":
  main()