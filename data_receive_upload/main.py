import argparse
import sys


class ActionRunner:
    def __init__(self, dev, db):
        self.dev = dev
        self.dbStr = db

    def run(self):
        print("Doing stuff")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=str,
                        help="The serial device to use.")
    parser.add_argument("--db", type=str,
                        help="The database connection string.")
    args = parser.parse_args()

    if args.dev is None or args.db is None:
        parser.print_help()
        sys.exit(1)

    runner = ActionRunner(dev=args.dev, db=args.db)
    runner.run()


if __name__ == '__main__':
    main()
