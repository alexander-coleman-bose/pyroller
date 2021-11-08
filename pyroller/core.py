#!/usr/bin/env python
"""pyroller"""

import random
import re
from typing import List, Tuple  # Python 3.8
import numpy as np

# Set class defaults here
DEFAULT_NUM_SIMULATIONS = 100
MAX_EXPLOSIONS = 100
MAX_REROLLS = 100


class KeepDropTag:
    """Tag that has high/low like keeps and drops"""

    def __init__(self, high: int = 0, low: int = 0):
        self.high = high
        self.low = low

    def __bool__(self) -> bool:
        return self.high > 0 or self.low > 0

    def __repr__(self) -> str:
        string_out = f"{self.__class__.__name__}"
        if self:
            attr_strings = [
                f"{key}={value}"
                for key, value in zip(self.__dict__.keys(), self.__dict__.values())
                if value > 0
            ]
            string_out = string_out + "(" + ", ".join(attr_strings) + ")"
        return string_out


class DropTag(KeepDropTag):
    """Tag for dropping highest/lowest dice"""


class KeepTag(KeepDropTag):
    """Tag for keeping highest/lowest dice"""


class RerollExplodeTag:
    """Tag that has once/over/under/value like rerolls and explode"""

    def __init__(
        self,
        once: bool = False,
        over: int = 0,
        under: int = 0,
        value: int = 0,
        num_faces: int = 0,
    ):
        self.once = once
        self.over = over
        self.under = under
        self.value = value
        # HACK: We need num_faces for reroll.over, but now we are dependent?
        self.num_faces = num_faces

    def __bool__(self) -> bool:
        return self.over < self.num_faces or self.under > 0 or self.value > 0

    def __repr__(self) -> str:
        string_out = f"{self.__class__.__name__}"
        if self:
            attr_strings = [
                f"{key}={value}"
                for key, value in zip(self.__dict__.keys(), self.__dict__.values())
                if not isinstance(key, bool) and value > 0
            ]
            string_out = (
                string_out + f"(once={self.once}, " + ", ".join(attr_strings) + ")"
            )
        return string_out


class RerollTag(RerollExplodeTag):
    """Tag for rerolling dice after the initial roll"""


class ExplodeTag(RerollExplodeTag):
    """Tag for rolling additional dice after the initial roll, i.e. "exploding dice\""""


