from app.SO import SO


class LCSO(SO):

    def __init__(self, population, dimension, opt_function, **kwargs):
        super().__init__(population, dimension, opt_function)
        # TODO: add needed definitions

        self.reset()

    def reset(self):
        super().reset()
        # TODO: add needed things to reset after finding solution

    def step(self) -> float:
        # TODO: add implementation
        return self.y

    def evaluate(self, iterations: int = None, *args, **kwargs):
        return super().evaluate(self.step, iterations)
