from dataclasses import dataclass, field


@dataclass
class Gems:
    white: int
    blue: int
    green: int
    red: int
    black: int
    yellow: int

    def __add__(self, other: "Gems") -> "Gems":
        return Gems(
            self.white + other.white,
            self.blue + other.blue,
            self.green + other.green,
            self.red + other.red,
            self.black + other.black,
            self.yellow + other.yellow,
        )

    def __sub__(self, other: "Gems") -> "Gems":
        return Gems(
            self.white - other.white,
            self.blue - other.blue,
            self.green - other.green,
            self.red - other.red,
            self.black - other.black,
            self.yellow - other.yellow,
        )

    def __ge__(self, other: "Gems") -> bool:
        return all(self.__dict__[c] >= other.__dict__[c] for c in ["white", "blue", "green", "red", "black", "yellow"])

    def __gt__(self, other: "Gems") -> bool:
        return (
            self >= other and
            any(self.__dict__[c] > other.__dict__[c] for c in ["white", "blue", "green", "red", "black", "yellow"])
        )

    def __le__(self, other: "Gems") -> bool:
        return all(self.__dict__[c] <= other.__dict__[c] for c in ["white", "blue", "green", "red", "black", "yellow"])

    def __lt__(self, other: "Gems") -> bool:
        return (
            self <= other and
            any(self.__dict__[c] < other.__dict__[c] for c in ["white", "blue", "green", "red", "black", "yellow"])
        )

    def __len__(self) -> int:
        return sum(self.__dict__.values())


@dataclass
class Card:
    level: int
    points: int
    generation: Gems
    cost: Gems


@dataclass
class Noble:
    points: int
    requirements: Gems


@dataclass
class Player:
    gems: Gems = field(default_factory=lambda: Gems(0, 0, 0, 0, 0, 0))
    generation: Gems = field(default_factory=lambda: Gems(0, 0, 0, 0, 0, 0))
    hand: list[Card] = field(default_factory=list)
    reserved_cards: list[Card] = field(default_factory=list)
    purchased_cards: list[Card] = field(default_factory=list)
    nobles: list[Noble] = field(default_factory=list)
    points: int = 0

    def check_consistency(self) -> None:
        assert self.generation == sum([card.generation for card in self.purchased_cards], start=Gems(0, 0, 0, 0, 0, 0))
        assert self.points == (
            sum([card.points for card in self.purchased_cards]) +
            sum([noble.points for noble in self.nobles])
        )


@dataclass
class GameState:
    players: list[Player]
    decks_by_level: list[list[Card]]
    revealed_cards_by_level: list[list[Card]]
    nobles: list[Noble]
    gem_pool: Gems
    first_player_n: int
    current_player_n: int
    round: int
    last_round: bool

    def check_consistency(self) -> None:
        # total number of gems
        total_gems = self.gem_pool + sum(
            [player.gems for player in self.players],
            start=Gems(0, 0, 0, 0, 0, 0),
        )
        n_gems = (
            4 if len(self.players) == 2
            else 5 if len(self.players) == 3
            else 7
        )
        expected_gems = Gems(n_gems, n_gems, n_gems, n_gems, n_gems, 5)
        assert total_gems == expected_gems, f"Gems discrepancy - Expected {expected_gems}, got {total_gems}."
        # points and gem generation for each player
        for player in self.players:
            player.check_consistency()
        # total number of cards by level
        field_cards = [
            len(deck) + len(revealed)
            for deck, revealed in zip(self.decks_by_level, self.revealed_cards_by_level)
        ]
        player_cards = [
            len([
                card
                for player in self.players
                for card in player.hand + player.reserved_cards + player.purchased_cards
                if card.level == level
            ])
            for level in [1, 2, 3]
        ]
        total_cards = [a + b for a, b in zip(field_cards, player_cards)]
        expected_cards = [40, 30, 20]
        assert total_cards == expected_cards, f"Cards discrepancy - Expected {expected_cards}, got {total_cards}."
