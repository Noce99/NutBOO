import json
import pathlib
import os
import random

NUM_OF_TEAMS = 111

if __name__ == "__main__":
    current_path = pathlib.Path(__file__).parent.resolve()
    teams_path = os.path.join(current_path, "src_server", "teams.json")

    teams = []
    for i in range(NUM_OF_TEAMS):
        teams.append(
            {
                "name": "Ellemazing",
                "passcode": "Ellen"
            }
        )

    with open(teams_path, mode='w') as f:
        f.write(json.dumps(teams, indent=4))
