from datetime import datetime

from app.core.config import settings

DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
REPORT_DATE = datetime.now().strftime(DATE_FORMAT)
SPREADSHEET_URL_TEMPLATE = 'https://docs.google.com/spreadsheets/d/{}/edit'

MIN_SIZE = 100
MAX_SIZE = 1000

TABLE_HEADER = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]

DISCOVER_SHEETS_V4 = ('sheets', 'v4')
DISCOVER_DRIVE_V3 = ('drive', 'v3')

SPREADSHEET_PROPERTIES = {
    'properties': {
        'title': 'Отчет от {datetime.now().strftime(DATE_FORMAT)}',
        'locale': 'ru_RU',
    },
    'sheets': {
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {'rowCount': 100, 'columnCount': 11},
        }
    },
}

PERMISSIONS_CONFIG = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email,
    'fields': 'id',
}
