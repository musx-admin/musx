class Part():
    def __init__(self, measures=[]):
        self.measures = []
        for m in measures:
            self.add_measure(m)

    def __iter__(self):     
        return iter(self.measures)

    def __str__(self):
        text = self.id
        return f'<Part: {text}>' #  {hex(id(self))}

    __repr__ = __str__ 

    def add_measure(self, measure):
        measure.part = self  # back link from measure to its part
        self.measures.append(measure)
