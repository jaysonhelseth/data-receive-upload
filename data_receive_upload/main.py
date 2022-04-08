import sys
import asyncio
import mysql.connector
import uuid
import json
from dotenv import dotenv_values
from digi.xbee.devices import XBeeDevice


class ActionRunner:
    def __init__(self, dev, db):
        self.device = XBeeDevice(port=dev, baud_rate=9600)
        self.device.open()

        db_str = json.loads(db)
        self.connection = mysql.connector.connect(**db_str)

    def run(self):
        loop = asyncio.get_event_loop()

        try:
            self.device.add_data_received_callback(self.insert_data)
            loop.run_forever()
        finally:
            loop.close()
            self.connection.close()
            self.device.close()

    def insert_data(self, xbee_message):
        unique_id = str(uuid.uuid4())
        msg = xbee_message.data.decode("utf8")

        cursor = self.connection.cursor()

        # create the statement and add the argument data.
        add_record = ("insert into Sensors values (%s, %s, CURRENT_TIMESTAMP())")
        data = (unique_id, msg)

        cursor.execute(add_record, data)
        self.connection.commit()
        cursor.close()


def main():
    config = dotenv_values(".env")
    if config["DEV"] is None or config["DB"] is None:
        print("Please setup your .env configuration.")
        sys.exit(1)

    runner = ActionRunner(dev=config["DEV"], db=config["DB"])
    runner.run()


if __name__ == '__main__':
    main()
