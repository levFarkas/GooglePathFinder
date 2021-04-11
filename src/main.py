from backend.services.distance_service import DistanceService


class Handler:
    def __init__(self):
        self._distance_service = DistanceService()

    # Main function
    def handle(self, config=None):
        pass


if __name__ == '__main__':
    handler = Handler()
    handler.handle()
