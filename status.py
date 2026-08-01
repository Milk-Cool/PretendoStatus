import base64
import logging

from asgiref.sync import async_to_sync

from nintendo import nnas, nasc
from nintendo.nex import backend, settings
from nintendo.nex.authentication import AuthenticationInfo
from dns import resolver
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO)

access_token_3ds = None
access_token_3ds_expire = datetime.now()
nex_token = None
nex_token_expire = datetime.now()

@async_to_sync
async def checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, _COUNTRY_ID, _REGION_NAME, COUNTRY_NAME,
                    LANGUAGE, USERNAME, PASSWORD, CERT, TITLE_ID, TITLE_VERSION, ACCESS_KEY, NEX_VERSION,
                    GAME_SERVER_ID: int = None):
    if GAME_SERVER_ID is None:
        GAME_SERVER_ID = TITLE_ID & 0xFFFFFFFF
    try:
        global nex_token, nex_token_expire
        s = settings.default()
        s.configure(ACCESS_KEY, NEX_VERSION)
        if datetime.now() >= nex_token_expire:
            print("Expired token. Regenerating...")
            print(datetime.now())
            print(nex_token_expire)
            nas = nnas.NNASClient()
            nas.set_device(DEVICE_ID, SERIAL_NUMBER,
                           SYSTEM_VERSION, CERT)
            nas.set_title(TITLE_ID, TITLE_VERSION)
            nas.set_locale(REGION_ID, COUNTRY_NAME, LANGUAGE)

            access_token = await nas.login(USERNAME, PASSWORD, "hash")

            nex_token_expire = datetime.now() + timedelta(hours=1) # Ratelimit
            nex_token = await nas.get_nex_token(access_token.token, GAME_SERVER_ID)
            print("Token regenerated")

        s = settings.default()
        s.configure(ACCESS_KEY, NEX_VERSION)
        async with backend.connect(s, nex_token.host, nex_token.port) as be:
            be.login(str(nex_token.pid), nex_token.password)
            return True
    except Exception as e:
        print(f"Server {hex(TITLE_ID)} down!")
        logging.exception(e)
        return False


def splatoon(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x0005000010162B00, 272, "6f599f81", 30500)


def mk8(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x000500001010EB00, 64, "25dbf96a", 30504)


def smm(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x000500001018DB00, 64, "9f2b4678", 30803)


def friends(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x0005000010001C00, 0, "ridfebb9", 20000, 0x3200)


def minecraft(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x00050000101D9D00, 0, "f1b61c8e", 31000)


def pikmin3(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x0005000E1012BC00, 0, "f6accfc1", 30300)


def wiiuchat(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x000500101005A000, 0, "e7a47214", 30402)


def drluigi(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x0005000010150300, 0, "2a724fa4", 30502)


def smashu(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x0005000C10110E00, 0, "2869ba38", 30600)





def pokken(
        DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION,
        REGION_ID, COUNTRY_ID, REGION_NAME,
        COUNTRY_NAME, LANGUAGE, USERNAME,
        PASSWORD, CERT
):
    return checkWiiU(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_ID, REGION_NAME, COUNTRY_NAME,
                     LANGUAGE, USERNAME, PASSWORD, CERT, 0x00050000101C5800, 0, "6ef3adf1", 31000)



@async_to_sync
async def check3DS(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, TITLE_ID,
        TITLE_VERSION, ACCESS_KEY, NEX_VERSION, GAME_SERVER_ID: int = None
):
    global access_token_3ds, access_token_3ds_expire
    if GAME_SERVER_ID is None:
        GAME_SERVER_ID = TITLE_ID & 0xFFFFFFFF
    try:
        if datetime.now() >= access_token_3ds_expire:
            print("Expired token. Regenerating...")
            nas = nasc.NASCClient()
            nas.set_title(TITLE_ID, TITLE_VERSION)
            nas.set_device(SERIAL_NUMBER, MAC_ADDRESS, bytes.fromhex(DEVICE_CERT), DEVICE_NAME)
            nas.set_locale(REGION_ID, LANGUAGE)
            nas.set_user(PID, PID_HMAC)

            access_token_3ds_expire = datetime.now() + timedelta(hours=1) # Ratelimit
            access_token_3ds = await nas.login(GAME_SERVER_ID, DEVICE_NAME)
            if access_token_3ds is not None:
                print("Token regenerated successfully.")
            else:
                print("Token regeneration failed.")

        s = settings.default()
        s.configure(ACCESS_KEY, NEX_VERSION)
        async with backend.connect(s, access_token_3ds.host, access_token_3ds.port) as be:
            be.login(str(PID), base64.b64decode(NEX_PASSWORD).decode("utf-8"))
            return True

    except Exception as e:
        print(f"Server {hex(TITLE_ID)} down!")
        logging.exception(e)
        return False

def mk7(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000030600,
                    0, "6181dff1",
                    20403)

def steeldiver(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x00040000000D7C00,
                    0, "fb9537fe",
                    30700)

def smash3d(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x00040000000B8B00,
                    0, "9002f8c2",
                    30700)

def luigi(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000076400,
                    0, "3861a9f8",
                    30100)

def triforce(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000176E00,
                    0, "c1621b84",
                    30900)

def mh4u(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x000400000011D700,
                    0, "d44c6198",
                    30601)

def icarus(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000030000,
                    0, "58a7e494",
                    20702)

def ironfall(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x000400000017D000,
                    0, "feb81c7c",
                    30701)

def kirbyclash(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x00040000001A0000,
                    0, "e0c85605",
                    31001)

def pokexy(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000055E00,
                    0, "876138df",
                    30300)

def tippingstars(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x000400000012C900,
                    0, "d8927c3f",
                    30701)

def ykwblasters(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x00040000001CEF00,
                    0, "49744f0b",
                    30901, 0x0016C600)

def miraclecure(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x000400000013BB00,
                    0, "07f4860a",
                    30701)
def rumbleworld(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000185A00,
                    0, "844f1d0c",
                    30813)
def acnl(
        MAC_ADDRESS, SERIAL_NUMBER,
        REGION_ID,
        LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD
):
    return check3DS(MAC_ADDRESS, SERIAL_NUMBER,
                    REGION_ID,
                    LANGUAGE, DEVICE_CERT, DEVICE_NAME, PID, PID_HMAC, NEX_PASSWORD, 0x0004000000086300,
                    0, "d6f08b40",
                    31001)

def sssl():
    r = resolver.Resolver(configure=False)
    r.nameservers = ['88.198.140.154']
    try:
        answers = r.resolve("account.nintendo.net", "A")
        for ip in answers:
            if str(ip) == "88.198.140.154":
                return True
        return False
    except dns.exception.DNSException:
        return False
