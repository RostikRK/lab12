from arrays import Array
from arrayqueue import ArrayQueue
from people import TicketAgent, Passenger
import random


class TicketCounterSimulation:  # Create a simulation object.

    # Parameters supplied by the user.
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes
        self._pas_queue = ArrayQueue()  # manage the passangers
        self._agents_a = Array(numAgents)
        for i in range(numAgents):
            self._agents_a[i] = TicketAgent(i + 1)
        self._totalWaitTime = 0
        self._numPassengers = 0

    # Run the simulation using the parameters supplied earlier.

    def run(self):
        for curTime in range(self._numMinutes + 1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def _handleArrival(self, time):
        """
        Handles arrival of passenger.
        """
        random_value = random.random
        if self._arriveProb > random_value:
            self._pas_queue.add(Passenger(self._numPassengers, time))
            self._numPassengers += 1

    def _handleBeginService(self, time):
        """
        Handles the beginning of the service. Matches
        free agent and passangers
        """
        while not self._pas_queue.isEmpty():
            found_agent = False
            for agent in self._agents_a:
                if agent.isFree():
                    passenger = self._pas_queue.pop()
                    self._totalWaitTime += time - passenger.timeArrived()
                    agent.startService(passenger, time + self._serviceTime)
                    found_agent = True
                if found_agent:
                    break
            if not found_agent:
                break

    def _handleEndService(self, time):
        """
        Handles the ending of the service
        """
        for agent in self._agents_a:
            if agent.isFinished(time):
                agent.stopService()

    # Print the simulation results.

    def printResults(self):
        """
        Prints results for the whole simulation
        """
        numServed = self._numPassengers - len(self._pas_queue)
        avgWait = float(self._totalWaitTime) / numServed
        print("")
        print("Number of passengers served = ", numServed)
        print("Number of passengers remaining in line = %d" %
              len(self._pas_queue))
        print("The average wait time was %4.2f minutes." % avgWait)


if __name__ == '__main__':
    random.seed(100000)
    ticcoun = TicketCounterSimulation(10, 10000, 2, 4)
    ticcoun.run()
    ticcoun.printResults()
