import telebot
from telebot import types
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials  
CREDENTIALS_FILE = 'inphotechbot-44bc4a5413c7.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
spreadsheetId='1lCrcS7zt53PwyLDEaWlF3hDzfZ6kWlmUZx4wu3JmUpo'

data=[]
def find_type_by_id(id_to_find):
    global data
    return next(filter(lambda x: x['id'] == id_to_find, data), None)['type']

def find_number_by_id(id_to_find):
    global data
    return next(filter(lambda x: x['id'] == id_to_find, data), None)['number']

def setnumber(id_to_set, new_type):
  global data
  for element in data:
    if element['id'] == id_to_set:
      element['number'] = new_type
  return data

token='5631969958:AAHxm0IpX61JYtvMKgrS6lYqrzgH5QtatbE'
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
  buttons=[
    ["95.12 Ремонт обладнання зв'язку"],
    ["62.02 Консультація з питань інформатизації"],
    ["62.01 Комп'ютерне програмування"],
    ["62.09 Інша діяльність у сфері інформаційних технологій"],
    ["33.13 Ремонт і технічне обслуговування елетронного і оптичного устаткування"]
  ]
  keyboard = types.InlineKeyboardMarkup()
  b=0
  for button in buttons:
    b+=1
    keyboard.add(types.InlineKeyboardButton(text=str(button[0]), callback_data=str(b)))
  bot.send_message(message.chat.id,f"{message.from_user.first_name}, Виберіть, будь ласка, яку послугу ви хотіли б замовити.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
  global data
  data.append({'id':call.message.chat.id,'type':call.data})
  keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  reg_button = types.KeyboardButton(text="📞Надіслати номер телефону", request_contact=True)
  keyboard.add(reg_button)
  bot.send_message(call.message.chat.id,f"надішліть свій номер телефону", reply_markup=keyboard)
  bot.register_next_step_handler(call.message,get_number)

def get_number(message):
  try:
    number=message.contact.phone_number
    print(number)
    setnumber(message.from_user.id,number)
    bot.send_message(message.chat.id,f"Вкажіть ваше Прізвище, Ім'я, По батькові.", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message,save)
  except:
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="📞Надіслати номер телефону", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id,f"надішліть свій номер телефону!", reply_markup=keyboard)
    bot.register_next_step_handler(message,get_number)

def save(message):
  global spreadsheetId, service, data
  print(data)
  bot.send_message(message.chat.id,f"Готово")
  results = service.spreadsheets().values().append(
    spreadsheetId = spreadsheetId,
    range="Лист!A1",
    valueInputOption='RAW',
    body={'values': [[message.text, find_type_by_id(message.from_user.id), find_number_by_id(message.from_user.id)]]}).execute()
bot.polling()