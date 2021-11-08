# Pyroller

Basic die-rolling probability functions

- [Pyroller](#pyroller)
  - [The `Roll` class - Defining die rolls](#the-roll-class---defining-die-rolls)
    - [`Roll.calculate()` - Calculating die roll statistics](#rollcalculate---calculating-die-roll-statistics)
    - [`Roll.simulate()` - Simulating die roll statistics](#rollsimulate---simulating-die-roll-statistics)
    - [`win()` - Chance to meet or exceed a target value](#win---chance-to-meet-or-exceed-a-target-value)
    - [`lose()` - Chance to roll less than a target value](#lose---chance-to-roll-less-than-a-target-value)

---

## The `Roll` class - Defining die rolls

Rolls are defined by roll strings, following Roll20 syntax (i.e. `1d6+1`, `2d20kh1`, etc.). The predicted results for most rolls can be calculated, but some rolls are not fully supported by this module and their results must be simulated by rolling a number of dice and observing the statistics of the actual results.

Rolls are defined by Roll objects.

```python
import pyroller
fireball = pyroller.Roll('8d6')
```

### `Roll.calculate()` - Calculating die roll statistics

The `calculate()` method can be used to calculate the full statistics of a roll:

- minimum value
- maximum value
- mean value
- median value
- mode value
- results (dictionary of every possible result and its probability)

```shell
In [3]: fireball = pyroller.Roll('8d6')
   ...: print(f'fireball: {fireball.calculate()}')
fireball: RollStatsCalculated:
    roll_string: 8d6
    min: 8
    max: 48
    mean: 28.0
    median: None
    mode: 28
    results: {8: 5.953741807651271e-07, 9: 4.7629934461210166e-06, 10: 2.1433470507544573e-05, 11: 7.144490169181524e-05, 12: 0.00019647347965249192, 13: 0.0004715363511659807, 14: 0.001016899100746837, 15: 0.0020052202408169482, 16: 0.0036597650891632364, 17: 0.006239521414418533, 18: 0.010007049230300259, 19: 0.015174897119341562, 20: 0.021843087943910985, 21: 0.029940176802316712, 22: 0.03918038408779149, 23: 0.04904930650815423, 24: 0.0588307089239445, 25: 0.06768689986282575, 26: 0.07477185261393077, 27: 0.07935623380582225, 28: 0.08094350137174208, 29: 0.07935623380582227, 30: 0.07477185261393078, 31: 0.06768689986282576, 32: 0.05883070892394451, 33: 0.04904930650815423, 34: 0.03918038408779148, 35: 0.029940176802316705, 36: 0.02184308794391098, 37: 0.015174897119341557, 38: 0.010007049230300255, 39: 0.006239521414418532, 40: 0.0036597650891632364, 41: 0.0020052202408169482, 42: 0.0010168991007468372, 43: 0.0004715363511659808,
44: 0.00019647347965249197, 45: 7.144490169181525e-05, 46: 2.1433470507544577e-05, 47: 4.7629934461210166e-06, 48: 5.953741807651271e-07}
```

### `Roll.simulate()` - Simulating die roll statistics

The `simulate()` method can be used to simulate the results of rolls whose probabilities cannot be directly calculated. To simulate a roll, you must also choose a number of rolls to perform.

```shell
In [5]: fireball = pyroller.Roll('8d6')
   ...: print(f'fireball (1000 rolls): {fireball.simulate(1000)}')
fireball (1000 rolls): RollStatsSimulated:
    roll_string: 8d6
    min: 15
    max: 42
    mean: 27.862
    median: None
    mode: 29
    results: {15: 0.001, 16: 0.002, 17: 0.003, 18: 0.015, 19: 0.015, 20: 0.028, 21: 0.031, 22: 0.046, 23: 0.055, 24: 0.053, 25: 0.065, 26: 0.081, 27: 0.078, 28: 0.082, 29: 0.084, 30: 0.068, 31: 0.082, 32: 0.045, 33: 0.047, 34: 0.02, 35: 0.039, 36: 0.017, 37: 0.016, 38: 0.01, 39: 0.008, 40: 0.004, 41: 0.004, 42: 0.001}    num_rolls: 1000
```

### `win()` - Chance to meet or exceed a target value

```shell
In [9]: pyroller.win('1d20+5', 15)
Out[9]: 0.3
```

```shell
In [11]: pyroller.win(pyroller.Roll('2d20kh1+5').simulate(1000), 15)
Out[11]: 0.512
```

### `lose()` - Chance to roll less than a target value

```shell
In [10]: pyroller.lose('1d20+5', 15)
Out[10]: 0.7000000000000001
```

```shell
In [12]: pyroller.lose(pyroller.Roll('2d20kh1+5').simulate(1000), 15)
Out[12]: 0.47700000000000004
```
