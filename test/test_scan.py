from ownmap.Portscan import Portscan
from ownmap.State import *
import ownmap.db.DB_Interface


def main():
    state_A = ownmap.db.DB_Interface.load_state()
    ps = Portscan()
    ps.run()
    ps.save_state()
    state_B = ownmap.db.DB_Interface.load_state()
    delta = State.compare(state_A, state_B)
    print(delta)


if __name__ == '__main__':
    main()