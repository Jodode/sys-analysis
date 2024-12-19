import json
from typing import Dict, List, Tuple, Union
from dataclasses import dataclass

@dataclass
class FuzzySystem:
    temperature_set: Dict[str, List[List[float]]]
    regulator_set: Dict[str, List[List[float]]]
    transition_map: Dict[str, str]

    @classmethod
    def from_json(cls, temp_json: str, reg_json: str, trans_json: str) -> 'FuzzySystem':
        return cls(
            json.loads(temp_json),
            json.loads(reg_json),
            json.loads(trans_json)
        )

class FuzzyCalculator:
    def calculate_mu(x: float, points: List[List[float]]) -> float:
        for (x0, mu0), (x1, mu1) in zip(points[:-1], points[1:]):
            if x0 <= x <= x1:
                return mu0 if mu0 == mu1 else mu0 + (mu1 - mu0) * (x - x0) / (x1 - x0)
        return 0
    
    @staticmethod
    def fuzzify(input_value, fuzzy_set) -> Dict[str, float]:
        mu_vals = {
            term: round(FuzzyCalculator.calculate_mu(input_value, points), 2)
            for term, points in fuzzy_set.items()
        }
        print(f"Результат фаззификации температуры {input_value}: {mu_vals}\n")
        return mu_vals
    
    @staticmethod
    def map_to_regulator(temp_mu_vals, transition_map) -> Dict[str, float]:
        regulator_mu_vals = {}
        for temp_term, temp_mu in temp_mu_vals.items():
            reg_term = transition_map[temp_term]
            regulator_mu_vals[reg_term] = max(
                regulator_mu_vals.get(reg_term, 0),
                temp_mu
            )
        
        print(f"Результат проекции на нечеткое множество положений регулятора: {regulator_mu_vals}\n")
        return regulator_mu_vals

    @staticmethod
    def defuzzify_meanmax(regulator_mu_vals, fuzzy_set) -> float:
        max_mu = max(regulator_mu_vals.values())
        x_values = []

        for term, mu in regulator_mu_vals.items():
            if mu == max_mu:
                points = fuzzy_set[term]
                for (x0, mu0), (x1, mu1) in zip(points[:-1], points[1:]):
                    if mu0 <= max_mu <= mu1 or mu1 <= max_mu <= mu0:
                        x = x0 if mu0 == mu1 else x0 + (x1 - x0) * (max_mu - mu0) / (mu1 - mu0)
                        x_values.append(x)

        return sum(x_values) / len(x_values) if x_values else 0

def process_temperature(system: FuzzySystem, temperature: float) -> float:
    calculator = FuzzyCalculator()
    temp_mu_vals = calculator.fuzzify(temperature, system.temperature_set)
    regulator_mu_vals = calculator.map_to_regulator(temp_mu_vals, system.transition_map)
    result = calculator.defuzzify_meanmax(regulator_mu_vals, system.regulator_set)
    
    print(f"Дефаззифицированное положение регулятора методом среднего максимума: {result}\n")

    return result

def main(temperatures_json: str, regulator_json: str, transition_json: str, temperature_input: float):
    system = FuzzySystem.from_json(temperatures_json, regulator_json, transition_json)
    process_temperature(system, temperature_input)

temperatures = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0, 0],
        [22, 0],
        [26, 1],
        [50, 1]
    ]
}"""

regulator = """{
    "слабо": [
        [0, 1],
        [6, 1],
        [10, 0],
        [20, 0]
    ],
    "умеренно": [
        [6, 0],
        [10, 1],
        [12, 1],
        [16, 0]
    ],
    "интенсивно": [
        [0, 0],
        [12, 0],
        [16, 1],
        [20, 1]
    ]
}"""

transition = """{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}"""

if __name__ == '__main__':
    main(temperatures, regulator, transition, 25)