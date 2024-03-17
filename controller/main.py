import time

from control.controller import Controller
from control.base_models import SenseData


def main() -> None:
    ctrl = Controller()

    while True:

        time.sleep(5)
        print("")

        # Sense
        sense_data: SenseData = ctrl.sense()
        print(sense_data)

        if sense_data is None:
            continue

        # Think
        action = ctrl.think(sense_data)
        print(action)

        if action is None:
            continue

        # Act
        ctrl.act(action)


if __name__ == "__main__":
    main()
