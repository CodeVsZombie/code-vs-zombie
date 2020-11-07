# Code Vs Zombie

This code is for competition "Code Vs Zombie" on [Codingame](https://www.codingame.com/ide/puzzle/code-vs-zombies)

---

## Install

Install [Poetry](https://python-poetry.org/docs/#installation) in your system.

then install package dependencies

```bash
poetry install
```

---

## Run test

```bash
poetry run pytest
```

---

## Run simulation

```bash
poetry run simulator <simulation-name>
```

> `simulation-name` must be the name of one file inside `simulations` without .siml extension

![Simulation Example](./assets/simulation_example.png)

> :information_source: `blue_dot` is Ash  
> :information_source: `yellow_circle` is Ash attak range  
> :information_source: `red_dot` are Zombies  
> :information_source: `blue_circle` are Zombies attak range  
> :information_source: `green_dot` are Humans

### Simulation File Format

```text
A 13 13
H 1 6 7
H 2 6 7
H 3 6 7
Z 4 5 6
```

---

## Game Objective

- [ ] Save Always max human possible even if we hate them
