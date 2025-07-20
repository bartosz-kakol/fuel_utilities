from base import Display


class DisplayMockImpl(Display):
    def init(self, **properties):
        print("Mock display init()")

    def post_init(self):
        print("Mock display post_init()")

    def show(self, data: dict):
        print(data)


export = DisplayMockImpl
