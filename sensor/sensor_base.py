import datetime

import config
from sensor.google_sheets_writer import GoogleSheetsWriter


class SensorBase:

    def read_data(self):
        pass

    def periodic_gsheets_write(self, now, interval_in_min, sheet_value_dict):
        sheets_writer = GoogleSheetsWriter(config.SHEETS_CREDENTIAL_PATH,
                                           config.SPREADSHEET_ID)

        if now + datetime.timedelta(
                minutes=interval_in_min) < datetime.datetime.now():
            now = datetime.datetime.now()
            for sheet in sheet_value_dict.keys():
                sheets_writer.write(sheet, [now.isoformat('|', 'seconds'),
                                            sheet_value_dict[sheet]])
        return now
