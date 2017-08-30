import json
from datetime import datetime


class TaskManager(object):
    def __init__(self):
        self.taskQueues = {}

    def addTaskQueue(self, queueName, task_list):
        if queueName in self.taskQueues:
            raise ValueError('Task queue name is already defined.')
        else:
            self.taskQueues[queueName] = task_list

    def removeTaskQueue(self, queueName):
        if queueName in self.taskQueues:
            del self.taskQueues[queueName]
        else:
            raise ValueError('This task queue name is not existing')

    def getTaskQueue(self, queueName, task_list):
        if queueName in self.taskQueues:
            return self.taskQueues[queueName]
        else:
            raise ValueError('This task queue name is not existing')

    def setTaskQueue(self, queueName, task_list):
        if queueName in self.taskQueues:
            self.taskQueues[queueName] = task_list
        else:
            raise ValueError('This task queue name is not existing')


class TaskList(object):
    def __init__(self, bindingFile, taskList={}):
        self.bindingFile = bindingFile
        self.taskList = taskList

    def setBindingFile(self, bindingFile):
        self.bindingFile = bindingFile

    def getBindingFile(self):
        return self.bindingFile

    def loadFromFile(self):
        with open(self.bindingFile, mode='r', encoding='utf-8') as f:
            for task in f.readlines():
                taskitem = json.loads(task, object_hook=TaskItem.dict2taskitem)
                self.taskList[taskitem.rowid] = taskitem

    def flushToFile(self):
        with open(self.bindingFile, mode='w', encoding='utf-8') as f:
            for rowid in self.taskList:
                json.dump(self.taskList[rowid], f, default=TaskItem.taskitem2dict)
                f.write('\n')

    def generateRowID(self):
        rowIdIndex = 1
        strNow = datetime.now().strftime('%Y%m%d%H%M%S')
        while (strNow + self.getStrIndex(rowIdIndex)) in self.taskList:
            rowIdIndex += 1
        return strNow + self.getStrIndex(rowIdIndex)

    def getStrIndex(self, index):
        strIndex = str(index)
        if strIndex.__len__() == 1:
            strIndex = '0' + strIndex
        return strIndex


class TaskItem(object):
    def __init__(self, rowid, name, index=0, status='open', createddate=datetime.now(), updateddate=datetime.now()):
        self.rowid = rowid
        self.name = name
        self.index = index
        self.status = status
        self.createddate = createddate
        self.updateddate = updateddate

    @classmethod
    def taskitem2dict(cls, taskitem):
        return {
            'rowid': taskitem.rowid,
            'name': taskitem.name,
            'index': taskitem.index,
            'status': taskitem.status,
            'createddate': taskitem.createddate.strftime('%Y-%m-%d %H:%M:%S'),
            'updateddate': taskitem.updateddate.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def dict2taskitem(cls, dict):
        return TaskItem(dict['rowid'], dict['name'], dict['index'], dict['status'],
                        datetime.strptime(dict['createddate'], '%Y-%m-%d %H:%M:%S'),
                        datetime.strptime(dict['updateddate'], '%Y-%m-%d %H:%M:%S'))

# t = TaskItem('hello')
# print(json.dumps(t, default=TaskItem.taskitem2dict))

# d = r'{"name": "hello", "index": 8, "status": "open", "createddate": "2017-06-14 17:43:28", "updateddate": "2017-06-14 17:43:28"}'
# print(json.loads(d, object_hook=TaskItem.dict2taskitem).__dict__)
# print(datetime.now())

# t1 = TaskItem('task1')
# t2 = TaskItem('task2')
# t3 = TaskItem('task3')
#
# with open(r'tasklist.json', 'a') as f:
#     json.dump(t1, f, default=TaskItem.taskitem2dict)
#     f.write('\n')
#     json.dump(t2, f, default=TaskItem.taskitem2dict)
#     f.write('\n')
#     json.dump(t3, f, default=TaskItem.taskitem2dict)
#     f.write('\n')
