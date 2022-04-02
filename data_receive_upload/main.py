import argparse
import sys
import asyncio
import mysql.connector
import uuid
import time
import json


class ActionRunner:
    def __init__(self, dev, db):
        self.dev = dev
        db_str = json.loads(db)
        self.connection = mysql.connector.connect(**db_str)

    def run(self):
        print("Doing stuff")

        loop = asyncio.get_event_loop()
        try:
            self.test_db()
            loop.run_forever()
        finally:
            loop.close()
            # close db and device here
            self.connection.close()

    def test_db(self):
        add_record = ("insert into Sensors values (%s, %s, CURRENT_TIMESTAMP())")
        cursor = self.connection.cursor()

        while True:
            data = (str(uuid.uuid4()), f'{{ "data": "{uuid.uuid4()}"}}')
            print(data)
            cursor.execute(add_record, data)
            self.connection.commit()
            time.sleep(1)

        cursor.close()


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
