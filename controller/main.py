
from controller.controller import Controller


def main() -> None:
    ctrl = Controller()
    # Example sequence of operations
    ctrl.sense_environment()
    ctrl.decide_action()
    ctrl.act()


if __name__ == "__main__":
    main()
