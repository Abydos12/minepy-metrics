from enum import Enum, auto


class Damage(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    DEALT = auto()
    DEALT_ABSORBED = auto()


if __name__ == "__main__":
    x = Damage("dealt")
    z = Damage
    print()
