import random
import string
import json
from locust import HttpLocust, TaskSequence, seq_task
from configargparse import ArgumentParser




class UserBehavior(TaskSequence):
    def on_start(self):
        self.kitten = {
            "name": ''.join((random.choice(string.ascii_letters + string.digits) for _ in range(32))),
            "age": random.randint(1, 10)
        }
        self.endpoint = "/dev/v1/kitten"

    @seq_task(1)
    def create(self):
       self.client.post(self.endpoint, data=json.dumps(self.kitten))

    @seq_task(2)
    def update(self):
       self.kitten["age"] += 1
       self.client.put(self.endpoint, data=json.dumps(self.kitten))

    @seq_task(4)
    def delete(self):
       self.client.delete(self.endpoint, data=json.dumps(self.kitten))

    def on_stop(self):
        self.delete()

class APIUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000

