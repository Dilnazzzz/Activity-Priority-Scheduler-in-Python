# Activity Priority Scheduler

The scheduler uses a priority queue as the primary data structure to plan the execution of the tasks. I wrote my own max- and min-heap implementation (rather than using the heapq module). The scheduler keeps a clock, expressed in units of minutes, that gets incremented by a fixed time-step (an interval in time). The scheduler outputs a step-by-step execution of the input tasks as well as a report on the total amount of time required to execute all the tasks.
