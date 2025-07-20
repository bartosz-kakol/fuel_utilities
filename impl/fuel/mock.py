from base import Fuel


class FuelMockImpl(Fuel):
    def init(self, **properties):
        print("Mock fuel init()")

    def post_init(self):
        print("Mock fuel post_init()")

    def read(self) -> dict:
        return {"test": 123}


export = FuelMockImpl
