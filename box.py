# Represents a box to be picked up

class Box:
    def __init__(self, boxType: int, location: str) -> None:
        self.POSSIBLE_BARCODES = [
            [[3, 'W'], [1, 'B']], 
            [[1, 'W'], [1, 'B'], [1, 'W'], [1, 'B']], 
            [[2, 'W'], [2, 'B']],
            [[1, 'B'], [2, 'W'], [1, 'B']]
            ]

        self.boxType = boxType
        self.barcode = self.POSSIBLE_BARCODES[boxType - 1]
        self.location = location