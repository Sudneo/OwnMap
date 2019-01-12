from ownmap.Portscan import Portscan


def main():
    ps = Portscan()
    ps.run()
    ps.save_state()


if __name__ == '__main__':
    main()