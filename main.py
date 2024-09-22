# < Coded by Samrat >
import asyncio
import aiohttp
import time
import random
import uuid
from pyrogram import *
from pyrogram.types import *
import pymongo

bot = Client("bot", api_id, "api_hash", bot_token="put your bot token from botfather", in_memory=True)

temp = {}
alr = []
OWNER_ID = 123456789  # replace with your userid
mongodb_uri = "your mongodb uri"  # get this from mongodb.com (example: "mongodb+srv://<username>:<password>@<cluster>/?retryWrites=true&w=majority") [don't include <>]

client = pymongo.MongoClient(mongodb_uri)
db = client["HamsterKombat"]


def add(user_id, username):
    my_collection = db["users"]
    s = my_collection.find_one({"user_id": user_id})
    if not s:
        my_collection.insert_one({"user_id": user_id, "username": username, "hash": ""})

        
def get_hash(user_id):
    my_collection = db["users"]
    s = my_collection.find_one({"user_id": user_id})
    return s["hash"]


def add_hash(user_id, hash):
    my_collection = db["users"]
    return my_collection.update_one({"user_id": user_id}, {"$set": {"hash": hash}})  


def getall():
    my_collection = db["users"]
    return my_collection.find()


async def promogen(a, b, c, bot, msg, rep):

    app_token = a
    promo_id = b
  
    async def generate_client_id():
        hash_id = get_hash(msg.from_user.id)
        if len(hash_id) != 0:
            return hash_id
        else: 
            timestamp = int(time.time() * 1000)
            random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
            hash_id = f"{timestamp}-{random_numbers}"
            add_hash(msg.from_user.id, hash_id)
            return hash_id

    async def login_client():
        client_id = await generate_client_id()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post('https://api.gamepromo.io/promo/login-client', json={
                    'appToken': app_token,
                    'clientId': client_id,
                    'clientOrigin': 'deviceid'
                }, headers={
                    'Content-Type': 'application/json; charset=utf-8',
                }) as response:
                    data = await response.json()
                    return data['clientToken']
            except Exception as error:
                # await rep.reply('**ERROR:** `failed to login`', quote=True)
                await asyncio.sleep(5)
                return await login_client()  

    async def register_event(token):
        event_id = str(uuid.uuid4())
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post('https://api.gamepromo.io/promo/register-event', json={
                    'promoId': promo_id,
                    'eventId': event_id,
                    'eventOrigin': 'undefined'
                }, headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json; charset=utf-8',
                }) as response:
                    data = await response.json()
                    if not data.get('hasCode', False):
                        await asyncio.sleep(5)
                        return await register_event(token)
                    else:
                        return True
            except Exception as error:
                await asyncio.sleep(5)
                return await register_event(token)

    async def create_code(token):
        async with aiohttp.ClientSession() as session:
            response = None
            while not response or not response.get('promoCode'):
                try:
                    async with session.post('https://api.gamepromo.io/promo/create-code', json={
                        'promoId': promo_id
                    }, headers={
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json; charset=utf-8',
                    }) as resp:
                        response = await resp.json()
                except Exception as error:
                    await rep.reply('**ERROR:** `failed to get promoCode, trying again`', quote=True)
                    await asyncio.sleep(1)
            return response['promoCode']

    async def gen():
        token = await login_client()
        
        await register_event(token)
        code_data = await create_code(token)
        temp[msg.from_user.id].append(code_data)

    try:
        tasks = [gen() for _ in range(1)]
        await asyncio.gather(*tasks)
    except Exception as error:
        print(f'error: {error}')


