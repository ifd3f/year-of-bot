import random

from datetime import datetime

from . import data


def generate_prediction():
    today = datetime.now()
    y = random.randint(today.year, today.year + 25)
    p_template = random.choice(random.choice(data.predictions))

    fmt_dict = generate_fmt_dict()

    prediction = p_template.format(**fmt_dict)

    return f"{y} will be the year of {prediction}"


def generate_fmt_dict():
    fmt_dict = {f"s{i}": random.choice(data.subjects) for i in range(1, 10)}
    fmt_dict["s"] = random.choice(data.subjects)

    return fmt_dict
