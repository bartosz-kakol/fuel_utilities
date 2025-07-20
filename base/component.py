class Component:
    @staticmethod
    def get_component_name():
        raise NotImplementedError

    def init(self, **properties):
        raise NotImplementedError("The init() method has not been implemented.")

    def post_init(self):
        pass
