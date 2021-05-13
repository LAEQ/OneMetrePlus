import time
import threading, queue
import random


class Messenger:
    def __init__(self):
        self.q = queue.Queue(maxsize=60)

    def worker(self):
        while True:
            message = self.q.get()
            print(message)

        print("DONE")

    def put(self, message):
        # print("ICIT")
        self.q.put(message)

    def join(self):
        self.q.join()


# def worker():
#     while True:
#         item = q.get()
#         print(f'Working on {item}')
#         print(f'Finished {item}')
#         time.sleep(1)
#         q.task_done()


if __name__ == "__main__":
    messager = Messenger()

    # send thirty task requests to the worker
    for item in range(30):
        messager.put(item)

    messager.start()

    while True:
        time.sleep(5)
        messager.put(random.random())
        pass

    print('All task requests sent\n', end='')

    # block until all tasks are done
    q.join()
    print('All work completed')



