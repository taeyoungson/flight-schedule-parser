from apscheduler.jobstores import memory

JOBSTORES = {"default": memory.MemoryJobStore()}

EXECUTORS = {"default": {"type": "threadpool", "max_workers": 20}}

SCHEDULER_ARGS = {
    "coalesce": False,
    "max_instances": 1,
}


def get_jobstores():
    return JOBSTORES


def get_executor():
    return EXECUTORS


def get_scheduler_args():
    return SCHEDULER_ARGS