class Roll:
    """Represents a given type of die roll

    Reference for parsing: https://foundryvtt.com/article/dice/
    """

    def __init__(self, roll_string: str):
        """Roll constructor from string"""

        # Attributes
        self.num_dice = None  # Nd...
        self.num_faces = None  # ...dN...
        self.multiplier = None
        self.roll_string = roll_string

        # Match to the pattern of [-]<num_dice>d<num_faces><tags>
        matches = re.match(
            r"^(?P<neg>-|)(?P<num_dice>\d+)d(?P<num_faces>\d+)(?P<tags>.*$)",
            roll_string,
        )

        # If we don't match the XdN pattern
        if matches is None:
            raise ValueError(
                f"Roll string ({roll_string}) must follow the pattern XdN..."
            )

        self.num_dice = int(matches.group("num_dice"))
        self.num_faces = int(matches.group("num_faces"))

        # HACK: this is used mostly to imply reductive or additive results
        if matches.group("neg"):
            self.multiplier = -1
        else:
            self.multiplier = 1

        # Tag Attributes
        self.drop = DropTag()
        self.keep = KeepTag()
        self.reroll = RerollTag(over=self.num_faces, num_faces=self.num_faces)
        self.explode = ExplodeTag(over=self.num_faces, num_faces=self.num_faces)

        # Split the tags
        for this_match in re.finditer(
            r"(?P<dh>dh)(?P<dh_val>\d*)|"
            + r"(?P<dl>dl|d)(?P<dl_val>\d*)|"
            + r"(?P<kl>kl)(?P<kl_val>\d*)|"
            + r"(?P<kh>kh|k)(?P<kh_val>\d*)|"
            + r"(?P<roo>ro>)(?P<roo_val>\d*)|"
            + r"(?P<rou>ro<)(?P<rou_val>\d*)|"
            + r"(?P<rov>ro)(?P<rov_val>\d*)|"
            + r"(?P<ro>r>)(?P<ro_val>\d*)|"
            + r"(?P<ru>r<)(?P<ru_val>\d*)|"
            + r"(?P<rv>r)(?P<rv_val>\d*)|"
            + r"(?P<xoo>xo>)(?P<xoo_val>\d*)|"
            + r"(?P<xou>xo<)(?P<xou_val>\d*)|"
            + r"(?P<xov>xo)(?P<xov_val>\d*)|"
            + r"(?P<xo>x>)(?P<xo_val>\d*)|"
            + r"(?P<xu>x<)(?P<xu_val>\d*)|"
            + r"(?P<xv>x)(?P<xv_val>\d*)",
            matches.group("tags"),
        ):
            if this_match.group("dh"):
                if this_match.group("dh_val"):
                    self.drop.high = int(this_match.group("dh_val"))
                else:
                    self.drop.high = 1
            elif this_match.group("dl"):
                if this_match.group("dl_val"):
                    self.drop.low = int(this_match.group("dl_val"))
                else:
                    self.drop.low = 1
            elif this_match.group("kl"):
                if this_match.group("kl_val"):
                    self.keep.low = int(this_match.group("kl_val"))
                else:
                    self.keep.low = 1
            elif this_match.group("kh"):
                if this_match.group("kh_val"):
                    self.keep.high = int(this_match.group("kh_val"))
                else:
                    self.keep.high = 1
            elif this_match.group("roo"):
                if this_match.group("roo_val"):
                    self.reroll.once = True
                    self.reroll.over = int(this_match.group("roo_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "reroll over (r>) without a reroll value (i.e. r>4)"
                    )
            elif this_match.group("rou"):
                if this_match.group("rou_val"):
                    self.reroll.once = True
                    self.reroll.under = int(this_match.group("rou_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "reroll under (r<) without a reroll value (i.e. r<6)"
                    )
            elif this_match.group("rov"):
                if this_match.group("rov_val"):
                    self.reroll.once = True
                    self.reroll.value = int(this_match.group("rov_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "reroll (r) without a reroll value (i.e. r1)"
                    )
            elif this_match.group("ro"):
                if this_match.group("ro_val"):
                    self.reroll.over = int(this_match.group("ro_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "reroll over (r>) without a reroll value (i.e. r>4)"
                    )
            elif this_match.group("ru"):
                if this_match.group("ru_val"):
                    self.reroll.under = int(this_match.group("ru_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "reroll under (r<) without a reroll value (i.e. r<6)"
                    )
            elif this_match.group("rv"):
                if this_match.group("rv_val"):
                    self.reroll.value = int(this_match.group("rv_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "reroll (r) without a reroll value (i.e. r1)"
                    )
            elif this_match.group("xoo"):
                if this_match.group("xoo_val"):
                    self.explode.once = True
                    self.explode.over = int(this_match.group("xoo_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "explode over (x>) or explode over once (xo>) "
                        + "without a threshold value (i.e. x>4, xo>4)"
                    )
            elif this_match.group("xou"):
                if this_match.group("xou_val"):
                    self.explode.once = True
                    self.explode.under = int(this_match.group("xou_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "explode under (x<) or explode once under (xo<) "
                        + "without a threshold value (i.e. x<6, xo<6)"
                    )
            elif this_match.group("xov"):
                if this_match.group("xov_val"):
                    self.explode.once = True
                    self.explode.value = int(this_match.group("xov_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "explode (x) or explode once (xo) without an "
                        + "explode value (i.e. x1, xo1)"
                    )
            elif this_match.group("xo"):
                if this_match.group("xo_val"):
                    self.explode.over = int(this_match.group("xo_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "explode over (x>) or explode over once (xo>) "
                        + "without a threshold value (i.e. x>4, xo>4)"
                    )
            elif this_match.group("xu"):
                if this_match.group("xu_val"):
                    self.explode.under = int(this_match.group("xu_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "explode under (x<) or explode once under (xo<) "
                        + "without a threshold value (i.e. x<6, xo<6)"
                    )
            elif this_match.group("xv"):
                if this_match.group("xv_val"):
                    self.explode.value = int(this_match.group("xv_val"))
                else:
                    raise ValueError(
                        f"Roll string ({roll_string}) cannot specify "
                        + "explode (x) or explode once (xo) without an "
                        + "explode value (i.e. x1, xo1)"
                    )

        # Check keep high/low
        if self.keep and self.drop:
            raise ValueError(
                f"Roll string ({roll_string}) cannot specify both a keep "
                + "high/low (kh, kl, k) option and a drop high/low "
                + "(dh, dl, d) option"
            )
        if self.keep.high > self.num_dice or self.keep.low > self.num_dice:
            raise ValueError(
                f"Roll string ({roll_string}) cannot specify a keep "
                + "high/low (kh, kl, k) greater than the number of dice "
                + f"{self.num_dice}"
            )
        if self.keep.high > 0 and self.keep.low > 0:
            raise ValueError(
                f"Roll string ({roll_string}) cannot specify both keep "
                + "high (kh, k) and keep low (kl) options"
            )

        # Check drop high/low
        if self.drop.high >= self.num_dice or self.drop.low >= self.num_dice:
            raise ValueError(
                f"Roll string({roll_string}) cannot specify a drop "
                + "high/low greater than or equal to the number of dice "
                + f"{self.num_dice}"
            )

        # Check reroll
        invalid_reroll_value = self.num_faces == 1 and self.reroll.value == 1
        if self.reroll and (invalid_reroll_value or self.reroll.under > self.num_faces):
            raise ValueError(
                f"Roll string({roll_string}) cannot specify a reroll "
                + "condition that rerolls every roll (i.e. 1d6r>0 or 1d6r<7)"
            )

        # Check explode
        invalid_explode_value = self.num_faces == 1 and self.explode.value == 1
        if self.explode and (
            invalid_explode_value or self.explode.under > self.num_faces
        ):
            raise ValueError(
                f"Roll string({roll_string}) cannot specify a explode "
                + "condition that explodes every roll (i.e. 1d6x>0 or 1d6x<7)"
            )

    def __str__(self) -> str:
        string_out = (
            "Roll:\n"
            + f"    num_dice: {self.num_dice}\n"
            + f"    num_faces: {self.num_faces}\n"
            + f"    multiplier: {self.multiplier}"
        )

        if self.drop:
            string_out = string_out + "\n" + f"    {self.drop}"

        if self.keep:
            string_out = string_out + "\n" + f"    {self.keep}"

        if self.reroll:
            string_out = string_out + "\n" + f"    {self.reroll}"

        if self.explode:
            string_out = string_out + "\n" + f"    {self.explode}"
        return string_out

    def calculate(self) -> "RollStatsCalculated":
        """Get the calculated statistics for this roll."""
        return RollStatsCalculated(self)

    def simulate(self, num: int = DEFAULT_NUM_SIMULATIONS) -> "RollStatsSimulated":
        """Get the statistics of N attempts of this roll."""
        return RollStatsSimulated(self, num)

    def roll(self, num: int = 1, debug: bool = False) -> List[int]:
        """Simulate a number of die rolls"""
        roll_totals = list()

        for ind_roll in range(num):
            rolls = list()
            num_explosions = 0

            # Roll all of the dice
            ind = 0
            while ind < (self.num_dice + num_explosions):
                num_rerolls = 0
                tmp_roll = random.randint(1, self.num_faces)
                if debug:
                    print(f"roll({ind_roll, ind}): {tmp_roll}")

                # Determine if we need to reroll
                if self.reroll and not (num_rerolls > 0 and self.reroll.once):
                    while (
                        tmp_roll == self.reroll.value
                        or tmp_roll > self.reroll.over
                        or tmp_roll < self.reroll.under
                    ):
                        num_rerolls += 1
                        tmp_roll = random.randint(1, self.num_faces)
                        if debug:
                            print(f"reroll({ind_roll, ind}): {tmp_roll}")
                        if num_rerolls > MAX_REROLLS:
                            raise RuntimeError(
                                f"Number of rerolls exceeded {MAX_REROLLS}, so the simulation was stopped"
                            )

                # Store the result
                rolls.append(tmp_roll)

                # Determine if we need to explode
                explode_test = self.explode and not (
                    num_explosions > 0 and self.explode.once
                )
                if explode_test and (
                    tmp_roll == self.explode.value
                    or tmp_roll > self.explode.over
                    or tmp_roll < self.explode.under
                ):
                    num_explosions += 1
                    if debug:
                        print(f"explosion({ind_roll, ind})")

                # Increment the loop
                ind += 1

                # HACK: Explicit number of tries for explosions
                if num_explosions > MAX_EXPLOSIONS:
                    raise RuntimeError(
                        f"Number of explosions exceeded {MAX_EXPLOSIONS}, so the simulation was stopped"
                    )

            # Determine number of dice to drop
            if self.keep and self.keep.high > 0:
                num_to_drop_low = len(rolls) - self.keep.high
            else:
                num_to_drop_low = self.drop.low
            if self.keep and self.keep.low > 0:
                num_to_drop_high = len(rolls) - self.keep.low
            else:
                num_to_drop_high = self.drop.high

            # Drop any dice
            for ind in range(num_to_drop_low):
                rolls.pop(rolls.index(min(rolls)))
            for ind in range(num_to_drop_high):
                rolls.pop(rolls.index(max(rolls)))

            # Append the sum of these results
            roll_totals.append(sum(rolls))

        return roll_totals


class RollStats:
    """Statistics of a given type of die roll

    Reference for parsing: https://foundryvtt.com/article/dice/
    """

    def __init__(self, roll: Tuple["Roll", str]):
        # Convert strings to Roll objects
        if isinstance(roll, str):
            self.roll = Roll(roll)
        else:
            self.roll = roll

        # Attributes
        self.min = None  # Minimum possible value
        self.max = None  # Maximum possible value
        self.mean = None  # Expected mean average value
        self.median = None  # The middle value of the sorted set of outcomes
        self.mode = None  # Most common expected value
        self.results = None  # Dict where key is possible values and the dict values are the probability of that expected value

    def __str__(self) -> str:
        base_string = (
            f"{self.__class__.__name__}:\n"
            + f"    roll_string: {self.roll.roll_string}\n"
            + f"    min: {self.min}\n"
            + f"    max: {self.max}\n"
            + f"    mean: {self.mean}\n"
            + f"    median: {self.median}\n"
            + f"    mode: {self.mode}\n"
            + f"    results: {self.results}"
        )
        return base_string


class RollStatsCalculated(RollStats):
    """Calculated statistics of a given type of die roll

    Reference for parsing: https://foundryvtt.com/article/dice/
    """

    def __init__(self, roll: Tuple["Roll", str]):
        # Call parent class constructor
        super().__init__(roll)

        # Calculate maximum/minimum value - reroll/reroll once
        if self.roll.reroll and not self.roll.reroll.once:
            if self.roll.reroll.under > 1:
                min_die_value = self.roll.reroll.under
            elif self.roll.reroll.value == 1:
                min_die_value = 2  # Assuming that there are at least two faces
            else:
                min_die_value = 1

            if self.roll.reroll.over < self.roll.num_faces:
                max_die_value = self.roll.reroll.over
            elif self.roll.reroll.value == self.roll.num_faces:
                max_die_value = (
                    self.roll.num_faces - 1
                )  # Assuming that there are at least two faces
            else:
                max_die_value = self.roll.num_faces
        else:
            min_die_value = 1
            max_die_value = self.roll.num_faces

        # Calculate maximum/minimum values
        if self.roll.keep:
            num_to_keep = self.roll.keep.high + self.roll.keep.low
            self.min = self.roll.multiplier * num_to_keep * min_die_value
            self.max = self.roll.multiplier * num_to_keep * max_die_value
        else:
            num_to_drop = self.roll.drop.high + self.roll.drop.low
            remaining_dice = self.roll.num_dice - num_to_drop
            self.min = self.roll.multiplier * remaining_dice * min_die_value
            self.max = self.roll.multiplier * remaining_dice * max_die_value

        if self.roll.reroll or self.roll.explode:
            print("Warning: reroll/explode results & statistics TBD")
            return
        if self.roll.keep:
            print("Warning: keep high/low results & statistics TBD")
            return
        if self.roll.drop:
            print("Warning: drop high/low results & statistics TBD")
            return

        result_keys = list(range(self.min, self.max + 1))

        # Calculate the individual probabilities
        single_die_prob = np.array(
            [1 / self.roll.num_faces] * self.roll.num_faces, dtype=float
        )
        result_values = single_die_prob.copy()
        for _ in range(1, self.roll.num_dice):
            tmp_array = result_values[np.newaxis].T @ single_die_prob[np.newaxis]
            tmp_list = [
                tmp_array[::-1, :].diagonal(i)
                for i in range(-tmp_array.shape[0] + 1, tmp_array.shape[1])
            ]
            diags = [sum(tmp_array.tolist()) for tmp_array in tmp_list]
            result_values = np.array(diags)
        self.results = dict(zip(result_keys, result_values))

        # Calculate mean
        self.mean = sum(np.array(result_keys) * result_values)

        # Calculate mode
        self.mode = result_keys[np.argmax(result_values)]


class RollStatsSimulated(RollStats):
    """Experimentally derived statistics of a given type of die roll

    Reference for parsing: https://foundryvtt.com/article/dice/
    """

    def __init__(self, roll: Tuple["Roll", str], num: int = DEFAULT_NUM_SIMULATIONS):
        # Call parent class constructor
        super().__init__(roll)

        # Attributes
        self.num_rolls = num

        all_rolls = np.array(self.roll.roll(self.num_rolls))
        result_values_counts = np.unique(all_rolls, return_counts=True)
        result_keys = result_values_counts[0]
        result_values = result_values_counts[1] / self.num_rolls
        self.results = dict(zip(result_keys, result_values))

        # Calculate min/max
        self.min = min(result_keys)
        self.max = max(result_keys)

        # Calculate mean
        self.mean = sum(np.array(result_keys) * result_values)

        # Calculate mode
        self.mode = result_keys[result_values.argmax()]

    def __str__(self) -> str:
        base_string = super().__str__()
        return base_string + f"    num_rolls: {self.num_rolls}"


def win(
    roll: Tuple["Roll", "RollStatsCalculated", "RollStatsSimulated", str], target: int
) -> float:
    """Returns the probability that the given roll will meet or exceed the target value"""

    # Converts strings to Rolls and Rolls to RollStats
    if isinstance(roll, str):
        roll = Roll(roll)
    if isinstance(roll, Roll):
        roll = roll.calculate()

    accumulator = 0
    for key, value in roll.results.items():
        if int(key) >= target:
            accumulator += value

    return accumulator


def lose(
    roll: Tuple["Roll", "RollStatsCalculated", "RollStatsSimulated", str], target: int
) -> float:
    """Returns the probability that the given roll will not meet or exceed the target value"""

    # Converts strings to Rolls and Rolls to RollStats
    if isinstance(roll, str):
        roll = Roll(roll)
    if isinstance(roll, Roll):
        roll = roll.calculate()

    accumulator = 0
    for key, value in roll.results.items():
        if int(key) < target:
            accumulator += value

    return accumulator


if __name__ == "__main__":
    roll_advantage = Roll("2d20k")
    roll_stat = Roll("4d6d")
    roll_gwm = Roll("2d6r<3")
    roll_fireball = Roll("8d6")
    roll_basic = Roll("2d6")

    calculated_basic = roll_basic.calculate()
    calculated_fireball = roll_fireball.calculate()
    calculated_advantage = roll_advantage.calculate()
    calculated_stat = roll_stat.calculate()
    calculated_gwm = roll_gwm.calculate()

    simulated_basic = roll_basic.simulate()
    simulated_fireball = roll_fireball.simulate()
    simulated_advantage = roll_advantage.simulate()
    simulated_stat = roll_stat.simulate()
    simulated_gwm = roll_gwm.simulate()

    win_basic = win(roll_basic, 4)

    lose_basic = lose(roll_basic, 4)

    # print(f'basic ({roll_basic.roll_string}): {roll_basic.roll()}')
    # print(f'fireball ({roll_fireball.roll_string}): {roll_fireball.roll()}')
    # print(f'advantage ({roll_advantage.roll_string}): {roll_advantage.roll()}')
    # print(f'stat ({roll_stat.roll_string}): {roll_stat.roll()}')
    # print(f'gwm ({roll_gwm.roll_string}): {roll_gwm.roll()}')

    print(f"basic ({roll_basic.roll_string}): {calculated_basic}")
    print(f"fireball ({roll_fireball.roll_string}): {calculated_fireball}")
    print(f"advantage ({roll_advantage.roll_string}): {calculated_advantage}")
    print(f"stat ({roll_stat.roll_string}): {calculated_stat}")
    print(f"gwm ({roll_gwm.roll_string}): {calculated_gwm}")

    print(f"basic ({roll_basic.roll_string}): {simulated_basic}")
    print(f"fireball ({roll_fireball.roll_string}): {simulated_fireball}")
    print(f"advantage ({roll_advantage.roll_string}): {simulated_advantage}")
    print(f"stat ({roll_stat.roll_string}): {simulated_stat}")
    print(f"gwm ({roll_gwm.roll_string}): {simulated_gwm}")

    # print(f'win ({roll_basic.roll_string} >= 4): {win_basic}')
