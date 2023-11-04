import inquirer
import re

email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def validate_target(_answers, current) -> bool:
    if not re.match(email_regex, current):
        raise inquirer.errors.ValidationError("", reason="\u001b[31mInvalid email address format.")
    return True

def validate_amount_and_delay(_answers, current) -> bool:
    if not current.isnumeric():
        raise inquirer.errors.ValidationError("", reason="\u001b[31mInvalid number.")
    return True

questions = [
    inquirer.Text(
        "target",
        message="target email",
        validate=validate_target,
    ),
    inquirer.Text(
        "amount",
        message="how many emails",
        validate=validate_amount_and_delay,
    ),
    inquirer.Text(
        "delay",
        message="delay",
        validate=validate_amount_and_delay,
    ),
        inquirer.List(
            "proxies",
            message="Use proxies (less emails sent, more anonymous)?",
            choices=["yes", "no"],
            default="no",
    ),
]