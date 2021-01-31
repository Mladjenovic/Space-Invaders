from multiprocessing import Process, Pipe
import random

import time


class DeusExProcess(Process):

    def __init__(self, pipe: Pipe, max_arg: int):
        super().__init__(target=self.__count__, args=[pipe])
        self.max = max_arg

    def __count__(self, pipe: Pipe):
        pipe.recv()

        while True:
            time.sleep(15)
            x = random.randrange(200, 900)
            y = random.randrange(50, 350)
            luckyFactor = random.choice(range(-1, 2, 2))
            pipe.send([x, y, luckyFactor])


        '''
        for i in range(self.max):
            pipe.send(i)
            print("send {0}".format(i))
            time.sleep(0.05)
        '''
        pipe.send('end')
