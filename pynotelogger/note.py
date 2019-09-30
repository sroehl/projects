import datetime
import uuid


class Note:

    def print(self):
        if self.update_date is not None:
            print("{}".format(self.update_date))
        else:
            print("{}".format(self.date))
        print("{}".format(self.text))
        print("{} in {}".format(self.title, self.group))
        print(",".join(self.tags))

    def update(self, text=None, title=None, group=None, tags=None):
        if text is not None:
            self.text += text
        if title is not None:
            self.title = title
        if group is not None:
            self.group = group
        if tags is not None:
            self.tags = tags
        self.update_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def save(self):
        return {
            'id': self.id,
            'title': self.title,
            'group': self.group,
            'tags': self.tags,
            'text': self.text,
            'date': self.date,
            'update': self.update_date
        }

    def __init__(self, text, title, group, tags):
        self.id = str(uuid.uuid4())
        self.date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.update_date = None
        self.text = text
        self.title = title
        self.group = group
        self.tags = tags
