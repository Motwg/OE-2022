from app.SO import SO


class CSO(SO):

    def __init__(self, population, dimension, opt_function, **kwargs):
        super().__init__(population, dimension, opt_function)
        # TODO: (AL) add needed definitions

        self.reset()

    def reset(self):
        super().reset()
        # TODO: (AL) add needed things to reset after finding solution

    def step(self) -> float:
        # TODO: (AL) add implementation
        return self.y

    def evaluate(self, iterations: int = None, *args, **kwargs):
        return super().evaluate(self.step, iterations)
