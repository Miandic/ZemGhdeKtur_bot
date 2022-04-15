import logging, secret, time
from aiogram import Bot, Dispatcher, executor, types
from getpass import getpass
from python_aternos import Client

#Aternos part
aternos = Client.from_credentials(secret.aternUser, secret.aternPass)
srvs = aternos.list_servers()
print(srvs)


#Telegram part
API_TOKEN = secret.TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

'''
for srv in srvs:
    print('*** ' + srv.domain + ' ***')
    print(srv.motd)
    print('*** Status:', srv.status)
    print('*** Full address:', srv.address)
    print('*** Port:', srv.port)
    print('*** Name:', srv.subdomain)
    print('*** Minecraft:', srv.software, srv.version)
    print('*** IsBedrock:', srv.edition == atserver.Edition.bedrock)
    print('*** IsJava:', srv.edition == atserver.Edition.java)
'''

@dp.message_handler(commands=['start'])
async def msg_welcome(message: types.Message):
    await message.reply("Приветствую!\nЯ пинатель-пингователь для майнкрафт сервера ZemghdeKtur.aternos.me\n\nБольше: /help\nПриятного использования!")


@dp.message_handler(commands=['help'])
async def msg_help(message: types.Message):
    await message.reply("Бот находится в разработке!\n\nСписок доступных команд:\n/help - Увидеть это сообщение\n/status - Узнать статус сервера\n/kick - Поднять сервак\n/gently_wake_up - Поднять сервер, но аккуратно\nПо тех. вопросам бота: @Miandic")


@dp.message_handler(commands=['status'])
async def msg_help(message: types.Message):
    srvs = aternos.list_servers()
    s = srvs[0]
    await message.reply("Статус сервера:" + s.status)


@dp.message_handler(commands=['kick'])
async def msg_kick(message: types.Message):
    srvs = aternos.list_servers()
    s = srvs[0]
    print("Processing /kick")
    print(s.status)
    if s.status == 'online':
        await message.reply("Сервер работает и приветствует вас!")
    elif s.status == 'loading starting':
        await message.reply("Сервер прямо сейчас поднимается... Терпение, мой друг")
    elif s.status == 'loading':
        await message.reply("Сервер загружается... Попробуйте ещё раз через несколько секунд...")
    elif s.status == 'offline':
        await message.reply("Пинаем сервер...")
        s.start()
        cntr = 120
        while s.status != 'online' and cntr != 0:
            srvs = aternos.list_servers()
            s = srvs[0]
            print("Status: " + s.status + "; waiting " + str(120-cntr) + " seconds...")
            cntr -= 1
            time.sleep(1)
        if s.status == 'online':
            await message.reply("Сервер работает и приветствует вас!")
        else:
            await message.reply("Сервер ещё не запустился... Используйте /status для информации о состоянии сервера или попробуйте /gently_wake_up (дольше)")


@dp.message_handler(commands=['gently_wake_up'])
async def msg_gentelwake(message: types.Message):
    srvs = aternos.list_servers()
    s = srvs[0]
    print("Processing /gently_wake_up")
    print(s.status)
    if s.status == 'online':
        await message.reply("Сервер работает и приветствует вас!")
    else:
        await message.reply("Выполняется презагрузка сервера... Ожидайте")
        s.stop()
        cntr = 120
        while s.status != 'ofline' and cntr != 0:
            srvs = aternos.list_servers()
            s = srvs[0]
            cntr -= 1
            time.sleep(1)
        s.start()
        cntr = 120
        while s.status != 'online' and cntr != 0:
            srvs = aternos.list_servers()
            s = srvs[0]
            print("Status: " + s.status + "; waiting " + str(120-cntr) + " seconds...")
            cntr -= 1
            time.sleep(1)
        if s.status == 'online':
            await message.reply("Сервер работает и приветствует вас!")
        else:
            await message.reply("Сервер ещё не запустился... Используйте /status для информации о состоянии сервера или попробуйте /gently_wake_up (дольше)")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
