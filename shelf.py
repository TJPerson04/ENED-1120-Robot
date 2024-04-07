class Shelf:
    def __init__(self, name, start) -> None:
        self.name = name  # Ex: "A1"
        self.start = start  # Ex: [12, 12]

        BOX_OFFSETS = [
            [3, 0],
            [9, 0],
            [15, 0],
            [21, 0],
            [27, 0],
            [33, 0],
            [3, 12],
            [9, 12],
            [15, 12],
            [21, 12],
            [27, 12],
            [33, 12]
        ]
        self.boxLocations = []
        for i in range(len(BOX_OFFSETS)):
            x = start[0] + BOX_OFFSETS[i][0]
            y = start[1] + BOX_OFFSETS[i][1]

            self.boxLocations.append([x, y])