games = {
    "ZOO": {
        "app_token": "b2436c89-e0aa-4aed-8046-9b0515e1c46b",
        "promo_id": "b2436c89-e0aa-4aed-8046-9b0515e1c46b",
    },
    "TILE": {
        "app_token": "e68b39d2-4880-4a31-b3aa-0393e7df10c7",
        "promo_id": "e68b39d2-4880-4a31-b3aa-0393e7df10c7",
    },
    "CUBE": {
        "app_token": "d1690a07-3780-4068-810f-9b5bbf2931b2",
        "promo_id": "b4170868-cef0-424f-8eb9-be0622e8e8e3",
    },
    "TRAIN": {
        "app_token": "82647f43-3f87-402d-88dd-09a90025313f",
        "promo_id": "c4480ac7-e178-4973-8061-9ed5b2e17954",
    },
    "MERGE": {
        "app_token": "8d1cc2ad-e097-4b86-90ef-7a27e19fb833",
        "promo_id": "dc128d28-c45b-411c-98ff-ac7726fbaea4",
    },
    "TWERK": {
        "app_token": "61308365-9d16-4040-8bb0-2f4a4c69074c",
        "promo_id": "61308365-9d16-4040-8bb0-2f4a4c69074c",
    },
    "POLY": {
        "app_token": "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71",
        "promo_id": "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71",
    },
    "TRIM": {
        "app_token": "ef319a80-949a-492e-8ee0-424fb5fc20a6",
        "promo_id": "ef319a80-949a-492e-8ee0-424fb5fc20a6",
    },
    "STONE": {
        "app_token": "04ebd6de-69b7-43d1-9c4b-04a6ca3305af",
        "promo_id": "04ebd6de-69b7-43d1-9c4b-04a6ca3305af",
    },
    "BOUNC": {
        "app_token": "bc72d3b9-8e91-4884-9c33-f72482f0db37",
        "promo_id": "bc72d3b9-8e91-4884-9c33-f72482f0db37",
    },
    "HIDE": {
        "app_token": "4bf4966c-4d22-439b-8ff2-dc5ebca1a600",
        "promo_id": "4bf4966c-4d22-439b-8ff2-dc5ebca1a600",
    },
}


@bot.on_message(filters.command("broadcast_all"))
async def brd(bot, msg):
    if not msg.from_user.id in [OWNER_ID]:
        return    
    if msg.reply_to_message:
        ed = await msg.reply("Broadcasting...")
        try:
            users = getall()
            d = 0
            t = 0
            for x in users:
                t += 1
                user_id = x["username"] if x.get("username") else x["user_id"]
                try:
                    await msg.reply_to_message.copy(user_id)
                    d += 1
                    await asyncio.sleep(0.1)
                    if t % 25 == 0:
                        await ed.edit(f"Broadcasting... {t} done")
                except:
                    pass
                
            await msg.reply(f"Broadcast done to {d} out of {t} users!")    
            return
        except Exception as e:
            await msg.reply(e)
            return
                                                            
    await msg.reply("__reply to a msg to broadcast__") 


@bot.on_message(filters.command("stats"))
async def stats(bot, msg):
    if not msg.from_user.id in [OWNER_ID]:
        return
    try:
        users = getall()
        t = 0
        for x in users:
            t += 1                                                
        await msg.reply(f"Total {t} users!")    
        return
    except Exception as e:
        await msg.reply(e)
        return


@bot.on_message(filters.command("start"))
async def start(bot, msg):
    add(msg.from_user.id, msg.from_user.username)
    await msg.reply(f"**Hello {msg.from_user.mention}! 👋**\nYou can use me to generate Hamster Kombat Keys 🔑 of all the 4 games!\n\n__QnA: The API used in the generation of the keys doesn't contain any user data, so its 100% safe to use!__\n\n**🌀 Usage: /gen**", quote=True)

    
