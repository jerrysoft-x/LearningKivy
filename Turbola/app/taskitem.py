import json
from datetime import datetime


class TaskItem(object):
    def __init__(self, name, index=0, status='open', createddate=datetime.now(), updateddate=datetime.now()):
        self.name = name
        self.index = index
        self.status = status
        self.createddate = createddate
        self.updateddate = updateddate

    @classmethod
    def taskitem2dict(cls, taskitem):
        return {
            'name': taskitem.name,
            'index': taskitem.index,
            'status': taskitem.status,
            'createddate': taskitem.createddate.strftime('%Y-%m-%d %H:%M:%S'),
            'updateddate': taskitem.updateddate.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def dict2taskitem(cls, dict):
        return TaskItem(dict['name'], dict['index'], dict['status'],
                        datetime.strptime(dict['createddate'], '%Y-%m-%d %H:%M:%S'),
                        datetime.strptime(dict['updateddate'], '%Y-%m-%d %H:%M:%S'))


# t = TaskItem('hello')
# print(json.dumps(t, default=TaskItem.taskitem2dict))

d = r'{"name": "hello", "index": 8, "status": "open", "createddate": "2017-06-14 17:43:28", "updateddate": "2017-06-14 17:43:28"}'
print(json.loads(d, object_hook=TaskItem.dict2taskitem).__dict__)
print(datetime.now())

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
