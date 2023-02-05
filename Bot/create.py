import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
CREDENTIALS_FILE = 'inphotechbot-44bc4a5413c7.json'  # Имя файла с закрытым ключом, вы должны подставить свое
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 
def create_file():
    spreadsheet = service.spreadsheets().create(body = {
        'properties': {'title': 'Інфотех бот', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист',
                                   'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId = spreadsheetId,
        body = {'type': 'user', 'role': 'writer', 'emailAddress': 'mishapatioha03@gmail.com'},  # Открываем доступ на редактирование
        fields = 'id'
    ).execute()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"Лист!A1",
             "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
             "values": [
                        ["ПІБ", "Вид діяльності", "Номер телефону"]
                       ]}
        ]
    }).execute()
    return spreadsheetId
spreadsheetId=create_file()   
print(f'id: {spreadsheetId}')
print(f'url: https://docs.google.com/spreadsheets/d/{spreadsheetId}')
input()
input()