@bot.on_message(filters.command("gen"))
async def start(bot, msg):
    if not msg.from_user.id in alr:
        alr.append(msg.from_user.id)
        temp[msg.from_user.id] = []
    else:
        userid = {"user_id": msg.from_user.id}
        return await msg.reply(f"**ERROR:** `one process is already running for {userid}`")
    
    a = await msg.reply("**⌛️Generating Keys**\n\n**Note: It usually takes about 10 mins if the bot isn't flooded with many users (can take upto an hour in such cases)\n\nIf the process gets aborted, you will get to know!__", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Check Status", "status")],
            ]))
       
    await asyncio.gather(promogen(games["ZOO"]["app_token"], games["ZOO"]["promo_id"], "ZOO", bot, msg, a),
                         promogen(games["TILE"]["app_token"], games["TILE"]["promo_id"], "TILE", bot, msg, a),
                         promogen(games["CUBE"]["app_token"], games["CUBE"]["promo_id"], "CUBE", bot, msg, a),
                         promogen(games["TRAIN"]["app_token"], games["TRAIN"]["promo_id"], "TRAIN", bot, msg, a),
                         promogen(games["MERGE"]["app_token"], games["MERGE"]["promo_id"], "MERGE", bot, msg, a),
                         promogen(games["TWERK"]["app_token"], games["TWERK"]["promo_id"], "TWERK", bot, msg, a),
                         promogen(games["POLY"]["app_token"], games["POLY"]["promo_id"], "POLY", bot, msg, a),
                         promogen(games["TRIM"]["app_token"], games["TRIM"]["promo_id"], "TRIM", bot, msg, a),
                         promogen(games["STONE"]["app_token"], games["STONE"]["promo_id"], "STONE", bot, msg, a),
                         promogen(games["BOUNC"]["app_token"], games["BOUNC"]["promo_id"], "BOUNC", bot, msg, a),
                         promogen(games["HIDE"]["app_token"], games["HIDE"]["promo_id"], "HIDE", bot, msg, a)
                         )    
    
    ZOO = "\n**🔑 [Game] ZOO**\n"
    TILE = "\n**🔑 [Game] TILE**\n"
    cube = "\n**🔑 [Game] CUBE**\n"
    train = "\n**🔑 [Game] TRAIN**\n"
    merge = "\n**🔑 [Game] MERGE**\n"
    twerk = "\n**🔑 [Game] TWERK**\n"
    poly = "\n**🔑 [Game] POLY**\n"
    trim = "\n**🔑 [Game] TRIM**\n"
    STONE = "\n**🔑 [Game] STONE**\n"
    BOUNC = "\n**🔑 [Game] BOUNCE**\n"
    HIDE = "\n**🔑 [Game] HIDE**\n"

    if len(temp[msg.from_user.id]) == 0:
        return await a.reply("__process aborted, unexpected errors occured__")
    for x in temp[msg.from_user.id]:
        if x.startswith("ZOO"):
            ZOO += f"`{x}`\n"
        elif x.startswith("TILE"):
            TILE += f"`{x}`\n"
        elif x.startswith("CUBE"):
            cube += f"`{x}`\n"
        elif x.startswith("TRAIN"):
            train += f"`{x}`\n"
        elif x.startswith("MERGE"):
            merge += f"`{x}`\n"            
        elif x.startswith("TWERK"):
            twerk += f"`{x}`\n"
        elif x.startswith("POLY"):
            poly += f"`{x}`\n"
        elif x.startswith("TRIM"):
            trim += f"`{x}`\n" 
        elif x.startswith("STONE"):
            STONE += f"`{x}`\n" 
        elif x.startswith("BOUNC"):
            BOUNC += f"`{x}`\n" 
        elif x.startswith("HIDE"):
            HIDE += f"`{x}`\n"           
        else: 
            pass

    donate = """**Kindly consider donating:**

💳 **USDT TRC-20:** `UQAX9qPigD9JpdDQ3hhc3PyxUF4w-OK0GbjfPHO6NXTS2wth`
💳 **BTC:** `bc1qztej7fn8k5pn9m8a07h0kd6kjtpa3yajtxcn2c`
💳 **ETH:** `0xa6d2D5b56ED1a78504ea32d0255aF10567B0115c`
💳 **TON:** `UQAX9qPigD9JpdDQ3hhc3PyxUF4w-OK0GbjfPHO6NXTS2wth`"""
    await a.edit_reply_markup()
    b = await a.reply(ZOO + TILE + cube + train + merge + twerk + poly + trim + STONE + BOUNC + HIDE, quote=True)
    await b.reply(donate, quote=True)
    temp[msg.from_user.id].clear()
    alr.remove(msg.from_user.id)


@bot.on_callback_query(filters.regex("status"))
async def cb(bot, query: CallbackQuery):
    user = query.from_user.id
    a, b, c, d, e, f, g, h, i, j, k = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for x in temp[user]:
        if x.startswith("ZOO"):
            a += 1
        elif x.startswith("TILE"):
            b += 1
        elif x.startswith("CUBE"):
            c += 1
        elif x.startswith("TRAIN"):
            d += 1
        elif x.startswith("MERGE"):
            e += 1   
        elif x.startswith("TWERK"):
            f += 1  
        elif x.startswith("POLY"):
            g += 1  
        elif x.startswith("TRIM"):
            h += 1  
        elif x.startswith("STONE"):
            i += 1   
        elif x.startswith("BOUNC"):
            j += 1   
        elif x.startswith("HIDE"):
            k += 1             
        else: 
            pass        

    await query.answer(f"""STATUS of Keys Generated 🔑
    
ZOO: {a}/1
TILE: {b}/1
CUBE: {c}/1
TRAIN: {d}/1
MERGE: {e}/1
TWERK: {f}/1
POLY: {g}/1
TRIM: {h}/1
STONE: {i}/1
BOUNCE: {j}/1
HIDE: {k}/1""", show_alert=True)


bot.start()
idle()
