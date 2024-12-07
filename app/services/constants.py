from app.core.config import settings

DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

MIN_SIZE = 100
MAX_SIZE = 1000

ROW_COUNT = 100
COLUMN_COUNT = 11

TABLE_HEADER = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]

DISCOVER_SHEETS_V4 = ('sheets', 'v4')
DISCOVER_DRIVE_V3 = ('drive', 'v3')

SPREADSHEET_PROPERTIES = {
    'properties': {
        'title': 'Отчет',
        'locale': 'ru_RU',
    },
    'sheets': {
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': ROW_COUNT, 'columnCount': COLUMN_COUNT
            },
        }
    },
}

PERMISSIONS_CONFIG = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email,
    'fields': 'id',
}
