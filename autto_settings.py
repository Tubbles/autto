#!/usr/bin/env python3

from datetime import datetime, timedelta


class AuttoFile:
    keywords = ""
    available_on = datetime.utcnow()


class AuttoSequence:
    files = []

    def add_file(self, keywords, available_on):
        file = AuttoFile()
        file.keywords = keywords
        if type(available_on) == datetime:
            file.available_on = available_on
        elif type(available_on) == timedelta:
            file.available_on = self.files[-1].available_on + available_on
        else:
            raise TypeError
        self.files.append(file)

    def fetch(self):
        pass


# autto = object()

# autto.sequences = [
#     {
#         "asd": "asd"
#     }
# ]


def main():
    # sequence = AuttoSequence()
    # sequence.add_file("test", datetime.utcnow())
    # print([(x.keywords, str(x.available_on)) for x in sequence.files])
    # delta = timedelta(days=7)
    # sequence.add_file("test2", delta)
    # print([(x.keywords, str(x.available_on)) for x in sequence.files])
    # sequence.add_file("test3", 1)
    # print([(x.keywords, str(x.available_on)) for x in sequence.files])

    sequence = AuttoSequence()
    sequence.add_file("test", datetime.utcnow())
    sequence.fetch()


if __name__ == "__main__":
    main()
