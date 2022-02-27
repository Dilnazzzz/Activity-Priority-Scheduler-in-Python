#!/usr/bin/env python
# coding: utf-8

# ### Program an activity scheduler in Python, which receives the list of tasks above as input and returns a schedule for you to follow.

# In[ ]:


#import sys module to acess variables used or maintained by the interpreter
import sys

class MinHeap:
    """
    A class with methods to create a min heap, push a new element and pop the root
    Input: maximum size of the heap 
    """
    # initialization
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0]*(self.maxsize + 1)
        self.Heap[0] = -1 * sys.maxsize
        self.FRONT = 1
 
    def parent(self, pos):
        """
        Input: position of the node
        Output: the position of parent at pos
        """
        return pos // 2
 
    def leftChild(self, pos):
        """
        Input: position of the node
        Output: position of the left child
        """       
        return 2 * pos
 
    def rightChild(self, pos):
        """
        Input: position of the node
        Output: position of the right child
        """   
        return (2 * pos) + 1
 
    def isLeaf(self, pos):
        """
        Input: position of the node
        Output: returns true if the passed node is a leaf node
        """   
        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False
 
    def swap(self, fpos, spos):
        """
        Swaps two nodes
        Input: position of two node
        """ 
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    def minHeapify(self, pos):
        """
        A function that heapifies the node at pos
        Input: position of the node
        """ 
        # compare a non-leaf node and its child
        if not self.isLeaf(pos):
            if (self.Heap[pos] > self.Heap[self.leftChild(pos)] or
               self.Heap[pos] > self.Heap[self.rightChild(pos)]):
 
                # swap the node with the left child and heapify the left child
                if self.Heap[self.leftChild(pos)] < self.Heap[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
 
                # swap the node with the right child and heapify the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    def insert(self, element):
        """
        A function that inserts an element into the heap
        Input: position of the node
        """ 
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.Heap[self.size] = element
 
        current = self.size
 
        while self.Heap[current] < self.Heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
  
    def minHeap(self):
        """
        A function that builds the min heap
        """ 
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    def remove(self):
        """
        A function that removes and pops the root element
        Output: the root of the heap
        """ 
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped


# In[ ]:


class Task:
    """
    A class that stores the input which is referred in TaskScheduler
    Input:
    - id: a unique task identifier (that can be referenced by other tasks)  
    - priority: priority level of a task  
    - description: a short description of the task
    - duration: duration in minutes  
    - dependencies: list of id’s indicating whether the current task cannot begin until all of its dependencies have been completed
    - status: the state of a task; possible values are not_yet_started, in_progress, or completed.      
    """
    # initializes an instance of Task
    def __init__(self,task_id,priority,description,duration,dependencies,status="N"):
        self.id = task_id
        self.priority = priority
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status
        
    def __repr__(self):
        return f"{self.description} - id: {self.id}\n\tPriority: {self.priority}\n\tDuration:{self.duration}\n\tDepends on: {self.dependencies}\n\tStatus: {self.status}"

    def __lt__(self, other):
        return self.id < other.id   
    
class TaskScheduler:
    """
    A simple daily task scheduler using priority queues
    Input:
    - tasks: a list of tasks to be sorted by their priorities 
    Output: 
    - a list of sorted taks 
    """
    # status 
    NOT_STARTED ='N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    # initialization
    def __init__(self, tasks):
        self.tasks = tasks
            
    def remove_dependency(self, task_id):
        """
        Removes a task from the task list
        Input: list of taks and task_id of the task just completed
        Output: lists of tasks with t_id removed
        """
        for t in self.tasks:
            if t.id != task_id and task_id in t.dependencies:
                t.dependencies.remove(task_id)           
         
    
    def check_unscheduled_tasks(self):
        """
        Checks wheather the task is scheduled
        Input: list of tasks 
        Output: boolean (checks the status of all tasks and returns True if at least one task has status = 'N'
        """
        for task in tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        """
        Formats time
        Input: list of tasks and time
        Output: time written in from hours and minutes
        """
        return f"{time//60}h{time%60:02d}"
            
        
    def run_task_scheduler(self, starting_time = 480):
        """
        Runs task scheduler 
        Input: list of tasks and starting time of first task of the day
        Output: task schedule
        """
        # assign starting_time to current_time
        current_time = starting_time
        
        # create two heaps one to create a priority queue and second to store indices of items in the priority queue
        priority_queue = MinHeap(20)
        priority_queue_indices = MinHeap(20)
        
        # create a list to store indices of unsorted tasks
        indices = []
        
        # push task priorities to two heaps 
        for i in self.tasks:
            priority_queue.insert(i.priority)
            priority_queue_indices.insert(i.priority)
        
        # min heapify two heaps 
        priority_queue.minHeap()
        priority_queue_indices.minHeap()
        
        # append the task's id based on their order in the priority queue
        while len(indices) < priority_queue.size:
            for i in self.tasks:
                priority_index = priority_queue_indices.remove()
                if i.priority == priority_index:
                    indices.append(i.id)
                else:
                    priority_queue_indices.insert(priority_index)
        
        # start from the first element in the list
        i = 0
        
        # run the function below while prioritu_queue has an unscheduled task
        while priority_queue.size != 0:
            
            # assign the indices of tasks in the priority_queue
            index = indices[i]
            
            # pop the root of the priority_queue heap and store it in task
            task = priority_queue.remove()
            
            print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {self.tasks[index].id} that takes {self.tasks[index].duration} mins")
            current_time += self.tasks[index].duration           
            print(f"✅ Completed Task {self.tasks[index].id} with priority {self.tasks[index].priority} - '{self.tasks[index].description}' at time {self.format_time(current_time)}\n") 
            
            # remove the completed task from the dependency list
            self.remove_dependency(self.tasks[index].id)
            
            # change the task status
            self.tasks[index].status = self.COMPLETED
            
            # increment i by 1 to move to the next task in priority_queue
            i = i + 1
            
        total_time = current_time - starting_time             
        print(f"🏁 Completed all planned tasks in {total_time//60}h{total_time%60:02d}min")


# In[ ]:


tasks = [
    Task(0, 7, 'Complete readings', 40, []), 
    Task(1, 8, 'Answer study guide questions', 20, [0]), 
    Task(2, 9, 'Do pre-class work', 30, [0, 1]), 
    Task(3, 13, 'Buy noodles and tofu', 40, []), 
    Task(4, 13, 'Cook raw noodles and tofu', 15, [3]), 
    Task(5, 13, 'Add noodles to fried tofu', 20, [3, 4]), 
    Task(6, 4, 'Find a gift store', 10, []), 
    Task(7, 5, 'Choose a gift', 20, [6]), 
    Task(8, 6, 'Pay for the item', 5, [6, 7]), 
    Task(9, 1, 'Find a cafe to study', 10, []), 
    Task(10, 2, 'Put my technology into the bag', 5, [9]), 
    Task(11, 3, 'Take a bus to a cafe', 10, [9, 10]),
    Task(12, 10, 'Message my friend', 5, []), 
    Task(13, 11, 'Charge my phone', 5, []), 
    Task(14, 12, 'Save the location of the village', 5, [])]


task_scheduler = TaskScheduler(tasks)
task_scheduler.run_task_scheduler(starting_time=480)


# ### In addition to the actual scheduler, provide at least one simple example to demonstrate how your scheduler prioritizes tasks based on their priority value.

# In[ ]:


#import sys module to acess variables used or maintained by the interpreter
import sys

class MinHeap:
    """
    A class with methods to create a min heap, push a new element and pop the root
    Input: maximum size of the heap 
    """
    # initialization
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0]*(self.maxsize + 1)
        self.Heap[0] = -1 * sys.maxsize
        self.FRONT = 1
 
    def parent(self, pos):
        """
        Input: position of the node
        Output: the position of parent at pos
        """
        return pos // 2
 
    def leftChild(self, pos):
        """
        Input: position of the node
        Output: position of the left child
        """       
        return 2 * pos
 
    def rightChild(self, pos):
        """
        Input: position of the node
        Output: position of the right child
        """   
        return (2 * pos) + 1
 
    def isLeaf(self, pos):
        """
        Input: position of the node
        Output: returns true if the passed node is a leaf node
        """   
        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False
 
    def swap(self, fpos, spos):
        """
        Swaps two nodes
        Input: position of two node
        """ 
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    def minHeapify(self, pos):
        """
        A function that heapifies the node at pos
        Input: position of the node
        """ 
        # compare a non-leaf node and its child
        if not self.isLeaf(pos):
            if (self.Heap[pos] > self.Heap[self.leftChild(pos)] or
               self.Heap[pos] > self.Heap[self.rightChild(pos)]):
 
                # swap the node with the left child and heapify the left child
                if self.Heap[self.leftChild(pos)] < self.Heap[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
 
                # swap the node with the right child and heapify the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    def insert(self, element):
        """
        A function that inserts an element into the heap
        Input: position of the node
        """ 
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.Heap[self.size] = element
 
        current = self.size
 
        while self.Heap[current] < self.Heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
  
    def minHeap(self):
        """
        A function that builds the min heap
        """ 
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    def remove(self):
        """
        A function that removes and pops the root element
        Output: the root of the heap
        """ 
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped


# In[ ]:


class Task:
    """
    A class that stores the input which is referred in TaskScheduler
    Input:
    - id: a unique task identifier (that can be referenced by other tasks)  
    - priority: priority level of a task  
    - description: a short description of the task
    - duration: duration in minutes  
    - dependencies: list of id’s indicating whether the current task cannot begin until all of its dependencies have been completed
    - status: the state of a task; possible values are not_yet_started, in_progress, or completed.      
    """
    # initializes an instance of Task
    def __init__(self,task_id,priority,description,duration,dependencies,status="N"):
        self.id = task_id
        self.priority = priority
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status
        
    def __repr__(self):
        return f"{self.description} - id: {self.id}\n\tPriority: {self.priority}\n\tDuration:{self.duration}\n\tDepends on: {self.dependencies}\n\tStatus: {self.status}"

    def __lt__(self, other):
        return self.id < other.id   
    
class TaskScheduler:
    """
    A simple daily task scheduler using priority queues
    Input:
    - tasks: a list of tasks to be sorted by their priorities 
    Output: 
    - a list of sorted taks 
    """
    # status 
    NOT_STARTED ='N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    # initialization
    def __init__(self, tasks):
        self.tasks = tasks
            
    def remove_dependency(self, task_id):
        """
        Removes a task from the task list
        Input: list of taks and task_id of the task just completed
        Output: lists of tasks with t_id removed
        """
        for t in self.tasks:
            if t.id != task_id and task_id in t.dependencies:
                t.dependencies.remove(task_id)           
         
    
    def check_unscheduled_tasks(self):
        """
        Checks wheather the task is scheduled
        Input: list of tasks 
        Output: boolean (checks the status of all tasks and returns True if at least one task has status = 'N'
        """
        for task in tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        """
        Formats time
        Input: list of tasks and time
        Output: time written in from hours and minutes
        """
        return f"{time//60}h{time%60:02d}"
            
        
    def run_task_scheduler(self, starting_time = 480):
        """
        Runs task scheduler 
        Input: list of tasks and starting time of first task of the day
        Output: task schedule
        """
        # assign starting_time to current_time
        current_time = starting_time
        
        # create two heaps one to create a priority queue and second to store indices of items in the priority queue
        priority_queue = MinHeap(5)
        priority_queue_indices = MinHeap(5)
        
        # create a list to store indices of unsorted tasks
        indices = []
        
        # push task priorities to two heaps 
        for i in self.tasks:
            priority_queue.insert(i.priority)
            priority_queue_indices.insert(i.priority)
        
        # min heapify two heaps 
        priority_queue.minHeap()
        priority_queue_indices.minHeap()
        
        
        
        # append the task's id based on their order in the priority queue
        while len(indices) < priority_queue.size:
            for i in self.tasks:
                priority_index = priority_queue_indices.remove()
                if i.priority == priority_index:
                    indices.append(i.id)
                else:
                    priority_queue_indices.insert(priority_index)
        
        # start from the first element in the list
        i = 0
        
        # run the function below while prioritu_queue has an unscheduled task
        while priority_queue.size != 0:
            
            # assign the indices of tasks in the priority_queue
            index = indices[i]
            
            # pop the root of the priority_queue heap and store it in task
            task = priority_queue.remove()
            
            print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {self.tasks[index].id} that takes {self.tasks[index].duration} mins")
            current_time += self.tasks[index].duration           
            print(f"✅ Completed Task {self.tasks[index].id} with priority {self.tasks[index].priority} - '{self.tasks[index].description}' at time {self.format_time(current_time)}\n") 
            
            # remove the completed task from the dependency list
            self.remove_dependency(self.tasks[index].id)
            
            # change the task status
            self.tasks[index].status = self.COMPLETED
            
            # increment i by 1 to move to the next task in priority_queue
            i = i + 1
            
        total_time = current_time - starting_time             
        print(f"🏁 Completed all planned tasks in {total_time//60}h{total_time%60:02d}min")


# In[ ]:


tasks = [
    Task(0, 4, 'Read Sapiens', 30, []), 
    Task(1, 3, 'Do yoga', 30, []), 
    Task(2, 1, 'Schedule a doctor appointment', 5, []), 
    Task(3, 2, 'Hug my roommate', 3, [])]

task_scheduler = TaskScheduler(tasks)
task_scheduler.run_task_scheduler(starting_time=480)


# ### Write an activity priority scheduler with multi-tasking capability in Python, which receives as input a list of tasks and reports (outputs) a schedule for you to follow.

# In[ ]:


#import sys module to acess variables used or maintained by the interpreter
import sys

class MinHeap:
    """
    A class with methods to create a min heap, push a new element and pop the root
    Input: maximum size of the heap 
    """
    # initialization
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0]*(self.maxsize + 1)
        self.Heap[0] = -1 * sys.maxsize
        self.FRONT = 1
 
    def parent(self, pos):
        """
        Input: position of the node
        Output: the position of parent at pos
        """
        return pos // 2
 
    def leftChild(self, pos):
        """
        Input: position of the node
        Output: position of the left child
        """       
        return 2 * pos
 
    def rightChild(self, pos):
        """
        Input: position of the node
        Output: position of the right child
        """   
        return (2 * pos) + 1
 
    def isLeaf(self, pos):
        """
        Input: position of the node
        Output: returns true if the passed node is a leaf node
        """   
        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False
 
    def swap(self, fpos, spos):
        """
        Swaps two nodes
        Input: position of two node
        """ 
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    def minHeapify(self, pos):
        """
        A function that heapifies the node at pos
        Input: position of the node
        """ 
        # compare a non-leaf node and its child
        if not self.isLeaf(pos):
            if (self.Heap[pos] > self.Heap[self.leftChild(pos)] or
               self.Heap[pos] > self.Heap[self.rightChild(pos)]):
 
                # swap the node with the left child and heapify the left child
                if self.Heap[self.leftChild(pos)] < self.Heap[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
 
                # swap the node with the right child and heapify the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    def insert(self, element):
        """
        A function that inserts an element into the heap
        Input: position of the node
        """ 
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.Heap[self.size] = element
 
        current = self.size
 
        while self.Heap[current] < self.Heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
  
    def minHeap(self):
        """
        A function that builds the min heap
        """ 
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    def remove(self):
        """
        A function that removes and pops the root element
        Output: the root of the heap
        """ 
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped


# In[ ]:


class Task:
    """
    A class that stores the input which is referred in TaskScheduler
    Input:
    - id: a unique task identifier (that can be referenced by other tasks)  
    - priority: priority level of a task  
    - description: a short description of the task
    - duration: duration in minutes  
    - dependencies: list of id’s indicating whether the current task cannot begin until all of its dependencies have been completed
    - multitask: Indices of tasks that can be done together with the task
    - status: the state of a task; possible values are not_yet_started, in_progress, or completed.      
    """
    # initializes an instance of Task
    def __init__(self,task_id,priority,description,duration,dependencies,multitask,status="N"):
        self.id = task_id
        self.priority = priority
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.multitask = multitask
        self.status = status
        
    def __repr__(self):
        return f"{self.description} - id: {self.id}\n\tPriority: {self.priority}\n\tDuration:{self.duration}\n\tDepends on: {self.dependencies}\n\tMultitask: {self.multitask}\n\tStatus: {self.status}"

    def __lt__(self, other):
        return self.id < other.id   
    
class TaskScheduler:
    """
    A simple daily task scheduler using priority queues
    Input:
    - tasks: a list of tasks to be sorted by their priorities 
    Output: 
    - a list of sorted taks 
    """
    # status 
    NOT_STARTED ='N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    # initialization
    def __init__(self, tasks):
        self.tasks = tasks
            
    def remove_dependency(self, task_id):
        """
        Removes a task from the task list
        Input: list of taks and task_id of the task just completed
        Output: lists of tasks with t_id removed
        """
        for t in self.tasks:
            if t.id != task_id and task_id in t.dependencies:
                t.dependencies.remove(task_id)           
         
    
    def check_unscheduled_tasks(self):
        """
        Checks wheather the task is scheduled
        Input: list of tasks 
        Output: boolean (checks the status of all tasks and returns True if at least one task has status = 'N'
        """
        for task in tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        """
        Formats time
        Input: list of tasks and time
        Output: time written in from hours and minutes
        """
        return f"{time//60}h{time%60:02d}"
            
        
    def run_task_scheduler(self, starting_time = 480):
        """
        Runs task scheduler 
        Input: list of tasks and starting time of first task of the day
        Output: task schedule
        """
        # assign starting_time to current_time
        current_time = starting_time
        
        # create two heaps one to create a priority queue and second to store indices of items in the priority queue
        priority_queue = MinHeap(5)
        priority_queue_indices = MinHeap(5)
        
        # create a list to store indices of unsorted tasks
        indices = []
        
        # push task priorities to two heaps 
        for i in self.tasks:
            priority_queue.insert(i.priority)
            priority_queue_indices.insert(i.priority)
        
        # min heapify two heaps 
        priority_queue.minHeap()
        priority_queue_indices.minHeap()
        
        
        
        # append the task's id based on their order in the priority queue
        while len(indices) < priority_queue.size:
            for i in self.tasks:
                priority_index = priority_queue_indices.remove()
                if i.priority == priority_index:
                    indices.append(i.id)
                else:
                    priority_queue_indices.insert(priority_index)
        
        sorted_tasks = []
        for i in indices:
            sorted_tasks.append(self.tasks[i])
            
        forloop = []
        for i in indices:
            forloop.append(self.tasks[i])
            
        # start from the first element in the list
        i = 0
        
        for i in indices:

            print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {sorted_tasks[i].id} that takes {sorted_tasks[i].duration} mins")
            print(f"✅ Completed Task {sorted_tasks[i].id} with priority {sorted_tasks[i].priority} - '{sorted_tasks[i].description}' at time {self.format_time(current_time)}\n") 
            
            indices.remove(i)
            
            for j in sorted_tasks[i]:
                #print(j)
                if len(sorted_tasks[j].dependencies) == 0:
                    print(f"✅ Completed Task {sorted_tasks[j].id} with priority {sorted_tasks[j].priority} - '{sorted_tasks[j].description}' at time {self.format_time(current_time)}\n") 
                    if sorted_tasks[j] in forloop:
                        forloop.remove(sorted_tasks[j])
            
        total_time = current_time - starting_time             
        print(f"🏁 Completed all planned tasks in {total_time//60}h{total_time%60:02d}min")


# In[ ]:


tasks = [
    Task(0, 7, 'Complete readings', 40, [9], []), 
    Task(1, 8, 'Answer study guide questions', 20, [0], []), 
    Task(2, 9, 'Do pre-class work', 30, [0, 1, 9], []), 
    Task(3, 13, 'Buy noodles and tofu', 40, [], []), 
    Task(4, 13, 'Cook raw noodles and tofu', 15, [3], [9, 10, 12, 13, 14]), 
    Task(5, 13, 'Add noodles to fried tofu', 20, [3, 4], []), 
    Task(6, 4, 'Find a gift store', 10, [], []), 
    Task(7, 5, 'Choose a gift', 20, [6], [12, 14, 1]), 
    Task(8, 6, 'Pay for the item', 5, [6], []), 
    Task(9, 1, 'Find a cafe to study', 10, [], []), 
    Task(10, 2, 'Put my technology into the bag', 5, [9], []), 
    Task(11, 3, 'Take a bus to a cafe', 10, [9, 2, 10], [4, 9, 12, 14]),
    Task(12, 10, 'Message my friend', 5, [9], []), 
    Task(13, 11, 'Charge my phone', 5, [9], []), 
    Task(14, 12, 'Save the location of the village', 5, [], [])]

task_scheduler = TaskScheduler(tasks)
task_scheduler.run_task_scheduler(starting_time=480)

