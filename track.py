from shelf import Shelf

class Track:
    def __init__(self) -> None:
        SHELVES = [
            ["A1", [12, 12]],
            ["A2", [12, 36]],
            ["C1", [12, 60]],
            ["C2", [12, 84]],
            ["B1", [60, 12]],
            ["B2", [60, 36]],
            ["D1", [60, 60]],
            ["D2", [60, 84]]
        ]
        self.BOX_COORDS = {}
        for shelf in SHELVES:
            s = Shelf(shelf[0], shelf[1])
            for i in range(len(s.boxLocations)):
                self.BOX_COORDS[s.name + "_" + str(i + 1)] = s.boxLocations[i]