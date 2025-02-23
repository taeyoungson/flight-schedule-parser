import jobs  # noqa: F401

from scheduler import instance


def main():
    sdler = instance.DefaultBlockingScheduler
    sdler.start()


if __name__ == "__main__":
    main()
