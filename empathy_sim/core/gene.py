from dataclasses import dataclass
import random as rnd


@dataclass
class Gene:
    empathy: bool
    help_amount: int
    help_threshold: int
    min_energy_to_have: int

    mutation_rate: float = 0.02

    @classmethod
    def crossover(cls, g1: "Gene", g2: "Gene") -> "Gene":
        child_gene = cls(
            empathy=rnd.choice([g1.empathy, g2.empathy]),
            help_amount=rnd.choice([g1.help_amount, g2.help_amount]),
            min_energy_to_have=rnd.choice(
                [g1.min_energy_to_have, g2.min_energy_to_have]
            ),
            help_threshold=rnd.choice([g1.help_threshold, g2.help_threshold]),
        )
        child_gene.mutate()
        return child_gene

    def mutate(self) -> None:
        if rnd.random() < self.mutation_rate:
            self.empathy = not self.empathy

        if rnd.random() < self.mutation_rate:
            self.help_amount = rnd.choice([1, 2, 3, 4])

        if rnd.random() < self.mutation_rate:
            self.help_threshold = rnd.choice([2, 4, 6, 8])

        if rnd.random() < self.mutation_rate:
            self.min_energy_to_have = rnd.choice([12, 14, 16, 18])
