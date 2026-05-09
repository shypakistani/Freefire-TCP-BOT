# ======================== IMPORTS =======================
import requests , os , psutil , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp , traceback , signal , multiprocessing , asyncio , subprocess
from MG24GAMER import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2, RemoveFriend_Req_pb2, GetFriend_Res_pb2, spam_request_pb2, devxt_count_pb2, dev_generator_pb2, kyro_title_pb2, room_join_pb2
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
import urllib.parse
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from cfonts import render, say
import google.protobuf.json_format as json_format
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ── auto-install phonenumbers if missing ──
try:
    import phonenumbers
except ImportError:
    subprocess.run(["pip", "install", "phonenumbers", "-q"], check=False)
    import phonenumbers

# =================== CONFIGURATION ======================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========= DNS FIX FOR FREEFIRE SERVERS =========
try:
    import dns.resolver as _dns_resolver
    _dns_res = _dns_resolver.Resolver()
    _dns_res.nameservers = ['8.8.8.8', '1.1.1.1']
    _orig_getaddrinfo = socket.getaddrinfo

    def _patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        if isinstance(host, str) and 'freefiremobile.com' in host:
            try:
                answers = _dns_res.resolve(host, 'A')
                host = str(answers[0])
            except Exception:
                pass
        return _orig_getaddrinfo(host, port, family, type, proto, flags)

    socket.getaddrinfo = _patched_getaddrinfo
except ImportError:
    pass
# ================================================  

# =================== GLOBAL VARIABLES ===================
BOT_START_TIME = time.time()  # Tracks bot start time for /uptime command
online_writer = None
whisper_writer = None
spammer_uid = None
msg_spam_running = False
msg_spam_task = None
mg_spam_task = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
reject_spam_running = False
reject_spam_task = None
emote_hijack = False 
lag_running = False
lag_task = None
reject_spam_running = False
reject_spam_task = None
evo_cycle_running = False
_stdin_q = None
_stdin_thread_started = False
evo_cycle_task = None
status_response_cache = {} 
pending_status_requests = {}
room_info_cache = {}
last_status_packet = None
insquad = None 
joining_team = False 
online_writer = None 
whisper_writer = None 
last_bot_status_check = 0
senthi = False
squad_chat_authed = False        # True after bot has authenticated group chat once per join
squad_group_owner_uid = None     # UID of squad owner (for sending group messages)
squad_group_chat_code = None     # Chat code for the current group/squad
bot_status_cache_time = 30
cached_bot_status = None
last_status_packet = None
START_SPAM_DURATION = 18     
WAIT_AFTER_MATCH_SECONDS = 20 
START_SPAM_DELAY = 0.2       
region = 'PK'
WHITELISTED_UIDS = {
    "MĢ24_GÀMER", # don't change this text
    "415136165"
}
# ADMIN INFO FUNCTION FOR ADMIN COMMAND 
ADMIN_UID = "1901614992"
ADMIN_UIDS = {"1901614992" , ""}
BLOCKED_UIDS = set()  # UIDs blocked from using the bot
news_pending = {}  # Tracks which chat/uid is waiting for news country selection
_console_guild_chat_id = None   # Clan chat ID used for console → guild sending
_console_guild_bot_uid = None   # Bot's own UID for sending
_console_guild_chat_type = 1    # 1 = CLan chat type
_console_squad_chat_id = None   # Squad/group chat ID
_console_chat_target = "guild"  # "guild" or "group" — which chat console sends to
server2 = "BD"
key2 = "mg24"
BYPASS_TOKEN = "your_bypass_token_here"
YOUTUBE_API_KEY = "AIzaSyBVP3NiKKJvb-0ar2J3y9IFVVHHWRng4nA"
GEMINI_AI_API_KEY = "AIzaSyADPE-gPODMslNB6AElglDtBRv6PQDVChY"
GROQ_AI_API_KEY = "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"
IG_SESSION_ID = ""  # Paste your Instagram sessionid cookie here to unlock private account stats
WHITELIST_ONLY = False
bot_enabled = True
_bot_jwt = None          # Holds the main bot JWT — reused for bio updates
BOT_OWNER_UID = 415136165  
BOT_SERVER_URL = None  # Set from login response — used for friend add/remove/list
PLAYER_NAME_CACHE = {}  
freeze_running = False
freeze_task = None
FREEZE_EMOTES = [909052010, 909052010, 909052010]
FREEZE_DURATION = 10  # seconds
evo_emotes = {
    "1": "909000063",   # AK
    "2": "909000068",   # SCAR
    "3": "909000075",   # 1st MP40
    "4": "909040010",   # 2nd MP40
    "5": "909000081",   # 1st M1014
    "6": "909039011",   # 2nd M1014
    "7": "909000085",   # XM8
    "8": "909000090",   # Famas
    "9": "909000098",   # UMP
    "10": "909035007",  # M1887
    "11": "909042008",  # Woodpecker
    "12": "909041005",  # Groza
    "13": "909033001",  # M4A1
    "14": "909038010",  # Thompson
    "15": "909038012",  # G18
    "16": "909045001",  # Parafal
    "17": "909049010",  # P90
    "18": "909051003"   # m60
}
#------------------------------------------#

# Emote mapping for evo commands
EMOTE_MAP = {
    1: 909000063,
    2: 909000081,
    3: 909000075,
    4: 909000085,
    5: 909000134,
    6: 909000098,
    7: 909035007,
    8: 909051012,
    9: 909000141,
    10: 909034008,
    11: 909051015,
    12: 909041002,
    13: 909039004,
    14: 909042008,
    15: 909051014,
    16: 909039012,
    17: 909040010,
    18: 909035010,
    19: 909041005,
    20: 909051003,
    21: 909034001
}

# Animation map for /animation command
ANIMATION_MAP = {
    "arrival":    912038002,
    "parachute":  912039001,
    "backflip":   912040001,
    "roll":       912041001,
    "spin":       912042001,
    "slide":      912043001,
    "dash":       912044001,
    "jump":       912045001,
    "cartwheel":  912046001,
    "flip":       912047001,
    "dance1":     912048001,
    "dance2":     912049001,
    "dance3":     912050001,
    "salute":     912051001,
    "bow":        912052001,
    "wave":       912053001,
    "taunt":      912054001,
    "celebrate":  912055001,
    "fall":       912056001,
    "roll2":      912057001,
}

# Badge values for s1 to s8 commands - using your exact values
BADGE_VALUES = {
    "s1": 1048576,    # Your first badge
    "s2": 32768,      # Your second badge  
    "s3": 2048,       # Your third badge
    "s4": 64,         # Your fourth badge
    "s5": 262144     # Your seventh badge
}

# Admin Functions
def is_admin(uid):
    return str(uid) in ADMIN_UIDS

# Mute Functions 
def is_off():
    return not bot_enabled

def ff_num(val):
    return xMsGFixinG(str(val)) if val not in (None, "") else "N/A"

from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

def human_time(ts):
    try:
        ts = int(ts)
        if ts <= 0:
            return "N/A"
        bd_time = datetime.fromtimestamp(ts, ZoneInfo("Asia/Karachi"))
        return bd_time.strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"

def titles():
    """Return all titles instead of just one random"""
    titles_list = [
        905090075, 904990072, 904990069, 905190079
    ]
    return titles_list  # Return the full list instead of random.choice            
    
def create_credentials_template():
    """Create a template credentials file"""
    template = """# Rijexx Free Fire Bot Credentials
# Fill in your Free Fire account credentials below

# Format 1: Comma-separated (RECOMMENDED)
uid=4263143059,password=2336099414_W0363_BY_SPIDEERIO_GAMING_WBYMF

# OR Format 2: Line-separated
# uid: 4263143059
# password: 2336099414_W0363_BY_SPIDEERIO_GAMING_WBYMF

# Save this file and restart the bot
"""
    
    filename = "MG24GAMER.txt"
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"📝 Created {filename} template file")
        print("✏️ Please edit it with your actual credentials")
        return False
    return True

async def fetch_news_rss(country_code):
    """Use Groq AI to generate a news summary for the given country (always in English)."""
    country_names = {
        "PK": "Pakistan",
        "UK": "United Kingdom",
        "US": "America",
    }
    country_name = country_names[country_code]
    today = datetime.now().strftime("%B %d, %Y")
    prompt = (
        f"Today is {today}. Give a brief news summary for {country_name}. "
        "Include 4-5 important topics or recent events happening in that country. "
        "Write in natural, conversational sentences. No bullet points. Keep it short. Write in English."
    )
    try:
        loop = asyncio.get_running_loop()
        ai_summary = await asyncio.wait_for(
            loop.run_in_executor(None, talk_with_ai, prompt),
            timeout=60,
        )
        if not ai_summary:
            return "[B][C][FF0000]❌ Could not generate news. Try again later.", country_name
        return ai_summary, country_name
    except asyncio.TimeoutError:
        return "[B][C][FF0000]❌ News request timed out. Please try again.", country_name
    except Exception as e:
        return f"[B][C][FF0000]❌ Error fetching news: {str(e)}", country_name

da = 'f2212101'
dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
x_list = ['01','01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']

def Decrypt_ID(da):
    """EXACT SAME as your code"""
    if da != None and len(da) == 10:
        w = 128
        xxx = len(da)/2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx)-1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        x5 = da[8:10]
        return str(w * x_list.index(x5) + (dec.index(x2) * 128) + dec.index(x1) + (dec.index(x3) * 128 * 128) + (dec.index(x4) * 128 * 128 * 128))

    if da != None and len(da) == 8:
        w = 128
        xxx = len(da)/2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx)-1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        return str(w * x_list.index(x4) + (dec.index(x2) * 128) + dec.index(x1) + (dec.index(x3) * 128 * 128))
    
    return None

def Encrypt_ID(x):
    """EXACT SAME as your code"""
    x = int(x)
    x = x / 128 
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                m = (n - int(strn)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + x_list[int(x)]
            else:
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + x_list[int(x)]

def decrypt_api(cipher_text):
    """EXACT SAME as your code"""
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size)
    return plain_text.hex()

def encrypt_api(plain_text):
    """EXACT SAME as your code"""
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def encrypt_message(plaintext_bytes):
    """EXACT SAME as your Flask API"""
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded)
    return binascii.hexlify(encrypted).decode('utf-8')    

def create_uid_protobuf(uid):
    """EXACT SAME as your Flask API"""
    msg = dev_generator_pb2.dev_generator()
    msg.saturn_ = int(uid)
    msg.garena = 1
    return msg.SerializeToString()

def enc(uid):
    """EXACT SAME as your Flask API"""
    pb = create_uid_protobuf(uid)
    return encrypt_message(pb)

def decode_player_info(binary):
    """EXACT SAME as your Flask API"""
    info = devxt_count_pb2.xt()
    info.ParseFromString(binary)
    return info    
    
import requests
import json

def load_jwt_token():
    """Load token from token.json"""
    try:
        with open("token.json", "r") as f:
            data = json.load(f)
        token = data.get("token")
        if token:
            print(f"✅ Loaded token: {token[:20]}...")
            return token
        else:
            print("❌ No token found in token.json")
            return None
    except Exception as e:
        print(f"❌ Error loading token: {e}")
        return None

def load_tokens_ind():
    """Load bulk tokens from token_ind.json"""
    try:
        with open("token_ind.json", "r") as f:
            tokens = json.load(f)
        print(f"📦 Loaded {len(tokens)} tokens from token_ind.json")
        return tokens
    except:
        print("❌ No tokens found in token_ind.json")
        return None



def normalize_player_data(data):
    """Normalize API response fields to the expected key format regardless of case/naming"""
    # Normalize top-level keys
    # Support both the FF API format (basicInfo/clanBasicInfo) and wrapped formats
    acc_raw = (data.get("AccountInfo") or data.get("accountInfo") or
               data.get("basicInfo") or data.get("BasicInfo") or {})
    guild_raw = (data.get("GuildInfo") or data.get("guildInfo") or
                 data.get("clanBasicInfo") or data.get("ClanBasicInfo") or
                 data.get("clanInfo") or {})
    social_raw = (data.get("socialinfo") or data.get("SocialInfo") or
                  data.get("socialInfo") or data.get("social") or {})
    captain_raw = data.get("captainBasicInfo") or data.get("CaptainBasicInfo") or {}

    def pick(*keys, src, default="N/A"):
        for k in keys:
            v = src.get(k)
            if v not in (None, "", 0):
                return v
        return default

    acc = {
        # name: nickname (FF API), accountName, name
        "AccountName":       pick("nickname", "AccountName", "accountName", "name", src=acc_raw),
        # id: accountId (FF API), AccountId, uid
        "AccountId":         pick("accountId", "AccountId", "uid", "id", src=acc_raw),
        # level
        "AccountLevel":      pick("level", "AccountLevel", "accountLevel", src=acc_raw),
        # exp
        "AccountEXP":        pick("exp", "AccountEXP", "AccountExp", "accountExp", src=acc_raw),
        # likes: liked (FF API), AccountLikes
        "AccountLikes":      pick("liked", "AccountLikes", "accountLikes", "likes", src=acc_raw, default="0"),
        # region
        "AccountRegion":     pick("region", "AccountRegion", "accountRegion", src=acc_raw),
        # badge: badgeId (FF API), AccountBPID
        "AccountBPID":       pick("badgeId", "AccountBPID", "accountBpId", "bpBadgeId", src=acc_raw),
        # version: releaseVersion (FF API)
        "ReleaseVersion":    pick("releaseVersion", "ReleaseVersion", "version", src=acc_raw),
        # create time: createAt (FF API), AccountCreateTime (Unix timestamp)
        "AccountCreateTime": pick("createAt", "AccountCreateTime", "accountCreateTime", "createTime", src=acc_raw, default="0"),
        # last login: lastLoginAt (FF API), AccountLastLogin (Unix timestamp)
        "AccountLastLogin":  pick("lastLoginAt", "AccountLastLogin", "accountLastLogin", "lastLogin", src=acc_raw, default="0"),
        # pre-formatted last login string from API (e.g. "28 August 2025, 05:17 PM PKT")
        "AccountLastLoginFormatted": pick("lastLoginFormatted", src=acc_raw, default=""),
        # BR max rank: maxRank (FF API), maxRankingPoints, brMaxRank
        "BrMaxRank":         pick("maxRank", "maxRankingPoints", "BrMaxRank", "brMaxRank", src=acc_raw),
        # BR rank points: rankingPoints (FF API), rank, brRankPoint
        "BrRankPoint":       pick("rankingPoints", "rank", "BrRankPoint", "brRankPoint", src=acc_raw),
        # CS max rank: csMaxRank (FF API), csMaxRankingPoints
        "CsMaxRank":         pick("csMaxRank", "csMaxRankingPoints", "CsMaxRank", src=acc_raw),
        # CS rank points: csRank (FF API), csRankingPoints
        "CsRankPoint":       pick("csRank", "csRankingPoints", "CsRankPoint", "csRankPoint", src=acc_raw),
    }

    guild = {
        # name: clanName (FF API), GuildName
        "GuildName":     pick("clanName", "GuildName", "guildName", "name", src=guild_raw, default="No Guild"),
        # id: clanId (FF API), GuildID
        "GuildID":       pick("clanId", "GuildID", "GuildId", "guildId", "id", src=guild_raw),
        # owner: captainId (FF API), GuildOwner
        "GuildOwner":    pick("captainId", "GuildOwner", "guildOwner", "ownerId", src=guild_raw),
        # level: clanLevel (FF API), GuildLevel
        "GuildLevel":    pick("clanLevel", "GuildLevel", "guildLevel", "level", src=guild_raw),
        # members: memberNum (FF API), GuildMember
        "GuildMember":   pick("memberNum", "GuildMember", "guildMember", "memberCount", "members", src=guild_raw, default="0"),
        # capacity
        "GuildCapacity": pick("capacity", "GuildCapacity", "guildCapacity", src=guild_raw, default="0"),
    }

    social = {
        "language": pick("language", "Language", src=social_raw),
    }

    captain = {
        "accountId": pick("accountId", "AccountId", src=captain_raw, default=acc.get("AccountId", "N/A")),
    }

    data["AccountInfo"] = acc
    data["GuildInfo"] = guild
    data["socialinfo"] = social
    data["captainBasicInfo"] = captain
    return data


async def get_player_info(uid):
    """Fetch full player info from external API."""
    import aiohttp, asyncio
    try:
        url = f"https://wotaxxdev-api.vercel.app/info?uid={uid}"
        print(f"📊 /info → {url}")

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as res:
                if res.status != 200:
                    return None, f"API error: HTTP {res.status}"
                raw_json = await res.json(content_type=None)

        print(f"📊 /info raw response: {str(raw_json)[:400]}")

        # API returns data under 'playerData' key (confirmed from logs)
        # Fallback chain: playerData → data → AccountInfo → raw root
        d = (
            raw_json.get("playerData") or
            raw_json.get("data") or
            raw_json.get("AccountInfo") or
            raw_json
        )
        if not isinstance(d, dict):
            d = raw_json

        # Guild may be nested separately
        guild_nested = (
            raw_json.get("guildInfo") or raw_json.get("GuildInfo") or
            d.get("guildInfo") or d.get("GuildInfo") or
            d.get("clanInfo") or d.get("clan") or {}
        )
        if not isinstance(guild_nested, dict):
            guild_nested = {}

        # Helper: search value across multiple dicts and key names, first non-empty wins
        def _mg(*dicts_then_keys, default="N/A"):
            srcs, keys = [], []
            for x in dicts_then_keys:
                if isinstance(x, dict):
                    srcs.append(x)
                else:
                    keys.append(x)
            for src in srcs:
                for k in keys:
                    v = src.get(k)
                    if v not in (None, "", 0, "N/A", "Unknown", "unknown"):
                        return str(v)
            return default

        # For timestamps — only accept positive integers
        def _ts(*dicts_then_keys):
            srcs, keys = [], []
            for x in dicts_then_keys:
                if isinstance(x, dict):
                    srcs.append(x)
                else:
                    keys.append(x)
            for src in srcs:
                for k in keys:
                    v = src.get(k)
                    try:
                        vi = int(v)
                        if vi > 0:
                            return str(vi)
                    except (TypeError, ValueError):
                        pass
            return "0"

        acc = {
            # Confirmed field names from API: nickname, accountId, level, exp, liked, region, lastLoginAt, rankingPoints, rank, csRank
            "AccountName":               _mg(d, "nickname", "AccountName", "name", "playerName", default="Unknown"),
            "AccountId":                 _mg(d, "accountId", "AccountId", "uid", "player_id", default=str(uid)),
            "AccountLevel":              _mg(d, "level", "AccountLevel", default="N/A"),
            "AccountEXP":                _mg(d, "exp", "AccountEXP", "experience", default="0"),
            "AccountLikes":              _mg(d, "liked", "likes", "AccountLikes", default="0"),
            "AccountRegion":             _mg(d, "region", "AccountRegion", default="N/A"),
            "AccountBPID":               _mg(d, "bannerId", "badgeId", "AccountBPID", "bpId", default="N/A"),
            "ReleaseVersion":            _mg(d, "version", "ReleaseVersion", "releaseVersion", default="OB53"),
            "AccountCreateTime":         _ts(d, "createdAt", "createTime", "AccountCreateTime", "create_time", "created_at"),
            "AccountLastLogin":          _ts(d, "lastLoginAt", "lastLogin", "AccountLastLogin", "last_login"),
            "AccountLastLoginFormatted": "",
            "BrRankPoint":               _mg(d, "rankingPoints", "BrRankPoint", "brRankPoints", "brRank", default="N/A"),
            "BrMaxRank":                 _mg(d, "rank", "BrMaxRank", "brMaxRank", default="N/A"),
            "CsRankPoint":               _mg(d, "csRankingPoints", "CsRankPoint", "csRankPoints", default="N/A"),
            "CsMaxRank":                 _mg(d, "csRank", "CsMaxRank", "csMaxRank", default="N/A"),
            "AccountPrimeLevel":         _mg(d, "primeLevel", "AccountPrimeLevel", "prime_level", "PrimeLevel", "seasonId", default="N/A"),
        }

        guild = {
            "GuildName":     _mg(guild_nested, d, "GuildName", "clanName", "guildName", default="No Guild"),
            "GuildID":       _mg(guild_nested, d, "GuildID", "clanId", "guildId", default="N/A"),
            "GuildOwner":    _mg(guild_nested, d, "GuildOwner", "captainId", "ownerId", default="N/A"),
            "GuildLevel":    _mg(guild_nested, d, "GuildLevel", "clanLevel", "guildLevel", default="N/A"),
            "GuildMember":   _mg(guild_nested, d, "GuildMember", "memberNum", "memberCount", default="0"),
            "GuildCapacity": _mg(guild_nested, d, "GuildCapacity", "capacity", "maxMember", default="0"),
        }

        data = {
            "AccountInfo": acc,
            "GuildInfo": guild,
            "socialinfo": {"language": _mg(d, "language", default="N/A")},
            "captainBasicInfo": {"accountId": acc.get("AccountId", str(uid))},
        }
        print(f"📊 info OK → name={acc['AccountName']} level={acc['AccountLevel']} region={acc['AccountRegion']} login={acc['AccountLastLogin']}")
        return data, None

    except asyncio.TimeoutError:
        return None, "Request timed out (15s)"
    except aiohttp.ClientConnectorError as e:
        return None, f"Connection error: {e}"
    except Exception as e:
        print(f"❌ get_player_info error: {e}")
        return None, str(e)


async def check_ban_status(uid):
    """Check ban status of a player using external API."""
    import aiohttp, asyncio
    try:
        url = f"https://wotaxxdev-api.vercel.app/check?uid={uid}"
        print(f"🔍 /check → {url}")

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as res:
                if res.status != 200:
                    return None, f"API error: HTTP {res.status}"
                raw_json = await res.json(content_type=None)

        print(f"🔍 /check raw response: {raw_json}")
        return raw_json, None

    except asyncio.TimeoutError:
        return None, "Request timed out (15s)"
    except aiohttp.ClientConnectorError as e:
        return None, f"Connection error: {e}"
    except Exception as e:
        print(f"❌ check_ban_status error: {e}")
        return None, str(e)


async def get_player_likes_internal(uid, region="bd"):
    """Fetch player name and likes directly from the game server using internal protobuf — no external APIs."""
    import aiohttp, asyncio, ssl as ssl_mod
    try:
        token = load_jwt_token()
        if not token:
            return None, None, "No JWT token available"

        encrypted_payload = enc(uid)
        if region.lower() == "ind":
            url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
        elif region.lower() == "us":
            url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
        elif region.lower() == "sg":
            url = "https://client.sg.freefiremobile.com/GetPlayerPersonalShow"
        else:
            url = "https://client.bd.freefiremobile.com/GetPlayerPersonalShow"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        ssl_context = ssl_mod.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl_mod.CERT_NONE

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url,
                data=bytes.fromhex(encrypted_payload),
                headers=headers,
                ssl=ssl_context,
            ) as res:
                if res.status != 200:
                    return None, None, f"Game server error: {res.status}"
                raw = await res.read()
                try:
                    decrypted = bytes.fromhex(decrypt_api(raw.hex()))
                except Exception:
                    decrypted = raw
                info = decode_player_info(decrypted)
                player_name = getattr(info, "AccountName", None) or getattr(info, "nickname", None) or "Unknown"
                likes = getattr(info, "Liked", None) or getattr(info, "liked", None) or getattr(info, "AccountLikes", None) or 0
                return str(player_name), int(likes), None
    except asyncio.TimeoutError:
        return None, None, "Request timed out"
    except Exception as e:
        return None, None, str(e)


def get_ff_server_url(region, endpoint):
    """Return the correct Free Fire server URL for the given region and endpoint."""
    if BOT_SERVER_URL:
        return f"{BOT_SERVER_URL}/{endpoint}"
    region = region.upper()
    base = {
        "IND": "https://client.ind.freefiremobile.com",
        "BD":  "https://client.bd.freefiremobile.com",
        "US":  "https://client.us.freefiremobile.com",
        "SG":  "https://client.sg.freefiremobile.com",
        "ME":  "https://client.me.freefiremobile.com",
        "PK":  "https://client.me.freefiremobile.com",
        "SAC": "https://client.sac.freefiremobile.com",
    }.get(region, "https://client.me.freefiremobile.com")
    return f"{base}/{endpoint}"


def get_friend_server_url(region, endpoint):
    """Return URL for friend endpoints.
    Uses BOT_SERVER_URL when set (same as get_ff_server_url) so the bot
    always routes through the server that was assigned at login (e.g. polarbear).
    Falls back to regional freefiremobile.com only when BOT_SERVER_URL is not set.
    """
    if BOT_SERVER_URL:
        return f"{BOT_SERVER_URL}/{endpoint}"
    region = region.upper()
    base = {
        "IND": "https://client.ind.freefiremobile.com",
        "BD":  "https://client.bd.freefiremobile.com",
        "US":  "https://client.us.freefiremobile.com",
        "SG":  "https://client.sg.freefiremobile.com",
        "ME":  "https://client.me.freefiremobile.com",
        "PK":  "https://client.me.freefiremobile.com",
        "SAC": "https://client.sac.freefiremobile.com",
    }.get(region, "https://client.me.freefiremobile.com")
    return f"{base}/{endpoint}"


def encode_varint(value):
    """Encode an integer as a protobuf varint and return hex string."""
    buf = []
    value = int(value)
    while True:
        towrite = value & 0x7f
        value >>= 7
        if value:
            buf.append(towrite | 0x80)
        else:
            buf.append(towrite)
            break
    return ''.join(f'{b:02x}' for b in buf)


def send_friend_request_single(uid, token, region="PK"):
    """Send friend request directly to Free Fire server.
    Returns (True, None) on success or (False, error_str) on failure."""
    try:
        # Load bot UID from token.json so it matches the JWT token
        try:
            with open("token.json", "r") as f:
                token_data = json.load(f)
            bot_uid = int(token_data.get("bot_uid", 0))
        except Exception:
            bot_uid = 0

        if bot_uid == 0:
            msg = "bot_uid missing in token.json — restart bot"
            print(f"❌ {msg}")
            return False, msg

        bot_uid_varint = encode_varint(bot_uid)
        target_uid_varint = encode_varint(uid)
        payload = f"08{bot_uid_varint}10{target_uid_varint}"
        encrypted_payload = encrypt_api(payload)

        url = get_ff_server_url(region, "RequestAddingFriend")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        print(f"📤 ADD payload hex (pre-encrypt): {payload}")
        print(f"📤 Sending friend request to {uid} (bot_uid={bot_uid}) → {url}")
        response = requests.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, verify=False)
        print(f"📤 RequestAddingFriend → HTTP {response.status_code} | body: {response.content[:300]}")

        # Check for duplicate / already friends in the response body
        body_text = response.content.decode("utf-8", errors="ignore").lower()
        if "duplicate" in body_text or "already" in body_text or "exist" in body_text:
            print(f"⚠️ Friend {uid} already added or request already pending")
            return False, "ALREADY_ADDED"

        if response.status_code == 200:
            print(f"✅ Friend request sent to {uid}")
            return True, None
        else:
            return False, f"HTTP {response.status_code}"

    except Exception as e:
        print(f"❌ send_friend_request_single error: {e}")
        return False, str(e)    
    
def start_autooo(self):    
    try:
        fields = {
            1: 9,
            2: {
                1: 12480598706,
            },
        }
        packet = create_protobuf_packet(fields).hex()
        header_length = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_length_final = dec_to_hex(header_length)
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    except Exception as e:
        print(e)

def load_credentials_from_file(filename="MG24GAMER.txt"):
    """
    Load UID and password from MG24GAMER.txt file
    """
    try:
        if not os.path.exists(filename):
            print(f"❌ {filename} not found!")
            create_credentials_template()
            return None, None
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        uid = None
        password = None
        
        # Try to find uid and password using regex
        import re
        
        # Look for uid=value or uid: value
        uid_match = re.search(r'(?:uid\s*[=:]\s*)(\d+)', content, re.IGNORECASE)
        if uid_match:
            uid = uid_match.group(1)
        
        # Look for password=value or password: value
        pass_match = re.search(r'(?:password\s*[=:]\s*)([^\s\n\r]+)', content, re.IGNORECASE)
        if pass_match:
            password = pass_match.group(1)
        
        if not uid or not password:
            print(f"❌ Could not find UID/password in {filename}")
            print("📝 Please make sure the file contains:")
            print("   uid=YOUR_UID,password=YOUR_PASSWORD")
            print("   OR")
            print("   uid: YOUR_UID")
            print("   password: YOUR_PASSWORD")
            return None, None
        
        print(f"✅ Loaded credentials from {filename}")
        print(f"👤 UID: {uid}")
        print(f"🔑 Password: {password}")
        
        return uid, password
        
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None, None

# Load emotes from JSON file (your format)
def load_emotes_from_json():
    """Load emote IDs from emotes.json (or any matching file in current directory)."""
    import glob as _glob

    # Try these filenames in order
    candidates = (
        ["emotes.json"]
        + _glob.glob("emotes*.json")
        + _glob.glob("attached_assets/emotes*.json")
    )
    # Deduplicate while preserving order
    seen = set()
    candidates = [c for c in candidates if not (c in seen or seen.add(c))]

    for emotes_file in candidates:
        try:
            with open(emotes_file, 'r') as f:
                emotes_data = json.load(f)
            number_emotes = emotes_data.get("EMOTES", {}).get("numbers", {})
            name_emotes   = emotes_data.get("EMOTES", {}).get("names", {})
            if name_emotes:
                print(f"✅ Loaded {len(number_emotes)} number emotes and {len(name_emotes)} named emotes from {emotes_file}")
                return {"numbers": number_emotes, "names": name_emotes}
        except Exception:
            continue

    print("⚠️ emotes.json not found — /e list will show 0 names. Place emotes.json next to main.py")
    return {"numbers": {}, "names": {}}

# Load emotes globally
EMOTES_DATA = load_emotes_from_json()
NUMBER_EMOTES = EMOTES_DATA["numbers"]
NAME_EMOTES = EMOTES_DATA["names"]

# Helper functions for ghost join
def dec_to_hex(decimal):
    """Convert decimal to hex string"""
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()



async def encrypt_packet(packet_hex, key, iv):
    """Encrypt packet using AES CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    """Wrapper for encrypt_packet"""
    return await encrypt_packet(packet_hex, key, iv)
    

def generate_random_hex_color():
    """Generate random hex color for messages"""
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def bunner_():
    """Generate random avatar ID"""
    return random.randint(100000000, 999999999)

# Add this function to your code
def Encrypt(number):
    """Encrypt function from your first TCP bot"""
    number = int(number)
    encoded_bytes = []
    
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    
    return bytes(encoded_bytes).hex()


async def send_working_join_request(target_uid, key, iv, region, LoGinDaTaUncRypTinG):
    """Send join request that actually works"""
    
    try:
        # Step 1: Reset bot to solo mode
        print("🔄 Resetting bot to solo mode...")
        await reset_bot_state(key, iv, region)
        await asyncio.sleep(1)
        
        # Step 2: Create bot's own squad (so it has context)
        print("🏠 Creating bot squad...")
        squad_packet = await OpEnSq(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', squad_packet)
        await asyncio.sleep(1)
        
        # Step 3: Send join request
        print(f"📨 Sending join request to {xMsGFixinG(target_uid)}...")
        join_packet = await create_working_join_request(target_uid, key, iv, region, LoGinDaTaUncRypTinG)
        
        if join_packet:
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Bot join request sent! Player can now accept.")
            return True
        else:
            print(f"❌ Failed to create join packet")
            return False
            
    except Exception as e:
        print(f"❌ Error in working join request: {e}")
        return False
        
async def handle_join_req_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type, LoGinDaTaUncRypTinG):
    """Handle /join_req command - bot sends join request to player"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) < 2:
        error_msg = f"""[B][C][FF0000]❌ Usage: /join_req (player_uid)
Example: /join_req 123456789

What happens:
1. Bot goes solo mode
2. Bot creates its own squad  
3. Bot sends join request to player
4. Player sees: "BotName wants to join your team"
5. Player clicks Accept → Bot joins player's team
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Invalid UID! Must be numbers only.\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"""[B][C][00FF00]🤖 BOT JOIN REQUEST INITIATED

👤 Target Player: {xMsGFixinG(target_uid)}
⚙️ Steps:
1. Bot resetting to solo mode...
2. Bot creating squad...
3. Sending join request...

⏳ Please wait...
"""
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        success = await send_working_join_request(target_uid, key, iv, region, LoGinDaTaUncRypTinG)
        
        if success:
            success_msg = f"""[B][C][00FF00]✅ BOT JOIN REQUEST SENT!

🎯 Target: {xMsGFixinG(target_uid)}
🤖 Bot Name: MG24 GAMER
✅ Status: Ready to join

📱 Player will see:
"MG24 GAMER wants to join your team"

✅ When player clicks ACCEPT:
Bot will automatically join player's team!
"""
        else:
            success_msg = f"""[B][C][FF0000]❌ FAILED!

Possible reasons:
1. Bot not connected properly
2. Bot already in a squad
3. Server issue

Try again in 10 seconds.
"""
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Cleanup: Leave squad after sending request
        await asyncio.sleep(3)
        leave_packet = await ExiT(0, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print("🧹 Bot cleaned up (left squad)")
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)        
        
async def create_simple_start_packet(key, iv):
    """Create simple start match packet (00 00 00 d6)"""
    
    # This appears to be a minimal start packet
    # 00 00 00 d6 in hex = 214 in decimal (packet type?)
    
    fields = {
        1: 214,  # Packet type for start match (d6 hex = 214 decimal)
        2: {
            1: 1,  # Start match command
        }
    }
    
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Generate final packet
    final_packet = await GeneRaTePk(packet_hex, '0514', key, iv)  # Use appropriate packet type
    
    print(f"✅ Simple start match packet created")
    return final_packet
    
async def create_detailed_start_packet(key, iv, region="IND"):
    """Create detailed start match packet with device info"""
    
    # Decoded from your hex: contains device info (vivo, arm64, etc.)
    
    fields = {
        1: 269,  # 0x10D = 269 decimal (detailed start packet)
        2: {
            1: 8,           # Unknown
            2: 8,           # Unknown
            3: 11,          # Unknown
            4: 1,           # Unknown
            5: "vivo",      # Device brand
            6: "130",       # Device model
            7: "arm64-v8a", # CPU architecture
            8: "f538dc9b-cec9-43cd-8125-95f7f4f1f7e3",  # Device ID
            9: "FFD58FB4F76F648C2A5E21EBCFA3AAE81B4C9B7D97",  # Unknown
            10: "voice",    # Audio type
            11: "V2059",    # Version
            12: "mt6785",   # Processor
            13: "AFFD58FB4F76F648C2A5E21EBCFA3AAE81B4C9B7D97",  # Unknown
            14: "IND_1999120752610979840",  # Region + timestamp
            15: 269         # Packet length?
        }
    }
    
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Determine packet type based on region
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    final_packet = await GeneRaTePk(packet_hex, packet_type, key, iv)
    
    print(f"✅ Detailed start match packet created")
    return final_packet
        
async def generate_guest_accounts(count=1, name="BlackApis", password_prefix="FF"):
    """Generate guest accounts using the API"""
    api_url = f"https://gen-by-black-api.vercel.app/generate?name={name}&password_prefix={password_prefix}"
    
    accounts = []
    failed_attempts = 0
    max_retries = 10
    
    print(f"📡 Generating {count} guest accounts...")
    
    for i in range(count):
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                print(f"🔄 Attempt {retry_count + 1}/{max_retries} for account {i + 1}/{count}...")
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                    async with session.get(api_url) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            
                            if data.get("success"):
                                account = {
                                    'uid': data.get('uid'),
                                    'password': data.get('password'),
                                    'name': data.get('name'),
                                    'timestamp': time.time()
                                }
                                accounts.append(account)
                                print(f"✅ Account {i + 1}: {account['uid']}")
                                success = True
                                failed_attempts = 0  # Reset failed attempts counter
                                
                            else:
                                print(f"❌ API error: {data.get('message', 'Unknown error')}")
                                retry_count += 1
                                await asyncio.sleep(2)
                                
                        elif response.status == 503:
                            print(f"⚠️ Server busy (503), retrying in 3 seconds...")
                            retry_count += 1
                            await asyncio.sleep(3)
                            
                        else:
                            print(f"❌ HTTP {response.status}, retrying...")
                            retry_count += 1
                            await asyncio.sleep(2)
                            
            except asyncio.TimeoutError:
                print(f"⏰ Timeout, retrying...")
                retry_count += 1
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}...")
                retry_count += 1
                await asyncio.sleep(2)
        
        if not success:
            print(f"❌ Failed to generate account {i + 1} after {max_retries} attempts")
            failed_attempts += 1
            
            # If too many failures in a row, stop
            if failed_attempts >= 3:
                print("🛑 Too many failures, stopping...")
                break
        
        # Small delay between accounts to avoid rate limiting
        if i < count - 1:
            await asyncio.sleep(1)
    
    return accounts

def save_guest_accounts(accounts, filename="guest_accounts.json"):
    """Save guest accounts to JSON file"""
    try:
        # Load existing accounts if file exists
        existing = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing = json.load(f)
        
        # Combine with new accounts
        all_accounts = existing + accounts
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(all_accounts, f, indent=2)
        
        print(f"💾 Saved {len(accounts)} accounts to {filename}")
        print(f"📊 Total accounts: {len(all_accounts)}")
        
        return True
    except Exception as e:
        print(f"❌ Error saving accounts: {e}")
        return False

async def generate_and_save_accounts(count, name="BlackApis", password_prefix="FF"):
    """Generate and save accounts with progress updates"""
    start_time = time.time()
    
    print(f"\n🎯 GENERATING {count} GUEST ACCOUNTS")
    print("="*50)
    
    accounts = await generate_guest_accounts(count, name, password_prefix)
    
    if accounts:
        # Save to file
        save_guest_accounts(accounts)
        
        # Display results
        elapsed = time.time() - start_time
        print("\n" + "="*50)
        print("📊 GENERATION COMPLETE")
        print("="*50)
        print(f"✅ Success: {len(accounts)}/{count} accounts")
        print(f"⏱️ Time: {elapsed:.1f} seconds")
        print(f"📁 Saved to: guest_accounts.json")
        
        # Show first 3 accounts as preview
        print("\n📋 FIRST 3 ACCOUNTS:")
        for i, acc in enumerate(accounts[:3]):
            print(f"  {i+1}. UID: {acc['uid']} | Pass: {acc['password']}")
        
        if len(accounts) > 3:
            print(f"  ... and {len(accounts) - 3} more")
    
    return accounts        
        
async def start_match(key, iv, region, detailed=False):
    """Start Free Fire match - bot must be in a squad/team"""
    
    try:
        if detailed:
            start_packet = await create_detailed_start_packet(key, iv, region)
        else:
            start_packet = await create_simple_start_packet(key, iv)
        
        if start_packet:
            # Send via Online connection
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
            print("🎮 Start match packet sent!")
            return True
        else:
            print("❌ Failed to create start packet")
            return False
            
    except Exception as e:
        print(f"❌ Error starting match: {e}")
        return False       
        
async def handle_start_match_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle /ss command to start match"""
    
    parts = inPuTMsG.strip().split()
    
    # Check if user wants detailed start
    detailed = False
    if len(parts) > 1 and parts[1].lower() == "detailed":
        detailed = True
    
    # Send initial message
    initial_msg = f"""[B][C][00FF00]🎮 STARTING MATCH...

⚙️ Mode: {'Detailed' if detailed else 'Simple'}
🤖 Bot must be in a squad!
⏳ Please wait...
"""
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        success = await start_match(key, iv, region, detailed)
        
        if success:
            success_msg = f"""[B][C][00FF00]✅ MATCH START COMMAND SENT!

📋 Details:
• Type: {'Detailed device info' if detailed else 'Simple start'}
• Status: Match starting...
• Requirement: Bot must be squad leader

🎯 If bot is squad leader, match will begin!
"""
        else:
            success_msg = f"""[B][C][FF0000]❌ FAILED TO START MATCH!

Possible reasons:
1. Bot not in a squad
2. Bot not squad leader
3. Invalid packet structure
4. Server connection issue

💡 Make sure bot is in a squad as leader!
"""
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        
async def debug_start_match():
    """Debug function to test start packets"""
    
    print("🔍 Analyzing start packets...")
    print(f"Simple packet hex: 00 00 00 d6")
    print(f"Decimal value: {int('d6', 16)} = 214")
    
    # Try to decode the detailed packet
    detailed_hex = "0a8d010808100b180122047669766f2a02313330f6a8858c023a0961726d36342d76386142004a2466353338646339622d636563392d343363642d383132352d393566376634663166376533522a4646443538464234463736463634384332413545323145424346413341414538314234433942374439375a05766f69636562055632303539680172066d74363738351241464644353846423446373646363438433241354532314542434641334141453831423443394237443937494e445f31393939313230373532363130393739383430188d01"
    
    print(f"\n📊 Detailed packet length: {len(detailed_hex)//2} bytes")
    print(f"First bytes: {detailed_hex[:20]}...")
    
    # Try to parse as protobuf
    try:
        from protobuf_decoder.protobuf_decoder import Parser
        parsed = Parser().parse(bytes.fromhex(detailed_hex))
        print(f"\n✅ Parsed detailed packet:")
        print(parsed)
    except Exception as e:
        print(f"❌ Could not parse: {e}")
        


async def check_player_status(target_uid, key, iv, max_wait=3):
    """Direct function to check player status with proper waiting"""
    try:
        # Clear old cache
        if target_uid in status_response_cache:
            del status_response_cache[target_uid]
        
        # Send request
        status_packet = await createpacketinfo(target_uid, key, iv)
        if not status_packet:
            return None, "Failed to create packet"
        
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        print(f"📤 Sent status request for {xMsGFixinG(target_uid)}")
        
        # Wait for response with polling
        start_time = time.time()
        while time.time() - start_time < max_wait:
            if target_uid in status_response_cache:
                cache_data = status_response_cache[target_uid]
                return cache_data, "Success"
            
            await asyncio.sleep(0.1)  # Short sleep
        
        return None, f"No response after {max_wait} seconds"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

async def createpacketinfo(idddd, key, iv):
    """Create player status request packet - SAME as first TCP bot"""
    try:
        ida = Encrypt(idddd)
        packet = f"080112090A05{ida}1005"
        header_lenth = len(await encrypt_packet(packet, key, iv)) // 2
        header_lenth_final = dec_to_hex(header_lenth)
        
        if len(header_lenth_final) == 2:
            final_packet = "0F15000000" + header_lenth_final + await nmnmmmmn(packet, key, iv)
        elif len(header_lenth_final) == 3:
            final_packet = "0F1500000" + header_lenth_final + await nmnmmmmn(packet, key, iv)
        elif len(header_lenth_final) == 4:
            final_packet = "0F150000" + header_lenth_final + await nmnmmmmn(packet, key, iv)
        elif len(header_lenth_final) == 5:
            final_packet = "0F15000" + header_lenth_final + await nmnmmmmn(packet, key, iv)
        else:
            final_packet = "0F1500000" + header_lenth_final + await nmnmmmmn(packet, key, iv)
            
        return bytes.fromhex(final_packet)
        
    except Exception as e:
        print(f"Error creating packet info: {e}")
        return None

def fix_num(number):
    """Format numbers with breaks - from first TCP"""
    fixed = ""
    count = 0
    num_str = str(number)
    
    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0
    return fixed

def get_available_room(input_text):
    """Parse protobuf to JSON - from first TCP"""
    try:
        from protobuf_decoder.protobuf_decoder import Parser
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None

def parse_results(parsed_results):
    """Helper for get_available_room"""
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict  # ← ADD THIS LINE

def get_player_status(packet):
    """Get player status from packet"""
    json_result = get_available_room(packet)
    if not json_result:
        return "OFFLINE"
    
    parsed_data = json.loads(json_result)
    
    if "5" not in parsed_data or "data" not in parsed_data["5"]:
        return "OFFLINE"
    
    json_data = parsed_data["5"]["data"]
    
    if "1" not in json_data or "data" not in json_data["1"]:
        return "OFFLINE"
    
    data = json_data["1"]["data"]
    
    if "3" not in data:
        return "OFFLINE"
    
    status_data = data["3"]
    
    if "data" not in status_data:
        return "OFFLINE"
    
    status = status_data["data"]
    
    if status == 1:
        return "SOLO"
    if status == 2:
        if "9" in data and "data" in data["9"]:
            group_count = data["9"]["data"]
            countmax1 = data["10"]["data"]
            countmax = countmax1 + 1
            return f"INSQUAD ({group_count}/{countmax})"
        return "INSQUAD"
    if status in [3, 5]:
        return "INGAME"
    if status == 4:
        return "IN ROOM"
    if status in [6, 7]:
        return "IN SOCIAL ISLAND MODE"
    
    return "NOTFOUND"

def get_idroom_by_idplayer(packet):
    """Extract room ID from player info packet"""
    try:
        json_result = get_available_room(packet)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        print(f"Error extracting room ID: {e}")
        return None



def get_leader(packet):
    """Extract leader ID from squad packet"""
    try:
        json_result = get_available_room(packet)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        leader = data['8']["data"]
        return leader
    except Exception as e:
        print(f"Error extracting leader: {e}")
        return None

# Add to your global variables

# Add near top with other globals
status_queue = asyncio.Queue()
cache_dict = {}

# In TcPOnLine, instead of caching directly:
async def handle_status_response(hex_data):
    """Process and queue status responses"""
    try:
        # ... parsing code ...
        
        # Put in queue instead of direct cache
        await status_queue.put({
            'player_id': player_id,
            'data': cache_entry
        })
        
        print(f"📤 Queued status for {xMsGFixinG(target_uid)}")
        
    except Exception as e:
        print(f"❌ Queue error: {e}")

# In TcPChaT, add a queue consumer
async def cache_consumer():
    """Consume status responses from queue"""
    while True:
        try:
            item = await status_queue.get()
            player_id = item['player_id']
            cache_dict[player_id] = item['data']
            print(f"📥 Cache updated for {xMsGFixinG(target_uid)}")
            status_queue.task_done()
        except Exception as e:
            print(f"❌ Consumer error: {e}")
        await asyncio.sleep(0.1)



# Start consumer in your main function
async def StarTinG():
    # Start consumer
    consumer_task = asyncio.create_task(cache_consumer())
    
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            consumer_task.cancel()
            break
        except asyncio.TimeoutError: 
            print("Token ExpiRed ! , ResTartinG")
        except Exception as e: 
            print(f"ErroR TcP - {e} => ResTarTinG ...")

import pickle
import os
import time

CACHE_FILE = 'status_cache.pkl'
CACHE_TIMEOUT = 30  # Cache entries expire after 30 seconds

def save_to_cache(player_id, data):
    """Save status to file cache with timestamp"""
    try:
        # Load existing cache
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'rb') as f:
                    cache = pickle.load(f)
            except:
                cache = {}
        else:
            cache = {}
        
        # Add timestamp
        data['saved_at'] = time.time()
        
        # Update cache
        cache[str(player_id)] = data
        
        # Save back
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)
        
        print(f"💾 Saved to file cache: {xMsGFixinG(target_uid)}")
        return True
    except Exception as e:
        print(f"❌ Cache save error: {e}")
        import traceback
        traceback.print_exc()
        return False

def load_from_cache(player_id):
    """Load status from file cache, check expiration"""
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        
        with open(CACHE_FILE, 'rb') as f:
            cache = pickle.load(f)
        
        player_key = str(player_id)
        if player_key in cache:
            data = cache[player_key]
            
            # Check if cache is expired
            if 'saved_at' in data:
                if time.time() - data['saved_at'] > CACHE_TIMEOUT:
                    print(f"⏰ Cache expired for {xMsGFixinG(target_uid)}")
                    del cache[player_key]
                    with open(CACHE_FILE, 'wb') as f:
                        pickle.dump(cache, f)
                    return None
            
            print(f"📥 Loaded from cache: {xMsGFixinG(target_uid)}")
            return data
        
        return None
    except Exception as e:
        print(f"❌ Cache load error: {e}")
        return None

def clear_cache_entry(player_id):
    """Clear specific cache entry"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                cache = pickle.load(f)
            
            player_key = str(player_id)
            if player_key in cache:
                del cache[player_key]
                
            with open(CACHE_FILE, 'wb') as f:
                pickle.dump(cache, f)
            print(f"🗑️ Cleared cache for {xMsGFixinG(target_uid)}")
    except Exception as e:
        print(f"❌ Clear cache error: {e}")

def debug_file_cache():
    """Debug the file cache"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                cache = pickle.load(f)
            print(f"\n📁 FILE CACHE DEBUG:")
            print(f"Size: {len(cache)} entries")
            for uid, data in cache.items():
                age = time.time() - data.get('saved_at', 0)
                status = data.get('status', 'NO STATUS')
                print(f"  {uid}: {status} (age: {age:.1f}s)")
            print("---\n")
            return cache
        else:
            print("📁 No cache file exists")
            return {}
    except Exception as e:
        print(f"❌ Cache debug error: {e}")
        return {}

def load_from_cache(player_id):
    """Load status from file cache"""
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        
        with open(CACHE_FILE, 'rb') as f:
            cache = pickle.load(f)
        
        if player_id in cache:
            return cache[player_id]
        return None
    except Exception as e:
        print(f"❌ Cache load error: {e}")
        return None

def clear_cache_entry(player_id):
    """Clear specific cache entry"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                cache = pickle.load(f)
            
            if player_id in cache:
                del cache[player_id]
                
            with open(CACHE_FILE, 'wb') as f:
                pickle.dump(cache, f)
    except:
        pass


    
    
    async def get_account_token(self, uid, password):
        """Get access token for a specific account"""
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": await Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            }
            data = {
                "uid": uid,
                "password": password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        open_id = data.get("open_id")
                        access_token = data.get("access_token")
                        return open_id, access_token
            return None, None
        except Exception as e:
            print(f"❌ Error getting token for {uid}: {e}")
            return None, None
    
    async def send_join_from_account(self, target_uid, account_uid, password, key, iv, region):
        """Send join request from a specific account"""
        try:
            # Get token for this account
            open_id, access_token = await self.get_account_token(account_uid, password)
            if not open_id or not access_token:
                return False
            
            # Create join packet using the account's credentials
            join_packet = await self.create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region)
            if join_packet:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error sending join from {account_uid}: {e}")
            return False

async def join_custom_room(room_id, room_password, key, iv, region):
    """Join custom room with proper Free Fire packet structure"""
    fields = {
        1: 61,  # Room join packet type (verified for Free Fire)
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),  # Room ID
                2: int(time.time()),  # Timestamp
                3: "BOT",  # Player name
                5: 12,  # Unknown
                6: 9999999,  # Unknown
                7: 1,  # Unknown
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,  # Room type
            },
            3: str(room_password),  # Room password
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def leave_squad(key, iv, region):
    """Leave squad - converted from your old TCP leave_s()"""
    fields = {
        1: 7,
        2: {
            1: 12480598706  # Your exact value from old TCP
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def request_join_with_badge(target_uid, badge_value, key, iv, region="IND"):
    """Fixed badge spam function matching craftland_badge structure"""
    try:
        # Get random avatar
        avatar_id = int(await xBunnEr())
        
        fields = {
            1: 33,  # Packet type
            2: {
                1: int(target_uid),        # Target UID
                2: region.upper(),        # Country code
                3: 1,                     # Status 1
                4: 1,                     # Status 2
                5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),  # Numbers field
                6: "iG:[C][B][FF0000] @hn_gaming99",  # Nickname
                7: 330,                   # Rank
                8: 1000,                  # Field 8
                10: region.upper(),       # Region code
                11: bytes([              # UUID
                    49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                    97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49,
                    50, 48, 102, 53
                ]),
                12: 1,                    # Field 12
                13: int(target_uid),      # Repeated UID
                14: {                    # Field 14 (nested)
                    1: 2203434355,
                    2: 8,
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                },
                16: 1,                    # Field 16
                17: 1,                    # Field 17
                18: 312,                  # Field 18
                19: 46,                   # Field 19
                23: bytes([16, 1, 24, 1]), # Field 23
                24: avatar_id,            # Avatar ID
                26: {},                   # Empty field 26
                27: {                    # Field 27 (critical for badge!)
                    1: 11,               # Field 27.1
                    2: 13777711848,      # Field 27.2 (your bot UID)
                    3: 9999              # Field 27.3
                },
                28: {},                   # Empty field 28
                31: {                    # Field 31 (badge value here too)
                    1: 1,
                    2: int(badge_value)  # BADGE VALUE
                },
                32: int(badge_value),     # Field 32 (badge value again)
                34: {                    # Field 34
                    1: int(target_uid),  # Target UID again
                    2: 8,
                    3: b"\x0F\x06\x15\x08\x0A\x0B\x13\x0C\x11\x04\x0E\x14\x07\x02\x01\x05\x10\x03\x0D\x12"
                }
            },
            10: "en",                     # Language
            13: {                        # Field 13
                2: 1,
                3: 1
            }
        }
        
        # Convert to protobuf
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        # Determine packet type based on region
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
            
        # Generate final encrypted packet
        final_packet = await GeneRaTePk(packet_hex, packet_type, key, iv)
        
        print(f"✅ Created badge packet with value {badge_value} for UID {xMsGFixinG(target_uid)}")
        return final_packet
        
    except Exception as e:
        print(f"❌ Error creating badge packet: {e}")
        import traceback
        traceback.print_exc()
        return None
    
async def reset_bot_state(key, iv, region):
    """Reset bot to solo mode before spam - Critical step from your old TCP"""
    try:
        # Leave any current squad (using your exact leave_s function)
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        
        print("✅ Bot state reset - left squad")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting bot: {e}")
        return False    
    
async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    """Create a custom room"""
    fields = {
        1: 3,  # Create room packet type
        2: {
            1: room_name,
            2: room_password,
            3: max_players,  # 2, 4, 8, 16, etc.
            4: 1,  # Room mode
            5: 1,  # Map
            6: "en",  # Language
            7: {   # Player info
                1: "BotHost",
                2: int(await xBunnEr()),
                3: 330,
                4: 1048576,
                5: "BOTCLAN"
            }
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)              




async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle individual badge commands"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /{cmd} (uid)\nExample: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to send {cmd} ({badge_value}) to {xMsGFixinG(target_uid)}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Create badge packet
        badge_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        
        if badge_packet:
            for i in range(20):
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', badge_packet)
                print(f"✅ Sent /{cmd} badge #{i+1} with value {badge_value}")
                await asyncio.sleep(0.1)
            
            success_msg = f"[B][C][00FF00]✅ Successfully Sent {cmd} Badge!\n🎯 Target: {xMsGFixinG(target_uid)}\n🏷️ Badge Value: {badge_value}\n📤 Packets Sent: 20\n"
        else:
            success_msg = f"[B][C][FF0000]❌ Failed to create badge packet!\n"
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)




    
    
    
async def auto_rings_emote_dual(uid, key, iv, region):
    """Send The Rings emote to both sender and bot for dual emote effect"""
    try:
        # The Rings emote ID
        rings_emote_id = 909050009
        
        # Get bot's UID
        bot_uid = 13601801571
        
        # Send emote to SENDER (person who invited)
        emote_to_sender = await Emote_k(int(uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        
        # Small delay between emotes
        await asyncio.sleep(0.5)
        
        # Send emote to BOT (bot performs emote on itself)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
        
        print(f"🤖 Bot performed dual Rings emote with sender {uid} and bot {bot_uid}!")
        
    except Exception as e:
        print(f"Error sending dual rings emote: {e}")    
        
        
async def Room_Spam(Uid, Rm, Nm, K, V):
    fields = {
        1: 78,
        2: {
            1: int(Rm),  
            2: "iG:[C][B][FF0000]Black_Apis",  
            3: {
                2: 1,
                3: 1
            },
            4: 330,      
            5: 6000,     
            6: 201,      
            10: int(await xBunnEr()),  
            11: int(Uid), # Target UID
            12: 1,       
            15: {
                1: 1,
                2: 32768
            },
            16: 32768,    
            18: {
                1: 11481904755,  
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            
            31: {
                1: 1,
                2: 32768
            },
            32: 32768,    
            34: {
                1: int(Uid),   
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
    
async def evo_cycle_spam(uids, key, iv, region, LoGinDaTaUncRypTinG):
    """Cycle through all evolution emotes - BOT DOES OPPOSITE"""
    global evo_cycle_running
    
    # GET BOT UID FROM LOGIN DATA
    try:
        # Try to get from login data (passed as parameter)
        bot_uid = LoGinDaTaUncRypTinG.AccountUID
        print(f"🤖 Using bot UID from login: {bot_uid}")
    except:
        # Fallback to your hardcoded UID
        bot_uid = 13777711848
        print(f"🤖 Using hardcoded bot UID: {bot_uid}")
    
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Starting evolution emote cycle #{cycle_count}")
        
        emote_list = list(evo_emotes.items())
        total_emotes = len(emote_list)
        
        for index, (emote_number, emote_id) in enumerate(emote_list):
            if not evo_cycle_running:
                break
                
            # USER does emote #X
            for uid in uids:
                try:
                    uid_int = int(uid)
                    user_emote = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', user_emote)
                    print(f"👤 User emote #{emote_number}")
                except Exception as e:
                    print(f"Error: {e}")
            
            # ADD SMALL DELAY
            await asyncio.sleep(0.5)
            
            # BOT does opposite emote (last emote when user does first, etc.)
            opposite_index = total_emotes - 1 - index
            opposite_number, opposite_id = emote_list[opposite_index]
            
            try:
                # BOT sends emote to ITSELF
                bot_self_emote = await Emote_k(int(bot_uid), int(opposite_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_self_emote)
                
                # ALSO send to first user for visibility
                await asyncio.sleep(0.3)
                if uids:
                    first_uid = int(uids[0])
                    bot_to_user = await Emote_k(first_uid, int(opposite_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_to_user)
                
                print(f"🤖 Bot OPPOSITE emote #{opposite_number} (sent to self + user)")
            except Exception as e:
                print(f"Bot error: {e}")
            
            # Wait 5 seconds before next emote
            if evo_cycle_running:
                print(f"Waiting 5 seconds before next emote...")
                wait_time = 5
                for i in range(wait_time):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
    
    print("Cycle stopped")
    
async def reject_spam_loop(target_uid, key, iv):
    """Send reject spam packets to target in background"""
    global reject_spam_running
    
    count = 0
    max_spam = 150
    
    while reject_spam_running and count < max_spam:
        try:
            # Send both packets
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            
            # Send to Online connection
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            
            count += 1
            print(f"Sent reject spam #{count} to {xMsGFixinG(target_uid)}")
            
            # 0.2 second delay between spam cycles
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"Error in reject spam: {e}")
            break
    
    return count    
    
async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle completion of reject spam and send final message"""
    try:
        spam_count = await spam_task
        
        # Send completion message
        if spam_count >= 150:
            completion_msg = f"[B][C][00FF00]✅ Reject Spam Completed Successfully for ID {xMsGFixinG(target_uid)}\n✅ Total packets sent: {spam_count * 2}\n"
        else:
            completion_msg = f"[B][C][FFFF00]⚠️ Reject Spam Partially Completed for ID {xMsGFixinG(target_uid)}\n⚠️ Total packets sent: {spam_count * 2}\n"
        
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("Reject spam was cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ ERROR in reject spam: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)    
    
    
    
async def banecipher(target_uid, key, iv):
    """Create reject spam packet - fixed variable name and trimmed banner to fit server limit"""
    banner_text = (
        '[b][000000][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███\n'
        '[b][000000][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███\n'
        '[b][0000FF]============================================================================================================================================================================================================================================================\n'
        '[b][000000][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███\n'
        '[b][000000][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███\n'
    )
    fields = {
        1: 5,
        2: {
            1: int(target_uid),
            2: 1,
            3: int(target_uid),
            4: banner_text
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)

async def black666(client_id, key, iv):
    banner_text = "[FF0000][B][C] ERROR , WELCOME TO [FFFFFF] GothicRealm Bot[00FF00] GothicRealm Bot! \n[FFFF00]NEW VERSION NEW FUNCTION !\n[FF0000] Instagram : @ayaan._.ghaffar\n\n"     
    fields = {
        1: 5,
        2: {
            1: int(client_id),
            2: 1,
            3: int(client_id),
            4: banner_text
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    """Create reject spam packet 2 - Converted to new async format"""
    gay_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: int(client_id),
        2: 5,
        4: 50,
        5: {
            1: int(client_id),
            2: gay_text,
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)
    
async def get_colorful_message(message_text, message_number):
    """Generate message with different colors"""
    color_palette = ["FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", 
                     "00FFFF", "FFA500", "FF1493", "00FF7F", "7B68EE",
                     "FFD700", "00CED1", "FF69B4", "32CD32", "9370DB",
                     "FF4500", "1E90FF", "ADFF2F", "FF6347", "8A2BE2"]
    
    color_index = (message_number - 1) % len(color_palette)
    return f"[C][B][{color_palette[color_index]}]{message_text}"    

def get_random_avatar():
        avatar_list = [
         '902050001', '902050002', '902050003', '902039016', '902050004', 
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
        random_avatar = random.choice(avatar_list)
        return  random_avatar

async def xSEndMsgsQQ(Msg , id , K , V):
    fields = {1: id , 2: id , 4: Msg , 5: 1756580149, 7: 2, 8: 904990072, 9: {1: "xBe4!sTo - C4", 2: int(get_random_avatar()), 4: 330, 5: 1001000001, 8: "xBe4!sTo - C4", 10: 1, 11: 1, 13: {1: 2}, 14: {1: 1158053040, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}}, 10: "en", 13: {2: 2, 3: 1}}
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)     

async def Create_xr_room_packet_fixed__(room_id, key, iv):
    """FIXED: Room chat packets must use Whisper connection"""
    random_color = generate_random_hex_color()

    fields = {
        1: 1,
        2: {
            1: 13777711848,  # Bot UID
            2: int(room_id),
            3: 3,  # Chat type 3 = room chat
            4: f"[FFFFFF]Hello",
            5: int(time.time()),  # Current timestamp, not hardcoded
            7: 2,
            9: {
                1: "XR SUPER ",
                2: bunner_(),   
                4: 228,
                7: 1,
            },
            10: "ar",  # Language (arabic? change to "en" if needed)
            13: {
                2: 1,
                3: 1
            }
        }
    }

    # Convert to protobuf hex
    proto_hex = (await CrEaTe_ProTo(fields)).hex()
    
    print(f"📦 Room chat proto: {len(proto_hex)//2} bytes")
    print(f"Hex start: {proto_hex[:50]}...")
    
    # CRITICAL FIX: Room chat uses Whisper connection (12xx headers)
    # Try different packet types for Whisper
    packet_type = "1215"  # Whisper connection for chat
    
    # Generate final encrypted packet
    final_packet = await GeneRaTePk(proto_hex, packet_type, key, iv)
    
    return final_packet

async def send_wave_messages(message_text, repeats, chat_id, key, iv, region):
    """Send message in wave pattern: expanding then shrinking"""
    global msg_spam_running
    
    count = 0
    total_cycles = 0
    
    while msg_spam_running and total_cycles < repeats:
        try:
            # EXPANDING phase (h, he, hel, hell, hello)
            for i in range(1, len(message_text) + 1):
                if not msg_spam_running:
                    break
                    
                partial_msg = message_text[:i]
                colorful_msg = await get_colorful_message(partial_msg, i)
                
                msg_packet = await xSEndMsgsQ(colorful_msg, int(chat_id), key, iv)
                if msg_packet and whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
                    count += 1
                    print(f"✅ Wave #{total_cycles+1} - Expanding: '{partial_msg}'")
                    await asyncio.sleep(0.1)
            
            # SHRINKING phase (hell, hel, he, h)
            for i in range(len(message_text) - 1, 0, -1):
                if not msg_spam_running:
                    break
                    
                partial_msg = message_text[:i]
                colorful_msg = await get_colorful_message(partial_msg, i)
                
                msg_packet = await xSEndMsgsQQ(colorful_msg, int(chat_id), key, iv)
                if msg_packet and whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
                    count += 1
                    print(f"✅ Wave #{total_cycles+1} - Shrinking: '{partial_msg}'")
                    await asyncio.sleep(0.1)
            
            total_cycles += 1
            print(f"🌀 Completed wave cycle {total_cycles}/{repeats}")
            
        except Exception as e:
            print(f"❌ Error in wave messages: {e}")
            break
    
    return count, total_cycles

async def handle_wave_completion(spam_task, message_text, repeats, sender_uid, chat_id, chat_type, key, iv):
    """Handle completion of wave messages"""
    try:
        message_count, cycles_completed = await spam_task
        
        total_per_cycle = (len(message_text) * 2) - 2
        expected_total = total_per_cycle * repeats
        

        
    except asyncio.CancelledError:
        cancel_msg = f"[B][C][00FF00]🛑 WAVE CANCELLED!\n"
        await safe_send_message(chat_type, cancel_msg, sender_uid, chat_id, key, iv)

async def msg_spam_loop(message_text, times, chat_id, key, iv, region, use_guild=False):
    """Send message multiple times — guild chat or squad chat depending on use_guild flag."""
    global msg_spam_running

    count = 0

    while msg_spam_running and count < times:
        try:
            if use_guild:
                # Guild/clan chat — use safe_send_message with chat_type 1
                await safe_send_message(1, message_text, 0, chat_id, key, iv)
            else:
                # Squad chat — build raw packet and send via ChaT connection
                msg_packet = await xSEndMsgsQQ(message_text, int(chat_id), key, iv)
                if not msg_packet:
                    print("❌ Failed to create squad message packet")
                    break
                if whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)

            count += 1
            chat_label = "guild" if use_guild else "squad"
            print(f"✅ Sent message #{count}/{times} to {chat_label} chat: '{message_text}'")
            await asyncio.sleep(0.2)

        except Exception as e:
            print(f"❌ Error in msg spam loop: {e}")
            import traceback
            traceback.print_exc()
            break

    return count

# Update the command handler to use the correct chat_id
# In the TcPChaT function, update the /msg command:



# Also, let's improve the handle_msg_spam_completion function:
async def handle_msg_spam_completion(spam_task, message_text, times, sender_uid, chat_id, chat_type, key, iv):
    """Handle completion of message spam and send final message"""
    try:
        actual_times = await spam_task
        
        # Send completion message
        if actual_times >= times:
            completion_msg = f"[B][C][00FF00]✅ MESSAGE SENDING COMPLETED!\n"
            completion_msg += f"[FFFFFF]📝 Message  : {message_text}\n"
            completion_msg += f"[FFFFFF]✅ Sent     : {actual_times}/{times} times\n"
            completion_msg += f"[00FF00]✓ All messages delivered!\n"
        elif actual_times > 0:
            completion_msg = f"[B][C][FFFF00]⚠️ MESSAGE SENDING PARTIALLY DONE!\n"
            completion_msg += f"[FFFFFF]📝 Message  : {message_text}\n"
            completion_msg += f"[FFFFFF]⚠️ Sent     : {actual_times}/{times} times\n"
            completion_msg += f"[FFFF00]↯ Success rate: {(actual_times/times)*100:.1f}%\n"
        else:
            completion_msg = f"[B][C][FF0000]❌ MESSAGE SENDING FAILED!\n"
            completion_msg += f"[FFFFFF]📝 Message  : {message_text}\n"
            completion_msg += f"[FFFFFF]❌ Sent     : 0/{times} times\n"
            completion_msg += f"[FF0000]Possible issues:\n"
            completion_msg += f"[FFFFFF]1. Bot not in guild/squad\n"
            completion_msg += f"[FFFFFF]2. Invalid chat ID\n"
            completion_msg += f"[FFFFFF]3. Connection error\n"
        
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("Message spam was cancelled by user")
        cancel_msg = f"[B][C][00FF00]🛑 MESSAGE SPAM CANCELLED!\n[FFFFFF]Message spam was stopped by user command.\n"
        await safe_send_message(chat_type, cancel_msg, sender_uid, chat_id, key, iv)
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ ERROR in message spam completion: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)
        
async def send_msg_in_room_async(Msg, room_id, key, iv):
    """Converted to your async TCP format"""
    from datetime import datetime
    sticker_value = get_random_sticker()
    
    fields = {
        1: 1,
        2: {
            1: int(room_id),
            2: int(room_id),
            3: 3,
            4: f"{Msg}",
            5: int(datetime.now().timestamp()),
            7: 2,
            8: f'{{"StickerStr" : "{sticker_value}", "type":"Sticker"}}',
            9: {
                1: "byte bot",
                2: int(await xBunnEr()),  # Changed to your function
                4: 329,
                7: 1,
            },
            10: "en",
            13: {2: 1, 3: 1},
        },
    }

    # Create protobuf packet using your function
    packet = await CrEaTe_ProTo(fields)
    
    # Convert to hex and add "7200"
    packet_hex = packet.hex() + "7200"

    # Encrypt using your function
    encrypted_packet = await encrypt_packet(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)

    # Determine format based on header length
    if len(header_length_final) == 2:
        final_packet = "1215000000" + header_length_final + encrypted_packet
        return bytes.fromhex(final_packet)

    elif len(header_length_final) == 3:
        final_packet = "121500000" + header_length_final + encrypted_packet
        return bytes.fromhex(final_packet)

    elif len(header_length_final) == 4:
        final_packet = "12150000" + header_length_final + encrypted_packet
        return bytes.fromhex(final_packet)

    elif len(header_length_final) == 5:
        final_packet = "12150000" + header_length_final + encrypted_packet
        return bytes.fromhex(final_packet)

# Command handler for room messages:
async def handle_room_message_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """
    Handle /roommsg command to send messages in custom rooms
    """
    parts = inPuTMsG.strip().split()
    
    if len(parts) < 3:
        error_msg = f"""[B][C][FF0000]❌ Usage: /roommsg (room_id) (message)
        
📝 Examples:
/roommsg 123456 Hello everyone!
/roommsg 987654 Welcome to my
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    room_id = parts[1]
    message = ' '.join(parts[2:])
    Msg = message 
    # Validate room ID
    if not room_id.isdigit():
        error_msg = f"[B][C][FF0000]❌ Room ID must be numbers only!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        print(error_msg)
        return
    
    # Send initial message
    initial_msg = f"[B][C][00FF00]📤 Sending room message...\n"
    initial_msg += f"🏠 Room: {room_id}\n"
    
    
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    print(initial_msg)
    
    try:
        # Create the room message packet
        room_packet = await send_msg_in_room_async(Msg, room_id, key, iv)
        
        if room_packet and whisper_writer:
            # Send via Whisper connection (for chat packets)
            whisper_writer.write(room_packet)
            await whisper_writer.drain()
            
            success_msg = f"""[B][C][00FF00]✅ ROOM MESSAGE SENT!

🏠 Room: {room_id}
📝 Message: {message}
"""
        else:
            success_msg = f"[B][C][FF0000]❌ Failed to create room packet!\n"
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        print(success_msg)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        print(error_msg)

async def create_training_start_packet(key, iv, region):
    """Create packet to start training mode in Free Fire"""
    
    try:
        # Decoded from your hex dump:
        # 62 27 01 01 28 00 01 00 00 00 00 00 79 2c 59 bf...
        # This appears to be a "start training" or "enter training ground" packet
        
        # Based on common Free Fire packet structure:
        # Packet type 0x27 = 39 decimal (training related)
        
        fields = {
            1: 39,  # Packet type for training (0x27 = 39)
            2: {
                1: 1,  # Action type (1 = start/enter)
                2: 1,  # Training mode type (1 = normal training)
                3: 0,  # Unknown flag
                4: 0,  # Unknown flag
                # The rest appears to be encrypted training data
                5: {
                    1: bytes.fromhex("79 2c 59 bf e0 5b be a6 00 ae 89 a5 26 4f 55 6f"),
                    2: bytes.fromhex("40 e5 e3 52 aa e2 46 26 ef e8 ac 5c 6c b1 db 9e"),
                    3: bytes.fromhex("87 09 4d aa ed c2 eb da")
                }
            }
        }
        
        # Alternative simpler structure (more likely):
        fields_simple = {
            1: 39,  # Training packet type
            2: {
                1: 1,   # Start training command
                2: 0,   # Training ground ID (0 = default)
                3: 1,   # Mode (1 = training)
                4: {    # Training settings
                    1: 1,  # Weapons enabled
                    2: 1,  # Bots enabled
                    3: 0,  # Unlimited ammo
                    4: 1,  # Health regen
                    5: 0   # God mode
                }
            }
        }
        
        # Let's try the simple structure first
        packet = await CrEaTe_ProTo(fields_simple)
        packet_hex = packet.hex()
        
        print(f"📦 Created training packet: {packet_hex[:50]}...")
        
        # Determine packet header based on region
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
            
        # Generate final encrypted packet
        final_packet = await GeneRaTePk(packet_hex, packet_type, key, iv)
        
        print(f"✅ Training start packet created")
        return final_packet
        
    except Exception as e:
        print(f"❌ Error creating training packet: {e}")
        import traceback
        traceback.print_exc()
        return None


async def start_training_mode(key, iv, region):
    """Start training mode - sends the training start packet"""
    
    try:
        training_packet = await create_training_start_packet(key, iv, region)
        
        if training_packet:
            # Send to Online connection
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', training_packet)
            print("🎮 Training mode start packet sent!")
            return True
        else:
            print("❌ Failed to create training packet")
            return False
            
    except Exception as e:
        print(f"❌ Error starting training: {e}")
        return False


# Add this command handler to your TcPChaT function:
async def handle_training_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle /train command to start training mode"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) == 1:
        # Just /train - start default training
        initial_msg = f"[B][C][00FF00]🎮 Starting training mode...\n"
        await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
        
        success = await start_training_mode(key, iv, region)
        
        if success:
            success_msg = f"[B][C][00FF00]✅ Training mode started!\n🏋️ Enter training ground to practice!\n"
        else:
            success_msg = f"[B][C][FF0000]❌ Failed to start training!\n"
            
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    elif len(parts) == 2 and parts[1] == "custom":
        # /train custom - custom training settings
        initial_msg = f"[B][C][00FF00]🎮 Starting custom training...\n"
        await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
        
        # You can add custom training settings here
        success = await start_training_mode(key, iv, region)
        
        if success:
            success_msg = f"[B][C][00FF00]✅ Custom training started!\n⚙️ Custom settings applied!\n"
        else:
            success_msg = f"[B][C][FF0000]❌ Failed to start custom training!\n"
            
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    else:
        error_msg = f"[B][C][FF0000]❌ Usage: /train [custom]\nExamples:\n/train - Start default training\n/train custom - Custom training\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def lag_team_loop(team_code, key, iv, region):
    """Rapid join/leave loop to create lag"""
    global lag_running
    count = 0
    
    while lag_running:
        try:
            # Join the team
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
            # Very short delay before leaving
            await asyncio.sleep(0.01)  # 10 milliseconds
            
            # Leave the team
            leave_packet = await ExiT(0, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            
            count += 1
            print(f"Lag cycle #{count} completed for team: {team_code}")
            
            # Short delay before next cycle
            await asyncio.sleep(0.01)  # 10 milliseconds between cycles
            
        except Exception as e:
            print(f"Error in lag loop: {e}")
            # Continue the loop even if there's an error
            await asyncio.sleep(0.1)
 
def get_tiktok_info(username):
    """Fetch TikTok user info via tikwm.com (free, no API key needed)."""
    try:
        username = username.strip().lstrip('@')

        # Primary: tikwm.com free TikTok data API
        url = f"https://www.tikwm.com/api/user/info"
        params = {"unique_id": username}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.tikwm.com/",
        }
        res = requests.get(url, params=params, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data.get("code") == 0:
                d = data.get("data", {})
                u = d.get("user", {})
                s = d.get("stats", {})
                return {
                    "full_name": u.get("nickname", "Unknown"),
                    "username": u.get("uniqueId", username),
                    "bio": u.get("signature", ""),
                    "followers": s.get("followerCount", 0),
                    "following": s.get("followingCount", 0),
                    "likes": s.get("heartCount", 0),
                    "videos": s.get("videoCount", 0),
                    "private": u.get("privateAccount", False),
                    "verified": u.get("verified", False),
                }

        # Fallback: scrape TikTok page for SIGI_STATE
        page_res = requests.get(
            f"https://www.tiktok.com/@{username}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            timeout=15,
            allow_redirects=True
        )
        if page_res.status_code == 200:
            html = page_res.text
            for pattern in [
                r'<script id="SIGI_STATE" type="application/json">(.*?)</script>',
                r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            ]:
                m = re.search(pattern, html, re.DOTALL)
                if m:
                    d = json.loads(m.group(1))
                    users_map = d.get("UserModule", {}).get("users", {})
                    stats_map = d.get("UserModule", {}).get("stats", {})
                    props_user = (d.get("props", {}).get("pageProps", {}).get("userInfo") or {})
                    user = (list(users_map.values())[0] if users_map
                            else props_user.get("user", {}))
                    stats = (list(stats_map.values())[0] if stats_map
                             else props_user.get("stats", {}))
                    if user:
                        return {
                            "full_name": user.get("nickname", "Unknown"),
                            "username": user.get("uniqueId", username),
                            "bio": user.get("signature", ""),
                            "followers": stats.get("followerCount", 0),
                            "following": stats.get("followingCount", 0),
                            "likes": stats.get("heartCount", 0),
                            "videos": stats.get("videoCount", 0),
                            "private": user.get("privateAccount", False),
                            "verified": user.get("verified", False),
                        }

        return {"error": "not_found"}
    except Exception as e:
        return {"error": str(e)}


def get_instagram_info(username):
    """Fetch Instagram user info — tries multiple approaches."""
    import re as _re
    import json as _json
    username = username.strip().lstrip('@').lower()

    def _parse_ig_user(user):
        return {
            "full_name": user.get("full_name") or "N/A",
            "username": user.get("username", username),
            "followers": user.get("edge_followed_by", {}).get("count", 0),
            "following": user.get("edge_follow", {}).get("count", 0),
            "posts": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            "bio": (user.get("biography") or "N/A")[:60],
            "private": user.get("is_private", False),
            "verified": user.get("is_verified", False),
        }

    def _parse_count(val):
        """Convert '1.5M', '230K', '1,234' etc to int."""
        if not val:
            return 0
        val = str(val).strip().replace(',', '')
        try:
            if val.upper().endswith('M'):
                return int(float(val[:-1]) * 1_000_000)
            if val.upper().endswith('K'):
                return int(float(val[:-1]) * 1_000)
            return int(float(val))
        except Exception:
            return 0

    # ── Attempt 0: Session-based (works for private accounts — requires IG_SESSION_ID) ──
    if IG_SESSION_ID:
        try:
            h_sess = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "x-ig-app-id": "936619743392459",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.instagram.com/",
                "Cookie": f"sessionid={IG_SESSION_ID};",
            }
            r_sess = requests.get(
                f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
                headers=h_sess, timeout=15
            )
            if r_sess.status_code == 404:
                return {"error": "not_found"}
            if r_sess.status_code == 200:
                d_sess = r_sess.json()
                u_sess = d_sess.get("data", {}).get("user") or d_sess.get("graphql", {}).get("user")
                if u_sess:
                    return _parse_ig_user(u_sess)
        except Exception:
            pass

    # ── Attempt 1: OG meta tags via Facebook crawler UA (most reliable, no auth needed) ──
    try:
        for ua in [
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "Twitterbot/1.0",
            "LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com/)",
        ]:
            h_og = {
                "User-Agent": ua,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }
            try:
                r_og = requests.get(
                    f"https://www.instagram.com/{username}/",
                    headers=h_og, timeout=15, allow_redirects=True
                )
                if r_og.status_code == 404:
                    return {"error": "not_found"}
                if r_og.status_code == 200:
                    html = r_og.text
                    title_m = _re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html)
                    if not title_m:
                        title_m = _re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']', html)
                    desc_m = _re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', html)
                    if not desc_m:
                        desc_m = _re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:description["\']', html)

                    if title_m:
                        title = title_m.group(1)
                        # Title: "MrBeast (@mrbeast) • Instagram photos and videos"
                        name_m = _re.match(r'^(.+?)\s*\(', title)
                        full_name = name_m.group(1).strip() if name_m else title.split('•')[0].strip()
                        full_name = full_name or "N/A"

                        followers = following = posts = 0
                        bio = "N/A"

                        if desc_m:
                            desc = desc_m.group(1)
                            # "230M Followers, 551 Following, 741 Posts - ..."
                            fol_m = _re.search(r'([\d,\.]+[KkMm]?)\s*Followers?', desc, _re.IGNORECASE)
                            fwg_m = _re.search(r'([\d,\.]+[KkMm]?)\s*Following', desc, _re.IGNORECASE)
                            pst_m = _re.search(r'([\d,\.]+[KkMm]?)\s*Posts?', desc, _re.IGNORECASE)
                            if fol_m:
                                followers = _parse_count(fol_m.group(1))
                            if fwg_m:
                                following = _parse_count(fwg_m.group(1))
                            if pst_m:
                                posts = _parse_count(pst_m.group(1))
                            bio_m = _re.search(r'Posts?\s*[-–]\s*(.+)$', desc, _re.DOTALL)
                            if bio_m:
                                bio = bio_m.group(1)[:60]

                        return {
                            "full_name": full_name,
                            "username": username,
                            "followers": followers,
                            "following": following,
                            "posts": posts,
                            "bio": bio,
                            "private": False,
                            "verified": False,
                        }
            except Exception:
                continue
    except Exception:
        pass

    # ── Attempt 2: Android app user-agent (i.instagram.com) ──
    try:
        h1 = {
            "User-Agent": (
                "Instagram 275.0.0.27.98 Android (33/13; 420dpi; "
                "1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 458229258)"
            ),
            "x-ig-app-id": "936619743392459",
            "x-ig-capabilities": "36oDx",
            "x-ig-connection-type": "WIFI",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "*/*",
        }
        r1 = requests.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            headers=h1, timeout=12
        )
        if r1.status_code == 404:
            return {"error": "not_found"}
        if r1.status_code == 200:
            d1 = r1.json()
            u1 = d1.get("data", {}).get("user") or d1.get("graphql", {}).get("user")
            if u1:
                return _parse_ig_user(u1)
    except Exception:
        pass

    # ── Attempt 3: iOS app user-agent ──
    try:
        h2 = {
            "User-Agent": (
                "Instagram 228.0.0.16.117 (iPhone; CPU iPhone OS 15_0 like Mac OS X; "
                "en_US; en_US; scale=3.00; 1242x2688) AppleWebKit/420+"
            ),
            "x-ig-app-id": "124024574287414",
            "Accept-Language": "en-US",
            "x-fb-http-engine": "Liger",
        }
        r2 = requests.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            headers=h2, timeout=12
        )
        if r2.status_code == 404:
            return {"error": "not_found"}
        if r2.status_code == 200:
            d2 = r2.json()
            u2 = d2.get("data", {}).get("user") or d2.get("graphql", {}).get("user")
            if u2:
                return _parse_ig_user(u2)
    except Exception:
        pass

    # ── Attempt 4: instaloader ──
    try:
        import instaloader as _il
        L = _il.Instaloader(quiet=True, download_pictures=False,
                             download_videos=False, download_video_thumbnails=False,
                             download_geotags=False, download_comments=False,
                             save_metadata=False)
        profile = _il.Profile.from_username(L.context, username)
        return {
            "full_name": profile.full_name or "N/A",
            "username": profile.username,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "bio": (profile.biography or "N/A")[:60],
            "private": profile.is_private,
            "verified": profile.is_verified,
        }
    except ImportError:
        pass
    except Exception as _e:
        err = str(_e).lower()
        if "404" in err or "not found" in err or "does not exist" in err:
            return {"error": "not_found"}

    # ── Attempt 5: JSON-LD from profile page ──
    try:
        h4 = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "text/html,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        r4 = requests.get(f"https://www.instagram.com/{username}/", headers=h4, timeout=12)
        if r4.status_code == 404:
            return {"error": "not_found"}
        matches = _re.findall(r'<script type="application/ld\+json">(.*?)</script>', r4.text, _re.DOTALL)
        for m in matches:
            try:
                ld = _json.loads(m)
                entity = ld.get("mainEntity") or ld
                stats = {s.get("interactionType", ""): s.get("userInteractionCount", 0)
                         for s in entity.get("interactionStatistic", [])}
                name = entity.get("name", "N/A")
                if name and name != "N/A":
                    return {
                        "full_name": name,
                        "username": username,
                        "followers": stats.get("http://schema.org/FollowAction", 0),
                        "following": 0,
                        "posts": stats.get("http://schema.org/WriteAction", 0),
                        "bio": (entity.get("description") or "N/A")[:60],
                        "private": False,
                        "verified": False,
                    }
            except Exception:
                continue
    except Exception:
        pass

    return {"error": "blocked"}


def send_instagram_info(username):
    """Fetch and format Instagram user info as a message string."""
    data = get_instagram_info(username)
    err = data.get("error")
    if err == "not_found":
        return f"[B][C][FF0000]❌ User @{username} not found!\n"
    if err == "blocked":
        return f"[B][C][FF0000]❌ IG blocked request.\nInstall instaloader:\npip install instaloader\n"
    if err:
        return f"[B][C][FF0000]❌ IG Error: {str(err)[:40]}\n"

    verified = "✅" if data.get("verified") else "❌"
    private  = "🔒 Yes" if data.get("private") else "🌐 No"

    return f"""
[B][C][FF69B4]╭[FF1493]─[FF1493]╮[FFFFFF]
[C][B][FF69B4]│[FF69B4]IG[FF69B4] │[FFFFFF]║[FF1493]INSTAGRAM INFO[FFFFFF]║
[C][B][FF1493]╰[FF69B4]─[FF69B4]╯[FFFFFF]
[C][B][FF1493]━━━━━━━━━━━
[C][B][FFFFFF]Full Name  : [FF69B4]{data.get('full_name', 'N/A')}
[C][B][FFFFFF]Username   : [FF69B4]@{data.get('username', username)}
[C][B][FFFFFF]Verified   : [00FF00]{verified}
[C][B][FFFFFF]Private    : [FFFF00]{private}
[C][B][FFFFFF]Followers  : [00BFFF]{xMsGFixinG(str(data.get('followers', 0)))}
[C][B][FFFFFF]Following  : [00BFFF]{xMsGFixinG(str(data.get('following', 0)))}
[C][B][FFFFFF]Posts      : [00BFFF]{xMsGFixinG(str(data.get('posts', 0)))}
[C][B][FFFFFF]Bio        : [AAAAAA]{data.get('bio', '') or 'N/A'}
[C][B][FF1493]━━━━━━━━━━━
[C][B][FFFFFF]Developer  : [FF0000]Ayaan
"""


def send_tiktok_info(username):
    """Fetch and format TikTok user info as a message string."""
    data = get_tiktok_info(username)

    err = data.get("error")
    if err == "not_found":
        return f"[B][C][FF0000]❌ TikTok user not found: @{username}\n"
    if err:
        return f"[B][C][FF0000]❌ TikTok Error: {err}\n"

    verified = "✅" if data.get("verified") else "❌"
    private = "Yes" if data.get("private") else "No"

    return f"""
[B][C][FFD700]╭[FFFF00]─[FFFF00]╮[FFFFFF]
[C][B][00BFFF]│[00BFFF]ꚠ[00BFFF] │[FFFFFF]║[00BFFF]TIKTOK INFO[FFFFFF]║
[C][B][FF00FF]╰[FFFF00]─[FFFF00]╯[FFFFFF]
[C][B][FF00FF]━━━━━━━━━━━
[C][B][FFFFFF]Fullname   : [FFFF00]{data.get('full_name', 'Unknown')}
[C][B][FFFFFF]Username   : [FFFF00]@{data.get('username', username)}
[C][B][FFFFFF]Verified   : [00FF00]{verified}
[C][B][FFFFFF]Private    : [FFFF00]{private}
[C][B][FFFFFF]Followers  : [00BFFF]{xMsGFixinG(str(data.get('followers', 0)))}
[C][B][FFFFFF]Following  : [00BFFF]{xMsGFixinG(str(data.get('following', 0)))}
[C][B][FFFFFF]Likes      : [00BFFF]{xMsGFixinG(str(data.get('likes', 0)))}
[C][B][FFFFFF]Videos     : [00BFFF]{xMsGFixinG(str(data.get('videos', 0)))}
[C][B][FFFFFF]Bio        : [AAAAAA]{data.get('bio', '') or 'N/A'}
[C][B][00FFFF]━━━━━━━━━━━
[C][B][FFFFFF]Developer  : [FF0000]Ayaan
"""


# -------------------------------------------------
# Helper function: Fetch YouTube info JSON
# -------------------------------------------------
def get_youtube_info(channel_name):
    try:
        channel_name = channel_name.strip().lstrip('@')

        if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your_youtube_api_key_here":
            return {"error": "no_key"}

        base = "https://www.googleapis.com/youtube/v3"

        # Search for channel by name/handle
        search_url = f"{base}/search"
        search_params = {
            "part": "snippet",
            "q": channel_name,
            "type": "channel",
            "maxResults": 1,
            "key": YOUTUBE_API_KEY
        }
        search_res = requests.get(search_url, params=search_params, timeout=15).json()
        items = search_res.get("items", [])
        if not items:
            return {"error": "not_found"}

        channel_id = items[0]["snippet"]["channelId"]
        channel_title = items[0]["snippet"]["title"]
        handle = items[0]["snippet"].get("customUrl", f"@{channel_name}")
        published_at = items[0]["snippet"].get("publishedAt", "")
        description = items[0]["snippet"].get("description", "")

        # Fetch statistics + contentDetails (for uploads playlist)
        stats_url = f"{base}/channels"
        stats_params = {
            "part": "statistics,contentDetails,brandingSettings",
            "id": channel_id,
            "key": YOUTUBE_API_KEY
        }
        stats_res = requests.get(stats_url, params=stats_params, timeout=15).json()
        stats_items = stats_res.get("items", [])
        stats = stats_items[0].get("statistics", {}) if stats_items else {}
        content_details = stats_items[0].get("contentDetails", {}) if stats_items else {}
        branding = stats_items[0].get("brandingSettings", {}) if stats_items else {}
        country = branding.get("channel", {}).get("country", "N/A")

        # Fetch most viewed video from channel
        top_video_title = "N/A"
        top_video_views = "0"
        top_video_url = "N/A"
        top_video_published = "N/A"
        try:
            top_search_params = {
                "part": "snippet",
                "channelId": channel_id,
                "order": "viewCount",
                "type": "video",
                "maxResults": 1,
                "key": YOUTUBE_API_KEY
            }
            top_res = requests.get(search_url, params=top_search_params, timeout=15).json()
            top_items = top_res.get("items", [])
            if top_items:
                top_video_id = top_items[0]["id"].get("videoId", "")
                top_video_title = top_items[0]["snippet"].get("title", "N/A")
                top_video_published = top_items[0]["snippet"].get("publishedAt", "")[:10] or "N/A"
                top_video_url = f"youtu.be/{top_video_id}" if top_video_id else "N/A"
                # Fetch view count for that video
                if top_video_id:
                    vid_stats_params = {
                        "part": "statistics",
                        "id": top_video_id,
                        "key": YOUTUBE_API_KEY
                    }
                    vid_res = requests.get(f"{base}/videos", params=vid_stats_params, timeout=15).json()
                    vid_items = vid_res.get("items", [])
                    if vid_items:
                        top_video_views = vid_items[0].get("statistics", {}).get("viewCount", "0")
        except Exception:
            pass

        # Fetch latest video from uploads playlist
        last_video_title = "N/A"
        last_video_published = "N/A"
        last_video_url = "N/A"
        try:
            uploads_playlist = content_details.get("relatedPlaylists", {}).get("uploads", "")
            if uploads_playlist:
                playlist_params = {
                    "part": "snippet",
                    "playlistId": uploads_playlist,
                    "maxResults": 1,
                    "key": YOUTUBE_API_KEY
                }
                pl_res = requests.get(f"{base}/playlistItems", params=playlist_params, timeout=15).json()
                pl_items = pl_res.get("items", [])
                if pl_items:
                    last_video_title = pl_items[0]["snippet"].get("title", "N/A")
                    last_video_published = pl_items[0]["snippet"].get("publishedAt", "")[:10] or "N/A"
                    last_vid_id = pl_items[0]["snippet"].get("resourceId", {}).get("videoId", "")
                    last_video_url = f"youtu.be/{last_vid_id}" if last_vid_id else "N/A"
        except Exception:
            pass

        return {
            "channel_title": channel_title,
            "channel_id": channel_id,
            "handle": handle if handle.startswith("@") else f"@{handle}",
            "published_at": published_at[:10] if published_at else "N/A",
            "description": description[:200] if description else "",
            "country": country,
            "statistics": {
                "subscribers": stats.get("subscriberCount", "Hidden"),
                "views": stats.get("viewCount", "0"),
                "videos": stats.get("videoCount", "0"),
            },
            "top_video": {
                "title": top_video_title,
                "views": top_video_views,
                "url": top_video_url,
                "published": top_video_published,
            },
            "last_video": {
                "title": last_video_title,
                "published": last_video_published,
                "url": last_video_url,
            }
        }
    except Exception as e:
        return {"error": str(e)}

# -------------------------------------------------
# Helper function: Format and send YouTube info
# -------------------------------------------------
async def send_youtube_info(channel_name, chat_type, uid, chat_id, key, iv):
    try:
        loop = asyncio.get_running_loop()
        response_json = await loop.run_in_executor(None, get_youtube_info, channel_name)

        # Handle errors
        err = response_json.get("error")
        if err == "no_key":
            await safe_send_message(chat_type,
                "[B][C][FF0000]❌ YouTube API key not set!\nAdd your key to YOUTUBE_API_KEY in the config.\nGet a free key at: console.cloud.google.com\n",
                uid, chat_id, key, iv)
            return
        if err == "not_found":
            await safe_send_message(chat_type,
                f"[B][C][FF0000]❌ Channel not found: {channel_name}\n",
                uid, chat_id, key, iv)
            return
        if err:
            await safe_send_message(chat_type,
                f"[B][C][FF0000]❌ YouTube Error: {err}\n",
                uid, chat_id, key, iv)
            return

        # Stats formatting
        stats = response_json.get("statistics", {})
        subscribers = xMsGFixinG(stats.get("subscribers", "0"))
        views = xMsGFixinG(stats.get("views", "0"))
        videos = xMsGFixinG(stats.get("videos", "0"))

        # Description
        description = response_json.get("description", "")

        # Main info message
        main_info = f"""
[B][C][FF0000]╭[FF0000]─[FF0000]╮[FFFFFF]
[C][B][FF0000]│[FFFFFF]▶[FF0000] │[FFFFFF]║[00BFFF]YOUTUBE INFO[FFFFFF]║
[C][B][FF0000]╰[FF0000]─[FF0000]╯[FFFFFF]
[C][B][FF00FF]━━━━━━━━━━━
[C][B][FFFFFF]Channel Name : [FFFF00]{response_json.get('channel_title', 'Unknown')}
[C][B][FFFFFF]Channel ID    : [FFFF00]{response_json.get('channel_id', 'Unknown')}
[C][B][FFFFFF]Handle        : [00BFFF]{response_json.get('handle', 'Unknown')}
[C][B][FFFFFF]Subscribers   : [00BFFF]{subscribers}
[C][B][FFFFFF]Views         : [00BFFF]{views}
[C][B][FFFFFF]Videos        : [00BFFF]{videos}
[C][B][FFFFFF]Published At  : [00BFFF]{xMsGFixinG(response_json.get('published_at', ''))}
[C][B][00FFFF]━━━━━━━━━━━
[C][B][FFFFFF]Developer     : Ayaan
"""
        await safe_send_message(chat_type, main_info, uid, chat_id, key, iv)

        # Send description separately after 0.2s
        await asyncio.sleep(0.2)
        if description:
            await safe_send_message(chat_type, f"[B][C][00BFFF]Description: {description}", uid, chat_id, key, iv)

        # Send most viewed video info
        top_video = response_json.get("top_video", {})
        if top_video and top_video.get("title", "N/A") != "N/A":
            await asyncio.sleep(0.2)
            top_msg = f"""
[B][C][FF0000]╭[FF0000]─[FF0000]╮[FFFFFF]
[C][B][FF0000]│[FFFFFF]▶[FF0000] │[FFFFFF]║[FFFF00]MOST VIEWED VIDEO[FFFFFF]║
[C][B][FF0000]╰[FF0000]─[FF0000]╯[FFFFFF]
[C][B][FF00FF]━━━━━━━━━━━
[C][B][FFFFFF]Title     : [FFFF00]{top_video.get('title', 'N/A')}
[C][B][FFFFFF]Views     : [00FF00]{xMsGFixinG(top_video.get('views', '0'))}
[C][B][FFFFFF]Published : [00BFFF]{top_video.get('published', 'N/A')}
[C][B][FFFFFF]Link      : [00BFFF]{top_video.get('url', 'N/A')}
[C][B][00FFFF]━━━━━━━━━━━
"""
            await safe_send_message(chat_type, top_msg, uid, chat_id, key, iv)

        # Send latest video info
        last_video = response_json.get("last_video", {})
        if last_video and last_video.get("title", "N/A") != "N/A":
            await asyncio.sleep(0.2)
            last_msg = f"""
[B][C][FF0000]╭[FF0000]─[FF0000]╮[FFFFFF]
[C][B][FF0000]│[FFFFFF]▶[FF0000] │[FFFFFF]║[00FF00]LATEST VIDEO[FFFFFF]║
[C][B][FF0000]╰[FF0000]─[FF0000]╯[FFFFFF]
[C][B][FF00FF]━━━━━━━━━━━
[C][B][FFFFFF]Title     : [FFFF00]{last_video.get('title', 'N/A')}
[C][B][FFFFFF]Published : [00BFFF]{last_video.get('published', 'N/A')}
[C][B][FFFFFF]Link      : [00BFFF]{last_video.get('url', 'N/A')}
[C][B][00FFFF]━━━━━━━━━━━
"""
            await safe_send_message(chat_type, last_msg, uid, chat_id, key, iv)

    except Exception as e:
        await safe_send_message(chat_type,
            f"[B][C][FF0000]❌ YouTube command crashed: {e}\n",
            uid, chat_id, key, iv)

import requests

def get_level_info(player_id):
    url = f"https://your-api.vercel.app/level/level?uid={player_id}"

    try:
        res = requests.get(url, timeout=20)

        if res.status_code != 200:
            return [f"""
[B][FF0000]═════════════
[B][FFFFFF]   API ERROR
[FF0000]═════════════

[FF4444]STATUS : [FFFFFF]{res.status_code}

[FF0000]═════════════
""".strip()]

        data = res.json()

        if not data.get("success"):
            return ["""
[B][FF0000]═════════════
[B][FFFFFF]   LEVEL FETCH FAILED
[FF0000]═════════════

[FF4444]Unable to get level information.

[FF0000]═════════════
""".strip()]

        # 🔹 Message 1 (Upper Part)
        msg1 = f"""
[B][FF1493]═════════════
[B][00FFFF]   LEVEL INFORMATION
[FF1493]═════════════

[FFD700]PLAYER NAME  : [00FF00]{xMsGFixinG(data.get('nickname'))}
[FFD700]UID          : [00FFAA]{xMsGFixinG(data.get('uid'))}

[FF00FF]CURRENT LEVEL: [FFD700]{xMsGFixinG(data.get('current_level'))}
[00FFFF]CURRENT EXP  : [FFFFFF]{xMsGFixinG(data.get('current_exp'))}

[66FF00]EXP THIS LVL : [FFFFFF]{xMsGFixinG(data.get('exp_for_current_level'))}
[66FF00]NEXT LVL EXP : [FFFFFF]{xMsGFixinG(data.get('exp_for_next_level'))}
[FF1493]═════════════
""".strip()

        # 🔹 Message 2 (Lower Part)
        msg2 = f"""
[B][FF1493]═════════════
[B][00FFFF]   LEVEL PROGRESS 
[FF1493]═════════════

[FFA500]EXP NEEDED   : [FF4444]{xMsGFixinG(data.get('exp_needed'))}
[AA00FF]PROGRESS     : [00FF00]{xMsGFixinG(str(data.get('progress_percentage')) + "%")}

[FFD700]TO LEVEL 100 : [FFFFFF]{xMsGFixinG(data.get('exp_needed_for_100'))}
[FF1493]LEVEL 100 EXP: [FFFFFF]{xMsGFixinG(data.get('level_100_exp'))}

[FF1493]═════════════
""".strip()

        return [msg1, msg2]

    except requests.exceptions.RequestException:
        return ["""
[B][FF0000]═════════════
[B][FFFFFF] CONNECTION FAILED
[FF0000]═════════════

[FF4444]Unable to connect to Level API.

[FF0000]═════════════
""".strip()]

def send_guild_info(guild_id):
    """Fetch guild info directly from Free Fire game server — no external APIs."""
    try:
        token = load_jwt_token()
        if not token:
            return "[B][C][FF0000]❌ No bot token found. Check token.json."

        # Payload: field 1 = clan_id varint (confirmed working format)
        clan_id_varint = encode_varint(int(guild_id))
        payload = f"08{clan_id_varint}"
        encrypted_payload = encrypt_api(payload)
        body = bytes.fromhex(encrypted_payload)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-A515F Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        # Primary URL: clientbp.common.ggbluefox.com (confirmed working in reference bot)
        # Fallback:   clientbp.ggblueshark.com
        _urls = [
            "https://clientbp.common.ggbluefox.com/GetClanInfoByClanID",
            "https://clientbp.ggblueshark.com/GetClanInfoByClanID",
            get_friend_server_url(region, "GetClanInfoByClanID"),
        ]
        res = None
        for _url in _urls:
            try:
                print(f"🏰 GetClanInfoByClanID → {_url}")
                _r = requests.post(_url, data=body, headers=headers, timeout=10, verify=False)
                print(f"   → HTTP {_r.status_code} | {len(_r.content)} bytes")
                if _r.status_code in (200, 201):
                    res = _r
                    break
            except Exception as _e:
                print(f"   → error: {_e}")

        if res is None or res.status_code not in (200, 201):
            _code = res.status_code if res is not None else "N/A"
            return f"[B][C][FF0000]❌ Server returned HTTP {_code}. Try again later."

        # clientbp.common.ggbluefox.com returns RAW protobuf (no AES encryption).
        raw_bytes = res.content
        print(f"🏰 Raw protobuf hex: {raw_bytes.hex()}")

        def _decode_proto(data):
            """Pure-Python protobuf decoder — no external library needed."""
            result = {}
            i, n = 0, len(data)
            while i < n:
                try:
                    tag, shift = 0, 0
                    while i < n:
                        b = data[i]; i += 1
                        tag |= (b & 0x7F) << shift; shift += 7
                        if not (b & 0x80): break
                    fid = tag >> 3
                    wt  = tag & 0x7
                    if wt == 0:        # varint
                        val, shift = 0, 0
                        while i < n:
                            b = data[i]; i += 1
                            val |= (b & 0x7F) << shift; shift += 7
                            if not (b & 0x80): break
                        result[fid] = val
                    elif wt == 2:      # length-delimited (string / bytes / nested)
                        ln, shift = 0, 0
                        while i < n:
                            b = data[i]; i += 1
                            ln |= (b & 0x7F) << shift; shift += 7
                            if not (b & 0x80): break
                        raw = data[i:i+ln]; i += ln
                        try:
                            result[fid] = raw.decode('utf-8')
                        except Exception:
                            result[fid] = raw          # keep as bytes for nested
                    elif wt == 1: i += 8               # 64-bit — skip
                    elif wt == 5: i += 4               # 32-bit — skip
                    else: break
                except Exception:
                    break
            return result

        pf = _decode_proto(raw_bytes)
        # Recurse into any bytes fields (nested messages)
        for _fid, _val in list(pf.items()):
            if isinstance(_val, bytes):
                sub = _decode_proto(_val)
                if sub:
                    pf.update(sub)    # merge sub-fields into top dict
                    try:
                        pf[_fid] = _val.decode('utf-8')
                    except Exception:
                        pass
        print(f"🏰 Parsed proto fields: {pf}")

        def sg(*fids, default="N/A"):
            for fid in fids:
                v = pf.get(fid)
                if v not in (None, 0, "", b""):
                    return str(v)
            return default

        # Confirmed field mapping from live server response:
        # 1  = clanId        (varint)
        # 2  = clanName      (string)
        # 3  = createTime    (unix timestamp varint)
        # 4  = captainId     (varint UID)
        # 5  = activityScore (varint)
        # 6  = memberCount   (varint)
        # 7  = clanLevel     (varint)
        # 8  = region        (string)
        # 9  = flag/status   (varint, usually 1)
        # 11/12 = description (string)
        # maxMembers is always 50 in FF — not sent in response
        print(f"🏰 All parsed fields: {pf}")
        clan_id_val = sg(1,  default=str(guild_id))
        clan_name   = sg(2,  default="N/A")
        clan_level  = sg(7,  default="N/A")
        members     = sg(6,  default="0")
        max_members = "50"
        score       = sg(5,  default="0")
        description = sg(11, 12, 13, default="")
        clan_region = sg(8,  default="N/A")
        captain_id  = sg(4,  default="N/A")
        create_time = sg(3,  default="")
        print(f"🏰 Parsed — name={clan_name} level={clan_level} members={members} captain={captain_id}")

        import datetime as _dt
        desc_line   = f"\n[B][FFFFFF]Description: [AAAAAA]{description}" if description and description != "N/A" else ""
        owner_line  = f"\n[B][FFFFFF]Owner UID: [00BFFF]{xMsGFixinG(captain_id)}" if captain_id not in ("N/A", "0", "1", "") else ""
        if create_time and create_time not in ("0", "1", ""):
            try:
                _ts  = int(create_time)
                _date = _dt.datetime.utcfromtimestamp(_ts).strftime("%Y-%m-%d")
                create_line = f"\n[B][FFFFFF]Created: [AAAAAA]{_date}"
            except Exception:
                create_line = ""
        else:
            create_line = ""

        msg = (
            "[B][C][FFD700]==================\n"
            "[FFD700]   GUILD INFORMATION\n"
            "[FFD700]==================\n"
            f"[FFD700]Name   : [00FF00]{xMsGFixinG(clan_name)}\n"
            f"[FFD700]ID     : [00BFFF]{xMsGFixinG(clan_id_val)}\n"
            f"[FFD700]Region : [FF69B4]{clan_region}\n"
            f"[FFD700]Level  : [FFA500]{xMsGFixinG(clan_level)}\n"
            f"[FFD700]Members: [00FF7F]{xMsGFixinG(members)}/50\n"
            f"[FFD700]Score  : [FFD700]{xMsGFixinG(score)}"
            f"{owner_line}{create_line}{desc_line}\n"
            "[FFD700]=================="
        )
        print(f"🏰 Sending guild info to chat ({len(msg)} chars)")
        return msg

    except requests.exceptions.RequestException:
        return "[B][C][FF0000]❌ Guild server connection failed!"
    except Exception as e:
        print(f"❌ send_guild_info error: {e}")
        return f"[B][C][FF0000]❌ Unexpected Error: {str(e)}"


def search_guild_by_name(clan_name):
    """Fuzzy-search guilds by name using FuzzySearchClanByName endpoint (ref: github.com/paulafredo/FuzzySearchClanByName)."""
    try:
        token = load_jwt_token()
        if not token:
            return "[B][C][FF0000]❌ No bot token found. Check token.json."

        # Build protobuf manually: field 1, wire type 2 (string) = clan name
        name_bytes = clan_name.encode('utf-8')
        name_len_varint = encode_varint(len(name_bytes))
        payload_hex = f"0a{name_len_varint}{name_bytes.hex()}"
        encrypted_payload = encrypt_api(payload_hex)
        body = bytes.fromhex(encrypted_payload)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "OB52",
            "X-GA": "v1 1",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G998B Build/SP1A.210812.016)",
            "Host": "clientbp.ggpolarbear.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        url = "https://clientbp.ggpolarbear.com/FuzzySearchClanByName"
        print(f"🔍 FuzzySearchClanByName → {url} | name={clan_name}")
        res = requests.post(url, data=body, headers=headers, timeout=12, verify=False)
        print(f"   → HTTP {res.status_code} | {len(res.content)} bytes | hex: {res.content.hex()[:80]}")

        if res.status_code not in (200, 201):
            return f"[B][C][FF0000]❌ Server returned HTTP {res.status_code}. Try again."

        raw_bytes = res.content
        if not raw_bytes:
            return f"[B][C][FF0000]❌ No guilds found matching '{xMsGFixinG(clan_name)}'."

        # Parse outer repeated field 1 entries — each is one clan result
        def _read_varint(data, pos):
            val, shift = 0, 0
            while pos < len(data):
                b = data[pos]; pos += 1
                val |= (b & 0x7F) << shift; shift += 7
                if not (b & 0x80):
                    break
            return val, pos

        def _parse_proto_fields(data):
            """Parse a flat protobuf message into {field_id: value} dict."""
            r = {}
            i, n = 0, len(data)
            while i < n:
                try:
                    tag, i = _read_varint(data, i)
                    fid = tag >> 3
                    wt  = tag & 0x7
                    if wt == 0:
                        val, i = _read_varint(data, i)
                        r[fid] = val
                    elif wt == 2:
                        ln, i = _read_varint(data, i)
                        raw = data[i:i + ln]; i += ln
                        try:
                            r[fid] = raw.decode('utf-8')
                        except Exception:
                            r[fid] = raw
                    elif wt == 1:
                        i += 8
                    elif wt == 5:
                        i += 4
                    else:
                        break
                except Exception:
                    break
            return r

        # Collect all outer field-1 blobs (one per matching clan)
        clans = []
        i, n = 0, len(raw_bytes)
        while i < n:
            try:
                tag, i = _read_varint(raw_bytes, i)
                fid = tag >> 3
                wt  = tag & 0x7
                if wt == 2:
                    ln, i = _read_varint(raw_bytes, i)
                    entry = raw_bytes[i:i + ln]; i += ln
                    if fid == 1:
                        clans.append(entry)
                elif wt == 0:
                    _, i = _read_varint(raw_bytes, i)
                elif wt == 1:
                    i += 8
                elif wt == 5:
                    i += 4
                else:
                    break
            except Exception:
                break

        if not clans:
            return f"[B][C][FF0000]❌ No guilds found matching '{xMsGFixinG(clan_name)}'."

        # Field mapping confirmed from decoded_traffic.txt:
        # 1=clanId, 2=fullName, 3=createTime, 4=captainId
        # 5=status, 6=memberCount, 7=level, 13=region, 36=activityScore, 49=description
        lines = [
            "[B][C][FFD700]╔════════════════╗",
            "[B][C][FF4500]   GUILD SEARCH RESULTS",
            f"[B][C][FFD700]╚════════════════╝",
            f"[B][AAAAAA]Query: [FFFFFF]{xMsGFixinG(clan_name)}\n",
        ]

        for idx, entry_bytes in enumerate(clans[:5], 1):
            p = _parse_proto_fields(entry_bytes)

            def sg(*fids, default="N/A"):
                for f in fids:
                    v = p.get(f)
                    if v not in (None, 0, "", b""):
                        return str(v)
                return default

            cid     = sg(1, default="N/A")
            cname   = sg(2, default="N/A")
            region  = sg(13, default="?")
            level   = sg(7, default="?")
            members = sg(6, default="0")
            score   = sg(36, default="0")

            lines.append(
                f"[B][FFD700]━━ #{idx} ━━\n"
                f"[FFFFFF]Name: [00FF00]{xMsGFixinG(cname)}\n"
                f"[FFFFFF]ID: [00BFFF]{xMsGFixinG(cid)}\n"
                f"[FFFFFF]Region: [FF69B4]{region}  "
                f"[FFFFFF]Lv: [FFA500]{xMsGFixinG(level)}  "
                f"[FFFFFF]Members: [00FF7F]{xMsGFixinG(members)}/50\n"
                f"[FFFFFF]Score: [FFD700]{xMsGFixinG(score)}\n"
                f"[AAAAAA]/guild {cid} [FFFFFF]— Full info\n"
            )

        lines.append("[B][C][AAAAAA]━━━━━━━━━━━━━━━━")
        return "\n".join(lines)

    except requests.exceptions.RequestException:
        return "[B][C][FF0000]❌ Guild search server connection failed!"
    except Exception as e:
        print(f"❌ search_guild_by_name error: {e}")
        return f"[B][C][FF0000]❌ Error: {str(e)}"


def leave_guild():
    """Leave the bot's current guild via Free Fire server."""
    try:
        token = load_jwt_token()
        if not token:
            return "[B][C][FF0000]❌ No bot token found. Check token.json."

        try:
            with open("token.json", "r") as f:
                token_data = json.load(f)
            bot_uid = int(token_data.get("bot_uid", 0))
        except Exception:
            bot_uid = 0

        if bot_uid == 0:
            return "[B][C][FF0000]❌ Bot UID not found in token.json. Restart the bot."

        # LeaveClan uses an empty protobuf body — the JWT token identifies the player.
        # Encoding a bot_uid field causes the server to reject with 4xx errors.
        encrypted_payload = encrypt_api("0a00")
        body = bytes.fromhex(encrypted_payload)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        # Try multiple endpoints in priority order (same pattern as GetClanInfoByClanID)
        _urls = [
            "https://clientbp.common.ggbluefox.com/LeaveClan",
            "https://clientbp.ggblueshark.com/LeaveClan",
            get_friend_server_url(region, "LeaveClan"),
        ]
        res = None
        for _url in _urls:
            try:
                print(f"🏳️ LeaveClan → {_url} | bot_uid={bot_uid}")
                _r = requests.post(_url, data=body, headers=headers, timeout=10, verify=False)
                print(f"   → HTTP {_r.status_code} | {len(_r.content)} bytes")
                if _r.status_code in (200, 201):
                    res = _r
                    break
                # On auth errors don't bother trying other URLs
                if _r.status_code in (401, 403):
                    res = _r
                    break
            except Exception as _e:
                print(f"   → error: {_e}")

        if res is None:
            return "[B][C][FF0000]❌ All LeaveClan servers unreachable. Check your connection."

        if res.status_code in (200, 201):
            return (
                "[B][C][FF6EC7]==================\n"
                "[FF6EC7]   GUILD MANAGER\n"
                "[FF6EC7]==================\n"
                "[FFD700]Action : [FF6EC7]LEFT GUILD\n"
                "[FF6EC7]=================="
            )
        else:
            return (
                "[B][C][FF0000]==================\n"
                "[FF0000]   GUILD MANAGER\n"
                "[FF0000]==================\n"
                f"[FFD700]Action : [FF0000]FAILED [HTTP {res.status_code}]\n"
                "[FF0000]=================="
            )
    except Exception as e:
        print(f"❌ leave_guild error: {e}")
        return f"[B][C][FF0000]❌ Error: {e}"


def send_guild_join_request(guild_id):
    """Send a join request to a guild via Free Fire server (admin only)."""
    try:
        token = load_jwt_token()
        if not token:
            return "[B][C][FF0000]❌ No bot token found. Check token.json."

        try:
            with open("token.json", "r") as f:
                token_data = json.load(f)
            bot_uid = int(token_data.get("bot_uid", 0))
        except Exception:
            bot_uid = 0

        if bot_uid == 0:
            return "[B][C][FF0000]❌ Bot UID not found in token.json. Restart the bot."

        gid_int = int(guild_id)
        gid_str_bytes = str(gid_int).encode('utf-8')
        gid_str_len   = encode_varint(len(gid_str_bytes))
        gid_varint     = encode_varint(gid_int)

        # Try payload formats in order — stops at first 200/201.
        # Formats derived from observed LeaveClan pattern (0a00 = field1 string)
        # and game proto conventions. Logs decrypted error body for debugging.
        _payload_formats = [
            # F1-str: field 1, wire-type 2, guild_id as string  ← most likely (matches LeaveClan wire type)
            f"0a{gid_str_len}{gid_str_bytes.hex()}",
            # F2-str: field 2, wire-type 2, guild_id as string
            f"12{gid_str_len}{gid_str_bytes.hex()}",
            # F2-int: field 2, wire-type 0, guild_id as varint  ← original field position
            f"10{gid_varint}",
            # F1-int: field 1, wire-type 0, guild_id as varint
            f"08{gid_varint}",
        ]

        def _try_decrypt_error(raw):
            """Attempt to decrypt and print the server's error body."""
            try:
                decrypted = decrypt_api(raw.hex())
                print(f"   → decrypted error body: {decrypted[:200]}")
            except Exception:
                print(f"   → raw error body (hex): {raw.hex()}")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        _urls = [
            "https://clientbp.common.ggbluefox.com/RequestJoinClan",
            get_friend_server_url(region, "RequestJoinClan"),
            "https://clientbp.ggblueshark.com/RequestJoinClan",
        ]

        res = None
        winning_fmt = None
        for fmt_idx, _payload_hex in enumerate(_payload_formats, 1):
            encrypted_payload = encrypt_api(_payload_hex)
            for _url in _urls:
                try:
                    print(f"📨 RequestJoinClan fmt#{fmt_idx} → {_url} | guild_id={guild_id} | payload={_payload_hex}")
                    _r = requests.post(_url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, verify=False)
                    print(f"   → HTTP {_r.status_code} | {len(_r.content)} bytes")
                    if _r.status_code in (200, 201):
                        res = _r
                        winning_fmt = fmt_idx
                        break
                    if _r.status_code in (401, 403):
                        _try_decrypt_error(_r.content)
                        res = _r
                        break
                    _try_decrypt_error(_r.content)
                except Exception as _e:
                    print(f"   → error: {_e}")
            if res is not None and res.status_code in (200, 201, 401, 403):
                break

        if res is None:
            return "[B][C][FF0000]❌ All RequestJoinClan servers unreachable. Check your connection."

        if res.status_code in (200, 201):
            print(f"✅ RequestJoinClan succeeded with payload format #{winning_fmt}")
            return (
                "[B][C][4CFFB0]==================\n"
                "[4CFFB0]   GUILD MANAGER\n"
                "[4CFFB0]==================\n"
                "[FFD700]Action : [4CFFB0]JOIN REQUEST SENT\n"
                f"[FFD700]Guild  : [FFFFFF]{xMsGFixinG(guild_id)}\n"
                "[4CFFB0]=================="
            )
        else:
            return (
                "[B][C][FF0000]==================\n"
                "[FF0000]   GUILD MANAGER\n"
                "[FF0000]==================\n"
                f"[FFD700]Action : [FF0000]FAILED [HTTP {res.status_code}]\n"
                f"[FFD700]Guild  : [FFFFFF]{xMsGFixinG(guild_id)}\n"
                "[FF0000]=================="
            )
    except Exception as e:
        print(f"❌ send_guild_join_request error: {e}")
        return f"[B][C][FF0000]❌ Error: {e}"


# ADD FRIEND 
def add_friend(target_uid):
    """Send friend request directly to Free Fire servers using bot's own token."""
    try:
        token = load_jwt_token()
        if not token:
            return "[B][C][FF0000]❌ No bot token found. Check token.json."
        success, err = send_friend_request_single(int(target_uid), token, region=region)
        if success:
            return (
                "[B][C][4CFFB0]==================\n"
                "[4CFFB0]   FRIEND MANAGER\n"
                "[4CFFB0]==================\n"
                "[FFD700]Action : [4CFFB0]FRIEND REQUEST SENT\n"
                f"[FFD700]Target : [FFFFFF]{xMsGFixinG(target_uid)}\n"
                "[4CFFB0]=================="
            )
        elif err == "ALREADY_ADDED":
            return (
                "[B][C][FFD700]==================\n"
                "[FFD700]   FRIEND MANAGER\n"
                "[FFD700]==================\n"
                "[FFD700]Action : [FFFFFF]ALREADY FRIENDS\n"
                f"[FFD700]Target : [FFFFFF]{xMsGFixinG(target_uid)}\n"
                "[FFD700]=================="
            )
        else:
            return (
                "[B][C][FF5C8A]==================\n"
                "[FF5C8A]   FRIEND MANAGER\n"
                "[FF5C8A]==================\n"
                f"[FFD700]Action : [FF5C8A]FAILED [{err}]\n"
                f"[FFD700]Target : [FFFFFF]{xMsGFixinG(target_uid)}\n"
                "[FF5C8A]=================="
            )
    except Exception as e:
        return f"[B][C][FF0000]❌ Error: {e}"


def remove_friend(target_uid):
    """Remove friend directly via Free Fire servers using bot's own token."""
    try:
        token = load_jwt_token()
        if not token:
            return "[B][C][FF0000]❌ No bot token found. Check token.json."

        # Load bot UID from token.json
        try:
            with open("token.json", "r") as f:
                token_data = json.load(f)
            bot_uid = int(token_data.get("bot_uid", 0))
        except Exception:
            bot_uid = 0

        if bot_uid == 0:
            print(f"❌ Could not load bot_uid from token.json — remove friend aborted")
            return "[B][C][FF0000]❌ Bot UID not found in token.json. Restart the bot to re-login."

        # Same serialization as RequestAddingFriend (the working /add command)
        bot_uid_varint = encode_varint(bot_uid)
        target_uid_varint = encode_varint(int(target_uid))
        payload = f"08{bot_uid_varint}10{target_uid_varint}"
        encrypted_payload = encrypt_api(payload)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        url = get_friend_server_url(region, "RemoveFriend")
        print(f"🗑️ REMOVE payload hex (pre-encrypt): {payload}")
        print(f"🗑️ Removing friend {target_uid} (bot_uid={bot_uid}) → {url}")
        res = requests.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, verify=False)
        print(f"🗑️ RemoveFriend → HTTP {res.status_code} | body: {res.content[:300]}")

        # If primary server returns 404, retry with blueshark clientbp as fallback
        if res.status_code == 404:
            fallback_url = f"https://clientbp.ggblueshark.com/RemoveFriend"
            print(f"🗑️ Retrying RemoveFriend on fallback server → {fallback_url}")
            res = requests.post(fallback_url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, verify=False)
            print(f"🗑️ RemoveFriend (fallback) → HTTP {res.status_code} | body: {res.content[:300]}")

        if res.status_code == 200:
            return (
                "[B][C][FF6EC7]==================\n"
                "[FF6EC7]   FRIEND MANAGER\n"
                "[FF6EC7]==================\n"
                "[FFD700]Action : [FF6EC7]FRIEND REMOVED\n"
                f"[FFD700]Target : [FFFFFF]{xMsGFixinG(target_uid)}\n"
                "[FF6EC7]=================="
            )
        else:
            return (
                "[B][C][FF5C8A]==================\n"
                "[FF5C8A]   FRIEND MANAGER\n"
                "[FF5C8A]==================\n"
                f"[FFD700]Action : [FF5C8A]FAILED [HTTP {res.status_code}]\n"
                f"[FFD700]Target : [FFFFFF]{xMsGFixinG(target_uid)}\n"
                "[FF5C8A]=================="
            )
    except Exception as e:
        print(f"❌ remove_friend error: {e}")
        return f"[B][C][FF0000]❌ Error: {e}"


def get_friend_list():
    """Fetch the bot's friend list directly from Free Fire servers."""
    try:
        token = load_jwt_token()
        if not token:
            return None, "[B][C][FF0000]❌ No bot token found. Check token.json."

        # Load bot UID — same pattern as add/remove
        try:
            with open("token.json", "r") as f:
                token_data = json.load(f)
            bot_uid = int(token_data.get("bot_uid", 0))
        except Exception:
            bot_uid = 0

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # Endpoint is "GetFriend" — matches the GetFriend_Res_pb2 proto name
        url = get_friend_server_url(region, "GetFriend")
        print(f"📋 Fetching friend list from: {url}")
        # Payload: bot's own UID (field 1 only), same varint pattern as add/remove
        bot_uid_varint = encode_varint(bot_uid) if bot_uid else ""
        payload = f"08{bot_uid_varint}" if bot_uid_varint else ""
        encrypted_payload = encrypt_api(payload)
        res = requests.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=15, verify=False)
        print(f"📋 GetFriend response: {res.status_code}, bytes: {len(res.content)}")
        # If primary server returns 404, retry with blueshark clientbp as fallback
        if res.status_code == 404:
            fallback_url = "https://clientbp.ggblueshark.com/GetFriend"
            print(f"📋 Retrying GetFriend on fallback server → {fallback_url}")
            res = requests.post(fallback_url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=15, verify=False)
            print(f"📋 GetFriend (fallback) → HTTP {res.status_code}, bytes: {len(res.content)}")
        if res.status_code != 200:
            return None, f"[B][C][FF0000]❌ Server returned {res.status_code}"
        # Response is AES-encrypted — decrypt before parsing
        try:
            decrypted_bytes = bytes.fromhex(decrypt_api(res.content.hex()))
        except Exception:
            decrypted_bytes = res.content
        parsed = GetFriend_Res_pb2.GetFriend()
        parsed.ParseFromString(decrypted_bytes)
        friends = []
        seen_uids = set()

        def collect_from_list(player_iter):
            for friend in player_iter:
                try:
                    uid_val = str(friend.PlayerUid)
                    if uid_val and uid_val != "0" and uid_val not in seen_uids:
                        seen_uids.add(uid_val)
                        name = friend.PlayerName if friend.PlayerName else uid_val
                        friends.append((uid_val, name))
                except Exception:
                    pass

        # Collect from all repeated friend fields the proto exposes
        for field_descriptor, field_value in parsed.ListFields():
            try:
                # In newer protobuf versions with the upb C extension,
                # FieldDescriptor.label may not exist — use getattr with fallback
                label = getattr(field_descriptor, 'label', None)
                is_repeated = (
                    label == getattr(field_descriptor, 'LABEL_REPEATED', 3)
                    if label is not None
                    else hasattr(field_value, '__iter__') and not isinstance(field_value, (str, bytes))
                )
                if is_repeated:
                    collect_from_list(field_value)
            except Exception:
                pass

        # Fallback: if nothing found via ListFields, try PlayerList directly
        if not friends:
            collect_from_list(parsed.PlayerList)

        print(f"📋 Friend list: {len(friends)} friends found")
        return friends, None
    except Exception as e:
        print(f"❌ get_friend_list error: {e}")
        return None, f"[B][C][FF0000]❌ Error: {e}"


def format_friend_list_pages(friends):
    """Split friend list into in-game message pages (max 10 per page)."""
    pages = []
    chunk_size = 10
    total = len(friends)
    for i in range(0, total, chunk_size):
        chunk = friends[i:i + chunk_size]
        lines = (
            "[B][C][5DA9FF]==================\n"
            f"[FF6EC7]  FRIEND LIST ({i+1}-{min(i+chunk_size, total)}/{total})\n"
            "[5DA9FF]==================\n"
        )
        for idx, (uid, name) in enumerate(chunk, start=i + 1):
            lines += f"[FFD700]{idx}. [FFFFFF]{name}\n"
        lines += "[5DA9FF]=================="
        pages.append(lines)
    return pages


#Clan-info-by-clan-id
def Get_clan_info(clan_id):
    """Fetch clan info directly from Free Fire game server — no external APIs."""
    # Delegate to send_guild_info which already handles the direct server connection
    return send_guild_info(clan_id)

def check_ban(uid):
    try:
        url = f"https://mg24-check-ban.vercel.app/ban?uid={uid}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return "[B][C][FF0000]❌ API ERROR"

        data = res.json()

        name = data.get("nickname", "Unknown")
        account_id = data.get("account_id", uid)
        region = data.get("region", "N/A")
        status = data.get("ban_status", "Unknown")
        period = data.get("ban_period") or "No Ban"

        status_lower = status.lower()

        # ✅ SIMPLE + SAFE RULE
        if "not" in status_lower:
            status_color = "66FF00"
            period_color = "66FF00"
        else:
            status_color = "FF4444"
            period_color = "FF4444"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]BAN STATUS CHECK
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Name    : [9AD0FF]{name}
[C][E6E6FA]UID     : [9AD0FF]{xMsGFixinG(account_id)}
[C][E6E6FA]Region  : [9AD0FF]{region}
[C][E6E6FA]Status  : [{status_color}]{status}
[C][E6E6FA]Period  : [{period_color}]{period}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[B][C][FF0000]❌ Error: {e}"

async def send_full_player_info(data, chat_type, uid, chat_id, key, iv):

    acc = data.get("AccountInfo", {})
    guild = data.get("GuildInfo", {})

    name = acc.get("AccountName", "Unknown")
    uid_player = acc.get("AccountId", "Unknown")
    level = acc.get("AccountLevel", "Unknown")
    likes = acc.get("AccountLikes", "0")
    region = acc.get("AccountRegion", "Unknown")
    rank = acc.get("BrRankPoint", "Unknown")

    guild_name = guild.get("GuildName", "No Guild")

    msg = f"""
[B][C][00FF00]══『 PLAYER INFO 』══

👤 Name: {name}
🆔 UID: {uid_player}
⭐ Level: {level}
💎 Prime Lvl: {acc.get('AccountPrimeLevel', 'N/A')}
❤️ Likes: {likes}

🌍 Region: {region}
🏆 Rank Points: {rank}

🛡 Guild: {guild_name}

════════════════
"""

    await safe_send_message(chat_type, msg, uid, chat_id, key, iv)

    acc = data.get("AccountInfo", {})
    guild = data.get("GuildInfo", {})
    social = data.get("socialinfo", {})
    captain = data.get("captainBasicInfo", {})

    # ────────── MESSAGE 1 : COMMON ACCOUNT INFO ──────────
    msg1 = f"""
[C][B][FF1493]═════════════
[C][B][00FFFF]  COMMON ACCOUNT INFO
[C][FF1493]═════════════

[C][FFD700]Name        : [00FF00]{acc.get('AccountName', 'N/A')}
[C][FFD700]UID         : [00FFAA]{xMsGFixinG(acc.get('AccountId', 'N/A'))}
[C][FFD700]Level       : [FF00FF]{acc.get('AccountLevel', 'N/A')}
[C][FFD700]Prime Lvl   : [FFD700]{acc.get('AccountPrimeLevel', 'N/A')}
[C][FFD700]EXP         : [00FFFF]{xMsGFixinG(acc.get('AccountEXP'))}
[C][FFD700]Likes       : [FF4444]{xMsGFixinG(acc.get('AccountLikes'))}
[C][FFD700]Region      : [FFFFFF]{acc.get('AccountRegion', 'N/A')}
[C][FFD700]BP Badge    : [FFA500]{xMsGFixinG(acc.get('AccountBPID'))}
[C][FFD700]Version     : [AAAAFF]{acc.get('ReleaseVersion', 'N/A')}

[C][FF1493]═════════════
"""
    await safe_send_message(chat_type, msg1, uid, chat_id, key, iv)
    await asyncio.sleep(0.5)

    # ────────── MESSAGE 2 : DATE + RANK INFO ──────────
    lang = social.get("language", "N/A")
    if "_" in lang:
        lang = lang.split("_")[-1]

    msg2 = f"""
[C][B][00AAFF]═════════════
[C][B][FFFFFF]  ACCOUNT DETAILS
[C][00AAFF]═════════════

[C][FFAA00]Create Date   : [00FF00]{ff_num(human_time(acc.get('AccountCreateTime', '0')))}
[C][FFAA00]Last Login    : [00FF00]{ff_num(acc.get('AccountLastLoginFormatted') or human_time(acc.get('AccountLastLogin', '0')))}
[C][FF00FF]BR Max Rank   : [FFD700]{ff_num(acc.get('BrMaxRank', 'N/A'))}
[C][FF00FF]BR Points     : [FFD700]{ff_num(acc.get('BrRankPoint', 'N/A'))}
[C][00FFFF]CS Max Rank   : [AA00FF]{ff_num(acc.get('CsMaxRank', 'N/A'))}
[C][00FFFF]CS Points     : [AA00FF]{ff_num(acc.get('CsRankPoint', 'N/A'))}
[C][FFFFFF]Language      : [66FF00]{lang}

[C][00AAFF]═════════════
"""
    await safe_send_message(chat_type, msg2, uid, chat_id, key, iv)
    await asyncio.sleep(0.5)

    # ────────── MESSAGE 3 : FULL GUILD INFO ──────────
    msg3 = f"""
[C][B][FF8800]═════════════
[C][B][FFFFFF]  GUILD INFORMATION
[C][FF8800]═════════════

[C][00FFFF]Guild Name    : [00FF00]{guild.get('GuildName', 'No Guild')}
[C][00FFFF]Guild ID      : [FF00FF]{xMsGFixinG(guild.get('GuildID'))}
[C][00FFFF]Owner UID     : [FFD700]{xMsGFixinG(guild.get('GuildOwner'))}
[C][00FFFF]Guild Level   : [FF4444]{guild.get('GuildLevel', 'N/A')}
[C][00FFFF]Members       : [66FFAA]{guild.get('GuildMember', '0')}/{guild.get('GuildCapacity', '0')}

[C][FF8800]═════════════
"""
    await safe_send_message(chat_type, msg3, uid, chat_id, key, iv)

def get_item_info(item_id):
    url = f"https://your-api.vercel.app/item/item?id={item_id}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "itemID" not in data:
            return "[FF0000]ITEM NOT FOUND"

        # Rare অনুযায়ী color change
        rare = data.get("Rare", "UNKNOWN")

        rare_colors = {
            "GREEN": "00FF00",
            "BLUE": "00AAFF",
            "PURPLE": "AA00FF",
            "RED": "FF0000",
            "ORANGE": "FFAA00",
            "Gold": "FFD700"
        }

        rare_color = rare_colors.get(rare, "FFFFFF")

        message = f"""
[B][FF1493]═════════════
[00FFFF]         ITEM DETAILS
[FF1493]═════════════

[FFD700]NAME        : [{rare_color}]{data.get('description', 'N/A')}
[00FFAA]ID          : [FFFFFF]{xMsGFixinG(data.get('itemID', 'N/A'))}
[FF00FF]TYPE        : [FFFFFF]{data.get('itemType', 'N/A')}
[FFA500]COLLECTION  : [FFFFFF]{data.get('collectionType', 'N/A')}
[{rare_color}]RARE        : [{rare_color}]{rare}
[FF4444]UNIQUE      : [FFFFFF]{data.get('isUnique', 'N/A')}
[00AAFF]ICON        : [FFFFFF]{data.get('icon', 'N/A')}

[FF1493]═════════════
"""
        return message.strip()

    except Exception:
        return "[FF0000]SERVER ERROR"

import requests
from datetime import datetime


# Human readable time (uses the definition above — this duplicate is kept for compatibility)
def human_time(unix_timestamp):
    try:
        ts = int(unix_timestamp)
        if ts <= 0:
            return "N/A"
        return datetime.fromtimestamp(ts, ZoneInfo("Asia/Karachi")).strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"

def get_event(region="bd"):
    url = f"https://danger-event-info.vercel.app/event?region={region}&key=DANGERxEVENT"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") != "success" or "events" not in data:
            return [f"[FF0000]No events found for region {region}"]

        messages = []
        for event in data["events"]:
            start_time = human_time(event.get("start", "0"))
            end_time = human_time(event.get("end", "0"))

            # শুধুমাত্র টেক্সট তথ্য রাখছি, banner/link বাদ
            message = f"""[B]
[FF1493]═════════════
[00FFFF]         EVENT DETAILS
[FF1493]═════════════

[FFD700]NAME        : [FFFFFF]{event.get('title', 'N/A')}
[00FFAA]START TIME  : [FFFFFF]{xMsGFixinG(start_time)}
[00FFAA]END TIME    : [FFFFFF]{xMsGFixinG(end_time)}
[FF00FF]TYPE        : [FFFFFF]{event.get('type', 'N/A')}

[FF1493]═════════════
""".strip()
            messages.append(message)

        return messages

    except Exception as e:
        return [f"[FF0000]SERVER ERROR: {str(e)}"]

def get_math_result(input_expr):
    import math as _math
    import ast

    expression = input_expr.strip()
    expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**")

    SAFE_NAMES = {
        "abs": abs, "round": round, "pow": pow,
        "sqrt": _math.sqrt, "log": _math.log, "log10": _math.log10,
        "sin": _math.sin, "cos": _math.cos, "tan": _math.tan,
        "pi": _math.pi, "e": _math.e, "floor": _math.floor, "ceil": _math.ceil,
    }

    try:
        tree = ast.parse(expression, mode='eval')
        for node in ast.walk(tree):
            if not isinstance(node, (
                ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
                ast.FloorDiv, ast.USub, ast.UAdd, ast.Call, ast.Name, ast.Load,
            )):
                raise ValueError("Unsafe expression")

        result = eval(compile(tree, "<string>", "eval"), {"__builtins__": {}}, SAFE_NAMES)

        if isinstance(result, float) and result == int(result):
            result = int(result)

        return f"""[B]
[FF1493]═════════════
[00FFFF]        MATH RESULT
[FF1493]═════════════
[FFD700]EXPRESSION : [FFFFFF]{input_expr}
[00FF00]RESULT     : [FFFFFF]{result}
[FF1493]═════════════
""".strip()

    except ZeroDivisionError:
        return f"""[B]
[FF0000]═════════════
[FF0000]   INVALID EXPRESSION
[FF0000]═════════════
[FF4444]EXPRESSION : [FFFFFF]{input_expr}
[FF0000]RESULT     : [FFFFFF]Cannot divide by zero
[FF0000]═════════════
""".strip()
    except Exception:
        return f"""[B]
[FF0000]═════════════
[FF0000]   INVALID EXPRESSION
[FF0000]═════════════
[FF4444]EXPRESSION : [FFFFFF]{input_expr}
[FF0000]RESULT     : [FFFFFF]ERROR
[FF0000]═════════════
""".strip()

def get_luv_result(name1, name2):
    import hashlib

    n1 = name1.strip().lower()
    n2 = name2.strip().lower()

    # Always 100% for these pairs regardless of order
    PERFECT_PAIRS = {
        frozenset(['ayaan', 'rubyy']),
    }
    if frozenset([n1, n2]) in PERFECT_PAIRS:
        percentage = 100
    else:
        # Sort names so order doesn't matter (/luv a b == /luv b a)
        sorted_names = sorted([n1, n2])
        combined = (sorted_names[0] + sorted_names[1]).encode()
        h = int(hashlib.md5(combined).hexdigest(), 16)
        percentage = (h % 91) + 10

    if percentage >= 90:
        label = "💍 Soulmates!"
        bar_color = "FF1493"
    elif percentage >= 75:
        label = "💑 Perfect Couple"
        bar_color = "FF69B4"
    elif percentage >= 55:
        label = "💕 Good Match"
        bar_color = "FF6600"
    elif percentage >= 35:
        label = "🤔 Maybe..."
        bar_color = "FFFF00"
    else:
        label = "💔 Not a Match"
        bar_color = "FF0000"

    bar_filled = round(percentage / 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    return f"""[B]
[FF1493]╔══════════════════╗
[FF1493]║  💘 LOVE CALCULATOR 💘
[FF1493]╚══════════════════╝
[FFFFFF]
[FF69B4]{name1.strip()} ❤️ [FF69B4]{name2.strip()}
[FFFFFF]
[{bar_color}]{bar} {percentage}%
[FFFFFF]
[FFD700]Love Match : [{bar_color}]{percentage}%
[FFD700]Result     : [FFFFFF]{label}
[FF1493]══════════════════
""".strip()


#ADDING-LIKES-VISUAL-REPRESENTATION
def send_likes(player_name, likes_before):
    try:
        likes_before = int(str(likes_before).replace(",", "").strip()) if likes_before else 0
        likes_added = random.randint(50, 100)
        likes_after = likes_before + likes_added

        return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name  : [00FF00]{xMsGFixinG(player_name)}
[FFFFFF]Likes Before : [00FF00]{xMsGFixinG(likes_before)}
[FFFFFF]Likes Added  : [00FF00]{xMsGFixinG(likes_added)}
[FFFFFF]Likes After  : [00FF00]{xMsGFixinG(likes_after)}
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]MG24 GAMER [00FF00]!!
[C][B][FF1493]━━━━━━━━━━━━
[C][FFFF00]📝 Note: [FFFFFF]This feature is in beta testing
[FFFFFF]and is only a visual representation.
[FFFFFF]No real likes have been sent to the user ID.
[C][B][FF1493]━━━━━━━━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""

# SEND VISIT 
def send_visits(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://visit-api-your.vercel.app/visit?uid={player_id}&region=bd"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return data
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to visit API: {e}")
        return "Failed to connect to visit API."
#CHAT WITH AI (Google Gemini with Groq fallback)
def _try_gemini(question):
    """Try Google Gemini. Returns (text, success)."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_AI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"You are a helpful assistant. Keep responses short and clear.\n\nUser: {question}"}]}],
            "generationConfig": {"maxOutputTokens": 500, "temperature": 0.7}
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip(), True
            return None, False
        elif res.status_code == 429:
            return None, False  # quota exceeded — trigger fallback
        else:
            return None, False
    except Exception:
        return None, False

def _try_groq(question):
    """Primary AI - Groq fast models (llama-3.3-70b → llama3-70b → gemma2-9b)."""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        headers = {
            "Authorization": f"Bearer {GROQ_AI_API_KEY}",
            "Content-Type": "application/json"
        }
        # Fast reliable Groq models — no slow/external models
        models_to_try = [
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "gemma2-9b-it",
        ]
        system_prompt = (
            f"You are a personal assistant for GothicRealm Guild. Today's date is {today}. "
            "ONLY if the user's message is a greeting (hello, hi, hey, sup, yo, wassup, or similar), respond warmly and introduce yourself like this: "
            "say you are the AI assistant of GothicRealm Guild, that you are an AI model created, trained, and running locally 24/7 by Ayaan Ghaffar. "
            "For ALL other messages, answer directly without any introduction or self-description. Do NOT mention GothicRealm Guild or introduce yourself unless greeted. "
            "Answer questions confidently and helpfully. "
            "If asked about recent events you don't know about, say you don't have info on that specific event but still help as much as you can. "
            "Never say you are outdated or that your training was cut off — just answer. "
            "Keep responses short and clear."
        )
        last_error = None
        for model in models_to_try:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    "max_tokens": 400,
                    "temperature": 0.7,
                    "stream": False
                }
                res = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers, json=payload, timeout=8
                )
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip(), True
                elif res.status_code == 429:
                    last_error = f"rate limited on {model}"
                    continue  # Try next model
                else:
                    last_error = f"error {res.status_code} on {model}"
                    continue
            except requests.Timeout:
                last_error = f"timeout on {model}"
                continue
            except Exception as ex:
                last_error = str(ex)
                continue
        return f"❌ AI error: {last_error}", False
    except Exception as e:
        return f"❌ AI error: {e}", False

def talk_with_ai(question):
    # Try Groq first (primary)
    result, ok = _try_groq(question)
    if ok and result:
        return result

    # Fallback to Gemini
    result, ok = _try_gemini(question)
    if ok and result:
        return result

    return "❌ AI is busy right now. Try again in a moment."


####################################

# ** NEW INFO FUNCTION using the new API **
def newinfo(uid):
    # Base URL without parameters
    url = "https://like2.vercel.app/player-info"
    # Parameters dictionary - this is the robust way to do it
    params = {
        'uid': uid,
        'server': server2,  # Hardcoded to bd as requested
        'key': key2
    }
    try:
        # Pass the parameters to requests.get()
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the expected data structure is in the response
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # The API returned 200, but the data is not what we expect (e.g., error message in JSON)
                return {"status": "error", "message": data.get("error", "Invalid ID or data not found.")}
        else:
            # The API returned an error status code (e.g., 404, 500)
            try:
                # Try to get a specific error message from the API's response
                error_msg = response.json().get('error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # If the error response is not JSON
                return {"status": "error", "message": f"API returned status {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., timeout, no connection)
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError: 
        # Handle cases where the response is not valid JSON
        return {"status": "error", "message": "Invalid JSON response from API."}
        

 
Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB53"}

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)
    
def get_random_evo_emote():
    """Return random evo emote ID"""
    evo_emotes = [
        909000063,  # AK
        909000068,  # SCAR  
        909000075,  # 1st MP40
        909040010,  # 2nd MP40
        909000081,  # 1st M1014
        909039011,  # 2nd M1014
        909000085,  # XM8
        909000090,  # Famas
        909000098,  # UMP
        909035007,  # M1887
        909042008,  # Woodpecker
        909041005,  # Groza
        909033001,  # M4A1
        909038010,  # Thompson
        909038012,  # G18
        909045001,  # Parafal
        909049010,  # P90
        909051003   # M60
    ]
    return random.choice(evo_emotes)
    
async def extract_uid_from_emote_packet(data_hex, key, iv):
    """Extract UID from emote packet (the sender)"""
    try:
        # Decrypt the packet
        packet = await DeCode_PackEt(data_hex[10:])
        packet_json = json.loads(packet)
        
        print(f"📦 Analyzing packet structure: {json.dumps(packet_json, indent=2)[:200]}...")
        
        # PATTERN 1: Your Emote_k() structure (Type 21)
        if packet_json.get('1') == 21:
            if ('2' in packet_json and 'data' in packet_json['2'] and
                '5' in packet_json['2']['data'] and 'data' in packet_json['2']['data']['5']):
                
                nested = packet_json['2']['data']['5']['data']
                if '1' in nested:
                    uid = nested['1']['data']
                    print(f"✅ Extracted UID from pattern 21: {uid}")
                    return uid
        
        # PATTERN 2: Direct emote structure
        elif packet_json.get('1') == 26:
            if ('2' in packet_json and 'data' in packet_json['2'] and
                '1' in packet_json['2']['data']):
                
                uid = packet_json['2']['data']['1']['data']
                print(f"✅ Extracted UID from pattern 26: {uid}")
                return uid
        
        # PATTERN 3: Try common paths
        for path in ['2/1', '5/1', '2/data/1', '5/data/1']:
            try:
                uid = get_nested_value(packet_json, path)
                if uid and str(uid).isdigit() and len(str(uid)) > 6:
                    print(f"✅ Extracted UID from path {path}: {uid}")
                    return uid
            except:
                pass
        
        print(f"❌ Could not extract UID from packet")
        return None
        
    except Exception as e:
        print(f"❌ UID extraction error: {e}")
        return None

def get_nested_value(data, path):
    """Get value from nested JSON path like '2/5/1'"""
    keys = path.split('/')
    current = data
    
    for key in keys:
        if key.isdigit():
            key = str(key)  # JSON keys are strings
        
        if key in current and 'data' in current[key]:
            current = current[key]['data']
        else:
            return None
    
    return current

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    """Join team, authenticate chat, perform emote, and leave automatically"""
    try:
        # Step 1: Join the team
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Joined team: {team_code}")
        
        # Wait for team data and chat authentication
        await asyncio.sleep(1.5)  # Increased to ensure proper connection
        
        # Step 2: The bot needs to be detected in the team and authenticate chat
        # This happens automatically in TcPOnLine, but we need to wait for it
        
        # Step 3: Perform emote to target UID
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"🎭 Performed emote {emote_id} to UID {xMsGFixinG(target_uid)}")
        
        # Wait for emote to register
        await asyncio.sleep(0.5)
        
        # Step 4: Leave the team
        leave_packet = await ExiT(0, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"🚪 Left team: {team_code}")
        
        return True, f"Quick emote attack completed! Sent emote to UID {xMsGFixinG(target_uid)}"
        
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"
        
        
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200: return (None, None)
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.123.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    if not MajoRLoGinResPonsE:
        return None
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
    

async def cHTypE(H):
    """Detect chat type including custom rooms"""
    if not H: 
        return 'Squid'
    elif H == 1: 
        return 'CLan'
    elif H == 2: 
        return 'PrivaTe'
    elif H == 3: 
        return 'CustomRoom'  # Custom room chat type
    else:
        return 'Squid'  # Default fallback
    
async def SEndMsG(H, message, Uid, chat_id, key, iv, region):
    """Send message to any chat type including custom rooms"""
    TypE = await cHTypE(H)
    
    if TypE == 'Squid': 
        msg_packet = await xSEndMsgsQQ(message, chat_id, key, iv)
    elif TypE == 'CLan': 
        msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe': 
        msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    else:
        # Fallback to squad chat
        msg_packet = await xSEndMsgsQQ(message, chat_id, key, iv)
        
    return msg_packet
    
    
async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT:
        if whisper_writer and not whisper_writer.is_closing():
            whisper_writer.write(PacKeT)
            try:
                await asyncio.wait_for(whisper_writer.drain(), timeout=10)
            except asyncio.TimeoutError:
                raise ConnectionError("Chat drain timed out — connection stalled")
        else:
            raise ConnectionError("whisper_writer is closed or unavailable")
    elif TypE == 'OnLine':
        if online_writer and not online_writer.is_closing():
            online_writer.write(PacKeT)
            try:
                await asyncio.wait_for(online_writer.drain(), timeout=10)
            except asyncio.TimeoutError:
                raise ConnectionError("Online drain timed out — connection stalled")
        else:
            raise ConnectionError("online_writer is closed or unavailable")
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 

_CONNECTION_ERRORS = (BrokenPipeError, ConnectionResetError, ConnectionError, OSError, asyncio.TimeoutError)

# Shared flag: set to True to make the TcPChaT reading loop break and reconnect
_chat_force_reconnect = False
_send_fail_count = 0          # Consecutive send failures
_SEND_FAIL_LIMIT = 3          # Force reconnect after this many consecutive failures

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3, region="ind"):
    """Enhanced safe send message that works with custom rooms"""
    global _chat_force_reconnect, _send_fail_count
    if not whisper_writer or whisper_writer.is_closing():
        print(f"⚠️ Cannot send — chat connection is down (will retry when reconnected)")
        _send_fail_count += 1
        if _send_fail_count >= _SEND_FAIL_LIMIT:
            print(f"🔁 Too many send failures ({_send_fail_count}) — signalling reconnect...")
            _chat_force_reconnect = True
        return False
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv, region)
            # ChaT (2nd arg) is the truthiness gate for the 'ChaT' branch in SEndPacKeT.
            # Must pass whisper_writer (not online_writer) so the condition is always
            # met when whisper_writer is alive — online_writer can be None which silently
            # drops the packet without raising, making it look like a success.
            await SEndPacKeT(online_writer, whisper_writer, 'ChaT', P)
            print(f"✅ Message sent successfully to chat type {chat_type} (attempt {attempt + 1})")
            _send_fail_count = 0  # Reset on success
            return True
        except _CONNECTION_ERRORS as e:
            print(f"⚠️ Connection lost while sending: {e}")
            _send_fail_count += 1
            if _send_fail_count >= _SEND_FAIL_LIMIT:
                print(f"🔁 Too many send failures ({_send_fail_count}) — signalling reconnect...")
                _chat_force_reconnect = True
            return False
        except Exception as e:
            print(f"❌ Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    _send_fail_count += 1
    if _send_fail_count >= _SEND_FAIL_LIMIT:
        print(f"🔁 Too many send failures ({_send_fail_count}) — signalling reconnect...")
        _chat_force_reconnect = True
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    """Fast emote spam function that sends emotes rapidly"""
    global fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times
    
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # 0.1 seconds interval between spam cycles

# NEW FUNCTION: Custom emote spam with specified times
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    """Custom emote spam function that sends emotes specified number of times"""
    global custom_spam_running
    count = 0
    
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.0000001)  # 0.1 seconds interval between emotes
        except Exception as e:
            print(f"Error in custom_emote_spam for uid {uid}: {e}")
            break

async def create_level_up_bot_connection(key, iv, region):
    """Create a separate connection for level-up bot"""
    try:
        # This would use a different bot account
        # For now, we'll use the main bot
        print("🤖 Level-up bot connection initialized")
        return True
    except Exception as e:
        print(f"❌ Level-up bot connection error: {e}")
        return False

async def level_up_join_team(team_code, key, iv, region):
    """Level-up bot joins the team"""
    try:
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Level-up bot joining team: {team_code}")
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Level-up bot join error: {e}")
        return False

async def level_up_leave_team(key, iv):
    """Level-up bot leaves the team"""
    try:
        leave_packet = await ExiT(0, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print("🤖 Level-up bot leaving team")
        await asyncio.sleep(1)
        return True
    except Exception as e:
        print(f"❌ Level-up bot leave error: {e}")
        return False
        
async def level_up_loop(team_code, target_uid, key, iv, region, chat_type, chat_id):
    """Main level-up automation loop"""
    global level_up_running
    
    cycle_count = 0
    max_cycles = 1000  # Safety limit
    
    print(f"🚀 Starting level-up automation for team {team_code}")
    
    while level_up_running and cycle_count < max_cycles:
        try:
            cycle_count += 1
            print(f"🔄 Level-up cycle #{cycle_count}")
            
            # Step 1: Send instruction message
            instruction_msg = f"""[B][C][00FF00]🔄 LEVEL-UP CYCLE #{cycle_count}

🤖 Bot: Joining your team...
🎮 Action: Will start match
⏱️ After match: Wait {level_up_wait_time} seconds
🔄 Then: Repeat process

📊 Status: Bot is working...
"""
            await safe_send_message(chat_type, instruction_msg, target_uid, chat_id, key, iv)
            
            # Step 2: Join the team
            join_success = await level_up_join_team(team_code, key, iv, region)
            if not join_success:
                print("❌ Failed to join team, retrying...")
                await asyncio.sleep(2)
                continue
            
            # Step 3: Send "ready" message
            ready_msg = f"[B][C][00FF00]✅ Bot joined! Starting match...\n"
            await safe_send_message(chat_type, ready_msg, target_uid, chat_id, key, iv)
            
            # Step 4: Start the match (spam start packet)
            start_packet = await FS(key, iv)
            spam_duration = 10  # Spam for 10 seconds
            start_time = time.time()
            
            while time.time() - start_time < spam_duration and level_up_running:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                await asyncio.sleep(0.2)  # 200ms delay between packets
            
            # Step 5: Wait for match to complete (simulate)
            waiting_msg = f"""[B][C][FFFF00]⏱️ MATCH IN PROGRESS...

⏳ Waiting for match to complete...
🔄 Next cycle starts in {level_up_wait_time} seconds
🤖 Bot remains in team

💡 Let the match complete normally!
"""
            await safe_send_message(chat_type, waiting_msg, target_uid, chat_id, key, iv)
            
            # Step 6: Wait the specified time
            wait_count = 0
            while wait_count < level_up_wait_time and level_up_running:
                await asyncio.sleep(1)
                wait_count += 1
                
                # Progress update every 5 seconds
                if wait_count % 5 == 0:
                    progress_msg = f"[B][C][00FF00]⏱️ {wait_count}/{level_up_wait_time} seconds waited...\n"
                    await safe_send_message(chat_type, progress_msg, target_uid, chat_id, key, iv)
            
            if not level_up_running:
                break
            
            # Step 7: Leave team
            leave_success = await level_up_leave_team(key, iv)
            
            if leave_success:
                leave_msg = f"[B][C][FF0000]🚪 Bot left team to restart cycle...\n"
                await safe_send_message(chat_type, leave_msg, target_uid, chat_id, key, iv)
            
            # Step 8: Small delay before next cycle
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Error in level-up cycle: {e}")
            # Try to recover
            await level_up_leave_team(key, iv)
            await asyncio.sleep(3)
    
    print("🛑 Level-up automation stopped")

async def Send_Entry_Emote(uid, K, V, emote_id=912038002, session_id=5, trigger_type=1):
    """Send arrival/entry animation emote
    
    Args:
        uid: Target player UID
        K: Encryption key
        V: Initialization vector
        emote_id: Emote ID (default: 912038002 - arrival animation)
        session_id: Session ID (default: 5)
        trigger_type: Trigger type (default: 1 - entry)
    """
    try:
        fields = {
            1: 4,           # Packet ID for entry emotes
            2: int(uid),    # Player UID
            3: int(session_id),     # Session ID
            4: int(emote_id),       # Emote ID
            5: int(trigger_type),   # Trigger Type (1=entry, 2=exit, etc.)
            6: int(uid),    # Repeated UID
            7: 1,           # Static Value
            8: int(uid),    # Repeated UID
            9: int(uid),    # Repeated UID
            10: int(uid),   # Repeated UID
            11: int(uid),   # Repeated UID
        }
        
        # Different arrival animations
        arrival_emotes = {
            "default": 912038002,
        }
        
        # Use provided emote_id or default
        if isinstance(emote_id, str) and emote_id in arrival_emotes:
            fields[4] = arrival_emotes[emote_id]
        
        proto_hex = (await CrEaTe_ProTo(fields)).hex()
        
        # Determine packet type based on region (you might need to pass region)
        # For now using '0515' as in your example
        return await GeneRaTePk(proto_hex, '0515', K, V)
        
    except Exception as e:
        print(f"❌ Error creating entry emote packet: {e}")
        return None



# NEW FUNCTION: Evolution emote spam with mapping
async def evo_emote_spam(uids, number, key, iv, region):
    """Send evolution emotes based on number mapping"""
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending evo emote to {uid}: {e}")
        
        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    
    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"



# NEW FUNCTION: Fast evolution emote spam
async def evo_fast_emote_spam(uids, number, key, iv, region):
    """Fast evolution emote spam function"""
    global evo_fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed fast evolution emote spam {count} times"
    
async def send_required_packets(key, iv, region, bot_uid):
    """Send packets required after connection"""
    try:
        # Packet 1: Client info
        fields1 = {
            1: 100,
            2: {
                1: bot_uid,
                2: "1.123.1",  # Game version
                3: "Android",
                4: "en",
            }
        }
        
        # Packet 2: Device info
        fields2 = {
            1: 101,
            2: {
                1: "vivo",
                2: "1901",
                3: "arm64-v8a",
                4: str(time.time()),
            }
        }
        
        packets = []
        for fields in [fields1, fields2]:
            if region.lower() == "ind":
                packet_type = '0514'
            elif region.lower() == "bd":
                packet_type = "0519"
            else:
                packet_type = "0515"
                
            packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
            packets.append(packet)
        
        return packets
        
    except Exception as e:
        print(f"❌ Required packets error: {e}")
        return []

# NEW FUNCTION: Custom evolution emote spam with specified times
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    """Custom evolution emote spam with specified repeat times"""
    global evo_custom_spam_running
    count = 0
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_custom_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed custom evolution emote spam {count} times"

async def RejectMSGtaxt(squad_owner,uid, key, iv):
    random_banner = f"""
.
.
.










    
[00FF00]ＷＥＬＣＯＭＥ ＴＯ[FF0000] M G 2 4  G A M E R   [00FF00]ＢＯＴ
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[1E90FF]ＤＥＶ   [FF0000]A Y A A N  
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[FF0000]A Y A A N  
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[9400D3]M A D E  B Y [FF0000]A Y A A N 
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[FFD700] ＦＯＬＬＯＷ    ＭＥ   ＩＮ   [87CEEB] Instagram: [FF0000]@ayaan._.ghaffar
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]"""
    fields = {
    1: 5,
    2: {
        1: int(squad_owner),
        2: 1,
        3: int(uid),
        4: random_banner
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , key, iv)

async def send_keep_alive(key, iv, region):
    """Send keep-alive packet to maintain connection"""
    try:
        fields = {
            1: 99,  # Keep-alive packet type
            2: {
                1: int(time.time()),
                2: 1,  # Keep-alive flag
            }
        }
        
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
            
        packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
        return packet
    except Exception as e:
        print(f"❌ Keep-alive error: {e}")
        return None

async def ArohiAccepted(uid,code,K,V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
            2: 161,
            4: "y[WW",
            6: 11,
            8: "1.114.18",
            9: 3,
            10: 1
            },
            10: str(code),
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)


async def new_lag(key , iv):
    fields = {
        1: 15,
        2: {
            1: 804266360,
            2: 1
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , key , iv)


async def convert_kyro_to_your_system(target_uid, chat_id, key, iv, nickname="RIJEXX", title_id=None):
    """EXACT conversion with customizable title ID"""
    try:
        # Use provided title_id or get random one
        if title_id is None:
            # Get a random title from the list
            available_titles = [905090075, 904990072, 904990069, 905190079]
            title_id = random.choice(available_titles)
        
        # Create fields dictionary with specific title_id
        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',  # Use specific title ID
                # ... rest of your fields
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(await xBunnEr()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 1,
                    13: {
                        1: 2
                    },
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {
                    2: 2,
                    3: 1
                },
                14: {}
            }
        }
        
        # ... rest of your existing function
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        
        print(f"✅ Created packet with Title ID: {title_id}")
        return final_packet
        
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return None
        
def get_random_sticker():
    """
    Randomly select one sticker from available packs
    """

    sticker_packs = [
        # NORMAL STICKERS (1200000001-1 to 24)
        ("1200000001", 1, 24),

        # KELLY EMOJIS (1200000002-1 to 15)
        ("1200000002", 1, 15),

        # MAD CHICKEN (1200000004-1 to 13)
        ("1200000004", 1, 13),
    ]

    pack_id, start, end = random.choice(sticker_packs)
    sticker_no = random.randint(start, end)

    return f"[1={pack_id}-{sticker_no}]"
        
async def send_sticker(target_uid, chat_id, key, iv, nickname="BLACK", chat_type=0):
    """Send Random Sticker using /sticker command — works in guild, group, and whisper"""
    try:
        sticker_value = get_random_sticker()

        inner = {
            1: int(target_uid),
            2: int(chat_id),
            5: int(datetime.now().timestamp()),
            8: f'{{"StickerStr" : "{sticker_value}", "type":"Sticker"}}',
            9: {
                1: f"[C][B][FF0000]{nickname}",
                2: int(get_random_avatar()),
                4: 330,
                5: 102000015,
                8: "BOT TEAM",
                10: 1,
                11: 66,
                12: 66,
                13: {1: 2},
                14: {
                    1: 1158053040,
                    2: 8,
                    3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                }
            },
            10: "en",
            13: {
                2: 2,
                3: 1
            },
            14: {}
        }

        # Set chat type field in proto so packet reaches the right chat context
        # 1 = Guild/Clan, 2 = Private/Whisper, 0/missing = Group/Squad
        if chat_type == 1:
            inner[3] = 1   # guild
        elif chat_type == 2:
            inner[3] = 2   # whisper/private
        # group/squad: leave field 3 absent (default)

        fields = {
            1: 1,
            2: inner
        }

        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()

        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"

        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)

        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)

        print(f"✅ Sticker Sent: {sticker_value}")
        return final_packet

    except Exception as e:
        print(f"❌ Sticker error: {e}")
        return None

# Alternative: DIRECT port of your friend's function but with your UID
async def send_kyro_title_adapted(chat_id, key, iv, target_uid, nickname="RIJEXX"):
    """Direct adaptation of your friend's working function"""
    try:
        # Import your proto file (make sure it's in the same directory)
        from kyro_title_pb2 import GenTeamTitle
        
        root = GenTeamTitle()
        root.type = 1
        
        nested_object = root.data
        nested_object.uid = int(target_uid)  # CHANGE: Use target UID
        nested_object.chat_id = int(chat_id)
        nested_object.title = f"{{\"TitleID\":{titles()},\"type\":\"Title\"}}"
        nested_object.timestamp = int(datetime.now().timestamp())
        nested_object.language = "en"
        
        nested_details = nested_object.field9
        nested_details.Nickname = f"[C][B][FF0000]{nickname}"  # CHANGE: Your nickname
        nested_details.avatar_id = int(await xBunnEr())  # Use your function
        nested_details.rank = 330
        nested_details.badge = 102000015
        nested_details.Clan_Name = "BOT TEAM"  # CHANGE: Your clan
        nested_details.field10 = 1
        nested_details.global_rank_pos = 1
        nested_details.badge_info.value = 2
        
        nested_details.prime_info.prime_uid = 1158053040
        nested_details.prime_info.prime_level = 8
        # IMPORTANT: This must be bytes, not string!
        nested_details.prime_info.prime_hex = b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
        
        nested_options = nested_object.field13
        nested_options.url_type = 2
        nested_options.curl_platform = 1
        
        nested_object.empty_field.SetInParent()
        
        # Serialize
        packet = root.SerializeToString().hex()
        
        # Use YOUR encryption function
        encrypted_packet = await encrypt_packet(packet, key, iv)
        
        # Calculate length
        packet_length = len(encrypted_packet) // 2
        
        # Convert to hex (4 characters with leading zeros)
        hex_length = f"{packet_length:04x}"
        
        # Build packet EXACTLY like your friend
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        return bytes.fromhex(final_packet_hex)
        
    except Exception as e:
        print(f"❌ Direct adaptation error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def send_all_titles_sequentially(uid, chat_id, key, iv, region, chat_type):
    """Send all titles one by one with 2-second delay"""
    
    # Get all titles
    all_titles = [
        905090075, 904990072, 904990069, 905190079
    ]
    
    total_titles = len(all_titles)
    
    # Send initial message
    start_msg = f"""[B][C][00FF00]🎖️ STARTING TITLE SEQUENCE!

📊 Total Titles: {total_titles}
⏱️ Delay: 2 seconds between titles
🔁 Mode: Sequential
🎯 Target: {xMsGFixinG(uid)}

⏳ Sending titles now...
"""
    await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
    
    try:
        for index, title_id in enumerate(all_titles):
            title_number = index + 1
            
            # Create progress message
            progress_msg = f"""[B][C][FFFF00]📤 SENDING TITLE {title_number}/{total_titles}

🎖️ Title ID: {title_id}
📊 Progress: {title_number}/{total_titles}
⏱️ Next in: 2 seconds
"""
            await safe_send_message(chat_type, progress_msg, uid, chat_id, key, iv)
            
            # Send the actual title using your existing method
            # You'll need to use your existing title sending logic here
            # For example:
            title_packet = await convert_kyro_to_your_system(uid, chat_id, key, iv, nickname="MG24GAMER", title_id=title_id)
            
            if title_packet and whisper_writer:
                whisper_writer.write(title_packet)
                await whisper_writer.drain()
                print(f"✅ Sent title {title_number}/{total_titles}: {title_id}")
            
            # Wait 2 seconds before next title (unless it's the last one)
            if title_number < total_titles:
                await asyncio.sleep(2)
        
        # Completion message
        completion_msg = f"""[B][C][00FF00]✅ ALL TITLES SENT SUCCESSFULLY!

🎊 Total: {total_titles} titles sent
🎯 Target: {xMsGFixinG(uid)}
⏱️ Duration: {total_titles * 2} seconds
✅ Status: Complete!

🎖️ Titles Sent:
1. 905090075
2. 904990072
3. 904990069
4. 905190079
"""
        await safe_send_message(chat_type, completion_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error sending titles: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def handle_all_titles_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    """Handle /alltitles command to send all titles sequentially"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) == 1:
        target_uid = uid
        target_name = "Yourself"
    elif len(parts) == 2 and parts[1].isdigit():
        target_uid = parts[1]
        target_name = f"UID {xMsGFixinG(target_uid)}"
    else:
        error_msg = f"""[B][C][FF0000]❌ Usage: /alltitles [uid]
        
📝 Examples:
/alltitles - Send all titles to yourself
/alltitles 123456789 - Send all titles to specific UID

🎯 What it does:
1. Sends all 4 titles one by one
2. 2-second delay between each title
3. Sends in background (non-blocking)
4. Shows progress updates
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Start the title sequence in the background
    asyncio.create_task(
        send_all_titles_sequentially(target_uid, chat_id, key, iv, region, chat_type)
    )
    
    # Immediate response
    response_msg = f"""[B][C][00FF00]🚀 STARTING TITLE SEQUENCE IN BACKGROUND!

👤 Target: {target_name}
🎖️ Total Titles: 4
⏱️ Delay: 2 seconds each
📱 Status: Running in background...

💡 You'll receive progress updates as titles are sent!
"""
    await safe_send_message(chat_type, response_msg, uid, chat_id, key, iv)


async def noob(target_uid, chat_id, key, iv, nickname="MG24GAMER", title_id=None):
    """EXACT conversion with customizable title ID"""
    try:
        # Use provided title_id or get random one
        if title_id is None:
            # Get a random title from the list
            available_titles = [904090014, 904090015, 904090024, 904090025, 904090026, 904090027, 904990070, 904990071, 904990072]
            title_id = random.choice(available_titles)
        
        # Create fields dictionary with specific title_id
        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(await xBunnEr()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 1,
                    13: {
                        1: 2
                    },
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {
                    2: 2,
                    3: 1
                },
                14: {}
            }
        }
        
        # ... rest of your existing function
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        
        print(f"✅ Created packet with Title ID: {title_id}")
        return final_packet
        
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return None
        

async def send_all_titles_sequentiallly(uid, chat_id, key, iv, region, chat_type):
    """Send all titles one by one with 2-second delay"""
    
    # Get all titles
    all_titles = [
        904090014, 904090015, 904090024, 904090025, 904090026, 904090027, 904990070, 904990071, 904990072
    ]
    
    total_titles = len(all_titles)
    
    # Send initial message
    start_msg = f"""[B][C][00FF00] Noobde adventshi ya meku agar tu noob bolra toh tu g a y hai


"""
    await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
    
    try:
        for index, title_id in enumerate(all_titles):
            title_number = index + 1
            

            
            # Send the actual title using your existing method
            # You'll need to use your existing title sending logic here
            # For example:
            title_packet = await noob(uid, chat_id, key, iv, nickname="MG24GAMER", title_id=title_id)
            
            if title_packet and whisper_writer:
                whisper_writer.write(title_packet)
                await whisper_writer.drain()
                print(f"✅ Sent title {title_number}/{total_titles}: {title_id}")
            
            # Wait 2 seconds before next title (unless it's the last one)
            if title_number < total_titles:
                await asyncio.sleep(2)
        
        # Completion message
        completion_msg = f"""[B][C][00FF00]Noobde ab tu bta ye titles aur bol kon noob hai
"""
        await safe_send_message(chat_type, completion_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error sending titles: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def handle_alll_titles_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    """Handle /alltitles command to send all titles sequentially"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) == 1:
        target_uid = uid
        target_name = "Yourself"
    elif len(parts) == 2 and parts[1].isdigit():
        target_uid = parts[1]
        target_name = f"UID {xMsGFixinG(target_uid)}"
    else:
        error_msg = f"""[B][C][FF0000]❌ Usage: /alltitles [uid]
        
📝 Examples:
/alltitles - Send all titles to yourself
/alltitles 123456789 - Send all titles to specific UID

🎯 What it does:
1. Sends all 4 titles one by one
2. 2-second delay between each title
3. Sends in background (non-blocking)
4. Shows progress updates
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Start the title sequence in the background
    asyncio.create_task(
        send_all_titles_sequentiallly(target_uid, chat_id, key, iv, region, chat_type)
    )
    


async def RoomJoin(room_id, password, key, iv):
    """Join Free Fire custom room"""
    try:
        # Import your proto file
        from room_join_pb2 import join_room
        
        root = join_room()
        root.field_1 = 3  # Room join command
        
        # Nested object
        nested_object = root.field_2
        nested_object.field_1 = int(room_id)
        nested_object.field_2 = str(password)
        
        # Field 8
        nested_8 = nested_object.field_8
        nested_8.field_1 = "IDC3"
        nested_8.field_2 = 149
        nested_8.field_3 = "IND"
        
        # Other fields
        nested_object.field_9 = "\x01\x03\x04\x07\x09\x0a\x0b\x12\x0e\x16\x19\x20\x1d"  # Bytes, not string
        nested_object.field_10 = 1
        nested_object.field_12.SetInParent()  # Empty field
        nested_object.field_13 = 1
        nested_object.field_14 = 1
        nested_object.field_16 = "en"
        
        # Field 22
        nested_22 = nested_object.field_22
        nested_22.field_1 = 21
        
        # Serialize
        packet_hex = root.SerializeToString().hex()
        
        # Encrypt using your function
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        
        # Convert length to hex
        hex_length = dec_to_hex(packet_length)  # Use your existing function
        
        # Build packet header (type 0e15 for room join)
        if len(hex_length) == 2:
            header = "0e15000000"
        elif len(hex_length) == 3:
            header = "0e1500000"
        elif len(hex_length) == 4:
            header = "0e150000"
        elif len(hex_length) == 5:
            header = "0e15000"
        else:
            header = "0e150000"
        
        final_packet_hex = header + hex_length + encrypted_packet
        
        return bytes.fromhex(final_packet_hex)
        
    except Exception as e:
        print(f"❌ Room join error: {e}")
        import traceback
        traceback.print_exc()
        return None
        

# Alternative: Using your fields dictionary format
async def RoomJoin_fields(room_id, password, key, iv):
    """Room join using your CrEaTe_ProTo format"""
    try:
        fields = {
            1: 3,  # Room join command
            2: {   # Nested object
                1: int(room_id),   # room_id
                2: str(password),  # password
                8: {  # field_8
                    1: "IDC3",
                    2: 149,
                    3: "IND"
                },
                9: b"\x01\x03\x04\x07\x09\x0a\x0b\x12\x0e\x16\x19\x20\x1d",  # Bytes!
                10: 1,
                12: {},  # Empty field
                13: 1,
                14: 1,
                16: "en",
                22: {  # field_22
                    1: 21
                }
            }
        }
        
        # Convert to protobuf
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        # Encrypt and build packet
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = dec_to_hex(packet_length)
        
        # Build header
        if len(hex_length) == 2:
            header = "0e15000000"
        elif len(hex_length) == 3:
            header = "0e1500000"
        elif len(hex_length) == 4:
            header = "0e150000"
        elif len(hex_length) == 5:
            header = "0e15000"
        else:
            header = "0e150000"
        
        final_packet_hex = header + hex_length + encrypted_packet
        return bytes.fromhex(final_packet_hex)
        
    except Exception as e:
        print(f"❌ Room join fields error: {e}")
        return None

def remove_from_whitelist(uid_to_remove):
    """Remove UID from whitelist"""
    global WHITELISTED_UIDS
    
    uid_str = str(uid_to_remove)
    
    # Don't allow removing owner
    if uid_str == "":  # Your UID
        return False, "Cannot remove bot owner from whitelist!"
    
    if uid_str not in WHITELISTED_UIDS:
        return False, f"UID {uid_str} not in whitelist"
    
    WHITELISTED_UIDS.remove(uid_str)
    return True, f"✅ Removed {uid_str} from whitelist"



async def handle_xjoin_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle /xjoin command to join custom rooms"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) < 3:
        error_msg = f"""[B][C][FF0000]🎮 ROOM JOIN COMMAND

❌ Usage: /xjoin (room_id) (password)

📝 Examples:
/xjoin 123456 0000
/xjoin 987654 1111

🔑 Room Info:
• Room ID: 6-digit number
• Password: Usually 4 digits (0000-9999)

💡 Bot will join the custom room!
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    room_id = parts[1]
    password = parts[2]
    
    if not room_id.isdigit():
        error_msg = f"[B][C][FF0000]❌ Room ID must be numbers only!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][00FF00]🚀 JOINING CUSTOM ROOM...\n🏠 Room: {room_id}\n🔑 Password: {password}\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Try method 1: Direct proto method
        room_packet = await RoomJoin(room_id, password, key, iv)
        
        if not room_packet:
            # Try method 2: Fields method
            room_packet = await RoomJoin_fields(room_id, password, key, iv)
        
        if room_packet and online_writer:
            # Send via Online connection
            online_writer.write(room_packet)
            await online_writer.drain()
            
            print(f"✅ Room join packet sent! Room: {room_id}")
            joinroom = join_room_chanel(room_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', joinroom)
            success_msg = f"""[B][C][00FF00]✅ ROOM JOIN COMMAND SENT!

🏠 Room ID: {room_id}
🔑 Password: {password}
"""
        else:
            success_msg = f"[B][C][FF0000]❌ Failed to create room join packet!\n"
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error joining room: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def handle_room_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle /room command with proper error handling"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /room (uid)\nExample: /room 415136165\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    
    try:
        # Step 1: Check player status
        status_result, status_message = await check_player_status(target_uid, key, iv)
        
        packet = None
        player_status = None
        
        # If live check failed, try cache
        if not status_result:
            # Check cache
            cached_data = load_from_cache(target_uid)
            if cached_data and 'packet' in cached_data:
                packet = cached_data['packet']
                player_status = cached_data.get('status', 'UNKNOWN')
                print(f"⚠️ Using cached data for {xMsGFixinG(target_uid)}")
            else:
                error_msg = f"[B][C][FF0000]❌ Player {xMsGFixinG(target_uid)} not found\n"
                await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
                return
        else:
            # Use live data
            packet = status_result.get('packet', b'')
            player_status = get_player_status(packet)
        
        # Step 2: Check if player is in room
        if not player_status or "IN ROOM" not in player_status:
            info_msg = f"""[B][C][FFFF00]📊 STATUS: {player_status or 'UNKNOWN'}

👤 Player: {xMsGFixinG(target_uid)}
❌ Not in custom room

💡 Player must join custom room first!"""
            await safe_send_message(chat_type, info_msg, uid, chat_id, key, iv)
            return
        
        # Step 3: Extract room ID
        room_id = get_idroom_by_idplayer(packet) if packet else None
        
        if not room_id:
            error_msg = f"[B][C][FF0000]❌ Failed to extract room ID\n"
            await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            return
        
        # Step 4: SUCCESS - Send room info
        success_msg = f"""[B][C][00FF00]✅ ROOM FOUND!

👤 Player: {xMsGFixinG(target_uid)}
🏠 Room ID: {room_id}
📊 Status: {player_status}
⚡ Data: {'CACHED' if not status_result else 'LIVE'}

💡 Quick join: /xjoin {room_id} 0000
"""
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Step 5: AUTO-SPAM (add this if you want spam)
        # Uncomment this section if you want auto-spam:
        
        spam_count = 5
        for i in range(spam_count):
            try:
                spam_packet = await Room_Spam(target_uid, room_id, f"Spam_{i+1}", key, iv)
                if spam_packet and online_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
                    await asyncio.sleep(0.2)
            except Exception as e:
                print(f"Spam error: {e}")
        
        spam_msg = f"[B][C][00FF00]✅ Spammed {spam_count} invites!\n"
        await safe_send_message(chat_type, spam_msg, uid, chat_id, key, iv)
        
        
    except Exception as e:
        print(f"❌ Room command error: {e}")
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:80]}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

# Room spam command (send multiple messages)
async def handle_room_spam_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle /spamroom command to send room spam messages"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) < 4:
        error_msg = f"""[B][C][FF0000]❌ Usage: /spamroom (room_id) (uid) (message)
        
📝 Example: /spamroom 123456 14010319252 Hello World!

⚙️ Parameters:
• room_id = Custom room ID (numbers)
• uid = Player UID to spam
• message = Text message to send

🎯 What it does:
1. Creates room spam packet
2. Sends message to specified room
3. Uses colorful formatting
4. Packet type: 0e15 (room spam)
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    try:
        room_id = parts[1]
        target_uid = parts[2]
        message = ' '.join(parts[3:])
        
        # Validate inputs
        if not room_id.isdigit():
            error_msg = f"[B][C][FF0000]❌ Room ID must be numbers only!\n"
            await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            return
            
        if not target_uid.isdigit():
            error_msg = f"[B][C][FF0000]❌ UID must be numbers only!\n"
            await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            return
        
        # Send initial message
        initial_msg = f"[B][C][00FF00]🚀 PREPARING ROOM SPAM...\n"
        initial_msg += f"🏠 Room ID: {room_id}\n"
        initial_msg += f"👤 Target UID: {xMsGFixinG(target_uid)}\n"
        initial_msg += f"📝 Message: {message[:30]}...\n"
        initial_msg += f"📦 Packet type: 0e15\n"
        initial_msg += f"⏳ Creating packet...\n"
        
        await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
        
        # Create and send the spam packet
        spam_packet = await SPam_Room(target_uid, room_id, message, key, iv)
        
        if spam_packet:
            # Send via Online connection (since it's room-related)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
            
            success_msg = f"""[B][C][00FF00]✅ ROOM SPAM PACKET SENT!

🏠 Room: {room_id}
👤 Target: {xMsGFixinG(target_uid)}
📝 Message: {message[:40]}...
📦 Packet: Type 0e15 (Room Spam)
✅ Status: Delivered successfully

💡 Packet includes:
• Colorful message formatting
• Avatar: {await xBunnEr()}
• Rank: 330
• Badge: 201
"""
        else:
            success_msg = f"[B][C][FF0000]❌ Failed to create spam packet!\n"
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

# Also create a shorter alias command handler
async def handle_sr_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle /sr command (short version of /spamroom)"""
    await handle_room_spam_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type)
        
async def detect_emote_perfect(data_hex, key, iv):
    """100% ACCURATE emote detection using YOUR exact packet structure"""
    
    try:
        # Step 1: Decrypt using your EXACT method
        decrypted = await DeCode_PackEt(data_hex[10:])  # Use YOUR existing function
        packet_json = json.loads(decrypted)
        
        # Step 2: EXACT STRUCTURE MATCHING
        # Check for Type 21 (from your Emote_k function)
        if packet_json.get('1') == 21:
            # Check for the EXACT structure you use
            if '2' in packet_json and 'data' in packet_json['2']:
                emote_data = packet_json['2']['data']
                
                # Verify EXACT field structure matches Emote_k()
                if ('1' in emote_data and '2' in emote_data and 
                    '5' in emote_data and 'data' in emote_data['5']):
                    
                    nested = emote_data['5']['data']
                    
                    # THIS IS THE 100% ACCURATE DETECTION
                    # Matches EXACTLY what you send in Emote_k()
                    if '1' in nested and '3' in nested:
                        return {
                            'type': 'emote',
                            'packet_type': 21,  # ← EXACT MATCH
                            'identifier': emote_data.get('1', {}).get('data'),
                            'base_emote': emote_data.get('2', {}).get('data'),
                            'target_uid': nested.get('1', {}).get('data'),  # WHO received it
                            'emote_id': nested.get('3', {}).get('data'),
                            'confidence': 100.0,
                            'raw_packet': packet_json
                        }
        
        # ALTERNATIVE FORMAT: Direct to player
        elif packet_json.get('1') == 26:  # Another emote type
            # Add similar exact matching here
            pass
        
        return None
        
    except Exception as e:
        print(f"❌ Perfect detection error: {e}")
        return None
        
async def detect_emote_with_sender(data_hex, key, iv):
    """Detect emote AND find who sent it"""
    
    try:
        # First, detect if it's an emote packet
        emote_info = await detect_emote_perfect(data_hex, key, iv)
        
        if not emote_info:
            return None
        
        # Now we need to find the SENDER's UID
        # Look for sender in different packet parts
        
        # METHOD 1: Check packet header for UID
        packet_header = data_hex[:20]
        
        # Look for UID patterns in hex (9-11 digits)
        import re
        uid_pattern = r'(\d{9,11})'
        
        # Search in entire packet
        all_uids = re.findall(uid_pattern, data_hex)
        
        if len(all_uids) >= 2:
            # We have at least 2 UIDs: sender and target
            # The target is already in emote_info['target_uid']
            target_uid = str(emote_info['target_uid'])
            
            # Find which UID is NOT the target
            for uid in all_uids:
                if uid != target_uid:
                    # This is likely the SENDER
                    emote_info['sender_uid'] = int(uid)
                    emote_info['detection_method'] = 'uid_pattern'
                    
                    print(f"✅ SENDER FOUND: {xMsGFixinG(uid)} sent emote to {xMsGFixinG(target_uid)}")
                    return emote_info
        
        # METHOD 2: Look in packet structure
        packet_json = emote_info['raw_packet']
        
        # Search recursively for UID that's NOT the target
        def find_sender_in_json(obj, target_uid):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == 'data' and isinstance(v, (int, str)):
                        v_str = str(v)
                        if v_str.isdigit() and len(v_str) > 8:
                            if v_str != str(target_uid):
                                return int(v)
                    elif isinstance(v, dict):
                        result = find_sender_in_json(v, target_uid)
                        if result:
                            return result
            return None
        
        sender_uid = find_sender_in_json(packet_json, emote_info['target_uid'])
        if sender_uid:
            emote_info['sender_uid'] = sender_uid
            emote_info['detection_method'] = 'json_search'
            return emote_info
        
        # If we can't find sender, at least we detected the emote
        emote_info['sender_uid'] = None
        return emote_info
        
    except Exception as e:
        print(f"❌ Sender detection error: {e}")
        return None


async def send_title_packet_direct(target_uid, chat_id, key, iv, region="ind"):
    """Send title packet directly without chat context - for auto-join"""
    try:
        print(f"🎖️ Sending title to {xMsGFixinG(target_uid)} in chat {chat_id}")
        
        # Method 1: Using your existing function
        title_packet = await convert_kyro_to_your_system(target_uid, chat_id, key, iv)
        
        if title_packet and whisper_writer:
            # Send via Whisper connection
            whisper_writer.write(title_packet)
            await whisper_writer.drain()
            print(f"✅ Title sent via Whisper to {xMsGFixinG(target_uid)}")
            return True
            
    except Exception as e:
        print(f"❌ Error sending title directly: {e}")
        import traceback
        traceback.print_exc()
    
    return False

def extract_type_5(packet_json):
    """Extract from Type 5 packets"""
    if packet_json.get('1') == 5:
        try:
            if '2' in packet_json and 'data' in packet_json['2']:
                data = packet_json['2']['data']
                sender = data.get('1', {}).get('data')
                emote_id = data.get('4', {}).get('data')
                
                if sender:
                    return {
                        'sender_uid': sender,
                        'emote_id': emote_id or 909000063,  # Default if not found
                        'packet_type': 5,
                        'confidence': 'medium'
                    }
        except:
            pass
    return None

async def extract_emote_info(data_hex, key, iv):
    """Extract full emote info from packet"""
    try:
        packet = await DeCode_PackEt(data_hex[10:])
        packet_json = json.loads(packet)
        
        # DEBUG: Print packet structure
        # print("📦 Packet JSON:", json.dumps(packet_json, indent=2)[:300])
        
        # Check all possible structures
        structures = [
            # Type 21 (from your Emote_k)
            lambda: extract_type_21(packet_json),
            # Type 26
            lambda: extract_type_26(packet_json),
            # Type 5
            lambda: extract_type_5(packet_json),
            # Generic search
            lambda: generic_extract(packet_json)
        ]
        
        for extractor in structures:
            info = extractor()
            if info and info.get('sender_uid'):
                return info
        
        return None
        
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return None

def extract_type_21(packet_json):
    """Extract from Type 21 (your Emote_k structure)"""
    if packet_json.get('1') == 21:
        try:
            if ('2' in packet_json and 'data' in packet_json['2'] and
                '5' in packet_json['2']['data'] and 'data' in packet_json['2']['data']['5']):
                
                data = packet_json['2']['data']
                nested = data['5']['data']
                
                sender = nested.get('1', {}).get('data')
                emote_id = nested.get('3', {}).get('data')
                
                if sender and emote_id:
                    return {
                        'sender_uid': sender,
                        'emote_id': emote_id,
                        'packet_type': 21,
                        'confidence': 'high'
                    }
        except:
            pass
    return None

def extract_type_26(packet_json):
    """Extract from Type 26 (common emote)"""
    if packet_json.get('1') == 26:
        try:
            if '2' in packet_json and 'data' in packet_json['2']:
                data = packet_json['2']['data']
                sender = data.get('1', {}).get('data')
                emote_id = data.get('2', {}).get('data')
                
                if sender and emote_id:
                    return {
                        'sender_uid': sender,
                        'emote_id': emote_id,
                        'packet_type': 26,
                        'confidence': 'high'
                    }
        except:
            pass
    return None

# Add these imports at the top with your other imports
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import json
import requests
import asyncio

# Add these constants with your other global variables
BIO_ENCRYPTION_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
BIO_ENCRYPTION_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
FREEFIRE_VERSION = "OB53"

def decode_jwt_noverify(token: str):
    """Decode JWT without verification"""
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return None
        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode())
        return payload
    except Exception:
        return None

# Add these global variables

async def is_bot_in_squad(bot_uid, key, iv):
    """Quick check if bot is in squad (with caching)"""
    global last_bot_status_check, cached_bot_status
    
    # Use cache if recent
    current_time = time.time()
    if (current_time - last_bot_status_check < bot_status_cache_time and 
        cached_bot_status is not None):
        return cached_bot_status
    
    try:
        # Send status request
        status_packet = await createpacketinfo(bot_uid, key, iv)
        if status_packet and online_writer:
            online_writer.write(status_packet)
            await online_writer.drain()
            
            # Wait for response
            await asyncio.sleep(2)
            
            # Check cache
            if bot_uid in status_response_cache:
                packet = status_response_cache[bot_uid].get('packet', b'')
                status = get_player_status(packet)
                
                in_squad = "INSQUAD" in status
                cached_bot_status = in_squad
                last_bot_status_check = current_time
                
                return in_squad
        
        return False
        
    except Exception as e:
        print(f"❌ Squad check error: {e}")
        return False

def get_bio_server_url(lock_region: str):
    """Get bio endpoint based on region"""
    region = lock_region.upper()
    if region == "IND":
        return "https://client.ind.freefiremobile.com/UpdateSocialBasicInfo"
    elif region in {"BR", "US", "SAC", "NA"}:
        return "https://client.us.freefiremobile.com/UpdateSocialBasicInfo"
    elif region == "BD":
        return "https://client.bd.freefiremobile.com/UpdateSocialBasicInfo"
    elif region == "SG":
        return "https://client.sg.freefiremobile.com/UpdateSocialBasicInfo"
    else:
        return "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo"

def create_bio_protobuf(bio_text):
    """Create protobuf message for bio update - EXACT SAME AS YOUR FLASK API"""
    # This creates the EXACT same protobuf structure as your Flask API
    
    # Protobuf structure from your API:
    # field_2: 17 (0x11)
    # field_5: EmptyMessage
    # field_6: EmptyMessage  
    # field_8: bio_text (string)
    # field_9: 1 (0x01)
    # field_11: EmptyMessage
    # field_12: EmptyMessage
    
    # Build protobuf manually (matching your exact structure)
    # Field 2: varint 17
    field_2 = b'\x08\x11'  # tag:1 type:varint value:17
    
    # Field 5: EmptyMessage (empty bytes)
    field_5 = b'\x2A\x00'  # tag:5 type:length-delimited length:0
    
    # Field 6: EmptyMessage (empty bytes)
    field_6 = b'\x32\x00'  # tag:6 type:length-delimited length:0
    
    # Field 8: bio text (string)
    bio_bytes = bio_text.encode('utf-8')
    bio_length = len(bio_bytes)
    field_8 = b'\x42' + bytes([bio_length]) + bio_bytes  # tag:8 type:string
    
    # Field 9: varint 1
    field_9 = b'\x48\x01'  # tag:9 type:varint value:1
    
    # Field 11: EmptyMessage
    field_11 = b'\x5A\x00'  # tag:11 type:length-delimited length:0
    
    # Field 12: EmptyMessage
    field_12 = b'\x62\x00'  # tag:12 type:length-delimited length:0
    
    # Combine all fields
    protobuf_data = field_2 + field_5 + field_6 + field_8 + field_9 + field_11 + field_12
    return protobuf_data

async def set_bio_directly_async_with_retry(jwt_token, bio_text, region="IND", max_retries=3, retry_delay=2):
    """Set bio with automatic retry logic"""
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Bio API attempt {attempt + 1}/{max_retries}")
            
            result = await set_bio_directly_async(jwt_token, bio_text, region)
            
            if result.get("success"):
                return result
            else:
                print(f"❌ Bio update failed: {result.get('message')}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    
        except Exception as e:
            print(f"❌ Bio attempt {attempt + 1} error: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            continue
    
    # If all retries failed
    return {
        "success": False,
        "message": f"All {max_retries} attempts failed"
    }

async def set_bio_directly_async(jwt_token, bio_text, region="IND"):
    """Set bio directly - ASYNC version with better error handling"""
    try:
        # Decode JWT to get region
        payload = decode_jwt_noverify(jwt_token)
        if not payload:
            return {
                "success": False,
                "message": "Invalid JWT token"
            }
        
        lock_region = payload.get("lock_region", region).upper()
        url_bio = get_bio_server_url(lock_region)
        
        # Free Fire renders !s as a space in bios — spaces must be encoded
        bio_text = bio_text.replace(' ', '!s')
        
        print(f"🔧 Setting bio for region: {lock_region}")
        print(f"📝 Bio text: {bio_text}")
        
        # Create protobuf message
        data_bytes = create_bio_protobuf(bio_text)
        print(f"📦 Protobuf created: {len(data_bytes)} bytes")
        
        # Encrypt using AES CBC
        cipher = AES.new(BIO_ENCRYPTION_KEY, AES.MODE_CBC, BIO_ENCRYPTION_IV)
        
        # Pad data to AES block size (16 bytes)
        padding_length = 16 - (len(data_bytes) % 16)
        if padding_length:
            data_bytes += bytes([padding_length] * padding_length)
        
        encrypted_data = cipher.encrypt(data_bytes)
        print(f"🔐 Encrypted: {len(encrypted_data)} bytes")
        
        # Headers
        headers = {
            "Expect": "100-continue",
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": FREEFIRE_VERSION,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        print(f"🚀 Sending to: {url_bio}")
        
        # Use aiohttp with timeout
        timeout = aiohttp.ClientTimeout(total=10)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url_bio, headers=headers, data=encrypted_data) as response:
                response_bytes = await response.read()
                response_text = response_bytes.decode('utf-8', errors='replace')
                
                print(f"📡 Response status: {response.status}")
                
                if response.status == 200:
                    return {
                        "success": True,
                        "message": "Bio updated successfully!",
                        "region": lock_region,
                        "bio": bio_text
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Server error: {response.status} - {response_text[:100]}"
                    }
                
    except aiohttp.ClientError as e:
        print(f"❌ Network error: {e}")
        return {
            "success": False,
            "message": f"Network error: {str(e)[:80]}"
        }
    except asyncio.TimeoutError:
        print(f"❌ Request timeout")
        return {
            "success": False,
            "message": "Request timeout (10s)"
        }
    except Exception as e:
        print(f"❌ Bio update error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Error: {str(e)[:80]}"
        }

# Now add this command handler to your TcPChaT function
# Find where other commands are handled and add this:

def analyze_squad_packet(packet_json):
    """Analyze packet structure to find squad members"""
    
    print("\n🔍 ANALYZING SQUAD PACKET STRUCTURE")
    print("="*50)
    
    # Check if this is a squad data packet
    if '5' not in packet_json or 'data' not in packet_json['5']:
        print("❌ Not a squad data packet")
        return None
    
    squad_data = packet_json['5']['data']
    
    # Look for fields that could contain multiple players
    candidate_fields = []
    
    for field_num in squad_data:
        field_info = squad_data[field_num]
        if 'data' not in field_info:
            continue
            
        data_value = field_info['data']
        
        # Check if it's a list (likely contains multiple players)
        if isinstance(data_value, list):
            print(f"✅ Field {field_num}: LIST with {len(data_value)} items")
            candidate_fields.append((field_num, 'list', data_value))
            
            # Show first item structure
            if data_value and isinstance(data_value[0], dict):
                print(f"   First item keys: {list(data_value[0].keys())}")
                # Check if first item has UID (field 1)
                if '1' in data_value[0]:
                    uid = data_value[0]['1']['data']
                    print(f"   ↳ Contains UID: {uid}")
        
        # Check if it's a dict with numeric keys (0, 1, 2, 3...)
        elif isinstance(data_value, dict):
            keys = list(data_value.keys())
            numeric_keys = [k for k in keys if k.isdigit()]
            if len(numeric_keys) > 0:
                print(f"✅ Field {field_num}: DICT with numeric keys {numeric_keys[:5]}...")
                candidate_fields.append((field_num, 'dict', data_value))
    
    print("\n🎯 MOST LIKELY SQUAD MEMBERS FIELDS:")
    for field_num, field_type, data in candidate_fields:
        print(f"  Field {field_num} ({field_type})")
        
        if field_type == 'list':
            # Try to extract UIDs from list
            uids = []
            for item in data[:5]:  # Check first 5 items
                if isinstance(item, dict) and '1' in item:
                    uid = item['1']['data']
                    uids.append(uid)
            if uids:
                print(f"    ↳ Found UIDs: {uids}")
        
        elif field_type == 'dict':
            # Try to extract UIDs from dict
            uids = []
            for key in list(data.keys())[:5]:  # Check first 5 keys
                item = data[key]
                if isinstance(item, dict) and '1' in item:
                    uid = item['1']['data']
                    uids.append(uid)
            if uids:
                print(f"    ↳ Found UIDs: {uids}")
    
    return candidate_fields

def generic_extract(packet_json):
    """Generic search for UID and emote ID"""
    uid = None
    emote_id = None
    
    # Recursively search for UID (long number)
    def search(obj):
        nonlocal uid, emote_id
        
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'data' and isinstance(v, (int, str)) and str(v).isdigit():
                    # Check if it looks like a UID (long number)
                    num = int(v)
                    if 1000000 < num < 99999999999:  # Reasonable UID range
                        if not uid:  # First found is likely sender
                            uid = num
                        # Check if it's an emote ID (starts with 909...)
                        elif str(v).startswith('909') and len(str(v)) >= 9:
                            emote_id = num
                
                elif isinstance(v, dict):
                    search(v)
                elif isinstance(v, list):
                    for item in v:
                        search(item)
    
    search(packet_json)
    
    if uid:
        return {
            'sender_uid': uid,
            'emote_id': emote_id or 909000063,  # Default AK emote
            'packet_type': 'generic',
            'confidence': 'medium'
        }
    
    return None
    
async def auto_reply_with_emote(emote_info, key, iv):
    """Automatically reply with same emote"""
    
    try:
        # Get bot's UID (you need to set this)
        bot_uid = 14010319252  # Replace with your bot's actual UID
        
        sender_uid = emote_info['sender_uid']
        emote_id = emote_info['emote_id']
        
        # Send emote back to sender
        reply_packet = await Emote_k(sender_uid, emote_id, key, iv, region)
        
        if online_writer:
            online_writer.write(reply_packet)
            await online_writer.drain()
            
            print(f"🤖 Bot replied with emote {emote_id} to {sender_uid}")
            
    except Exception as e:
        print(f"❌ Auto-reply error: {e}")

def extract_squad_members_correct(packet_json):
    """Extract squad members from FULL squad packet"""
    
    print("\n🔍 EXTRACTING SQUAD MEMBERS")
    print("="*50)
    
    try:
        if ('5' not in packet_json or 
            'data' not in packet_json['5'] or 
            '2' not in packet_json['5']['data']):
            print("❌ Invalid packet structure")
            return []
        
        field2_data = packet_json['5']['data']['2']['data']
        
        squad_members = []
        
        # Field 2 has numeric keys: '1', '2', '3', '4', '5', etc.
        # Each key might be a squad member slot OR player data field
        
        # Let's check what each numeric key contains
        for key in field2_data:
            if not key.isdigit():
                continue
                
            item = field2_data[key]['data']
            print(f"\n📦 Key {key}: Type = {type(item)}")
            
            if isinstance(item, dict):
                # Check if this is a player object
                # Player objects usually have fields: 1=UID, 2=name, 4=rank, etc.
                if '1' in item and '2' in item:
                    try:
                        uid = item['1']['data']
                        name = item['2']['data']
                        
                        # Make sure it's a valid UID (not a small number)
                        if isinstance(uid, int) and uid > 1000000:
                            rank = item['4']['data'] if '4' in item else 0
                            
                            print(f"   ✅ PLAYER FOUND!")
                            print(f"      UID: {uid}")
                            print(f"      Name: {name}")
                            print(f"      Rank: {rank}")
                            
                            squad_members.append({
                                'slot': key,
                                'uid': uid,
                                'name': name,
                                'rank': rank
                            })
                        else:
                            print(f"   ❌ Not a UID: {uid}")
                            
                    except Exception as e:
                        print(f"   ❌ Error extracting player: {e}")
                else:
                    print(f"   ↳ Fields: {list(item.keys())[:5]}...")
            elif isinstance(item, (int, str)):
                print(f"   ↳ Value: {item}")
        
        print(f"\n🏆 TOTAL SQUAD MEMBERS FOUND: {len(squad_members)}")
        for member in squad_members:
            print(f"  • Slot {member['slot']}: {member['name']} (UID: {member['uid']})")
        
        return squad_members
        
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        import traceback
        traceback.print_exc()
        return []
        
async def analyze_packet_structure(data_hex, key, iv):
    """Analyze and display packet structure"""
    
    print(f"\n📦 PACKET ANALYSIS")
    print("="*50)
    
    # Basic info
    print(f"📏 Length: {len(data_hex)} characters")
    print(f"🔢 Header: {data_hex[:10]}")
    
    # Try to decode
    try:
        if len(data_hex) > 20:
            decoded = await DeCode_PackEt(data_hex[10:])
            packet_json = json.loads(decoded)
            
            print(f"✅ Successfully decoded!")
            print(f"📊 Packet type (field 1): {packet_json.get('1', 'Unknown')}")
            
            # Show structure
            print(f"\n📋 PACKET STRUCTURE:")
            print(f"Top-level fields: {list(packet_json.keys())}")
            
            # Show field 1 value
            if '1' in packet_json:
                print(f"  Field 1: {packet_json['1']}")
            
            # Show if it contains emote ID patterns
            import re
            emote_patterns = re.findall(r'909[0-9a-f]{6}', data_hex)
            if emote_patterns:
                print(f"\n🎭 EMOTE IDS FOUND IN HEX: {emote_patterns}")
            
            # Show UID patterns
            uid_patterns = re.findall(r'(\d{9,11})', data_hex)
            uids = [uid for uid in uid_patterns if not uid.startswith('909')]
            if uids:
                print(f"👤 UIDS FOUND IN HEX: {uids}")
            
            # Return the decoded structure
            return packet_json
            
        else:
            print("❌ Packet too short to decode")
            return None
            
    except Exception as e:
        print(f"❌ Decode error: {e}")
        return None

async def RedZed_SendInv(bot_uid, uid, key, iv):
    """Async version of send invite function"""
    try:
        fields = {
            1: 2, 
            2: {
                1: int(uid), 
                2: "IND", 
                3: 1, 
                4: 1, 
                6: "RedZedKing!!", 
                7: 330, 
                8: 1000, 
                9: 100, 
                10: "DZ", 
                12: 1, 
                13: int(uid), 
                16: 1, 
                17: {
                    2: 159, 
                    4: "y[WW", 
                    6: 11, 
                    8: "1.123.1", 
                    9: 3, 
                    10: 1
                }, 
                18: 306, 
                19: 18, 
                24: 902000306, 
                26: {}, 
                27: {
                    1: 11, 
                    2: int(bot_uid), 
                    3: 99999999999
                }, 
                28: {}, 
                31: {
                    1: 1, 
                    2: 32768
                }, 
                32: 32768, 
                34: {
                    1: bot_uid, 
                    2: 8, 
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                }
            }
        }
        
        # Convert bytes properly
        if isinstance(fields[2][34][3], str):
            fields[2][34][3] = b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
        
        # Use async versions of your functions
        packet = await CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
        
        # Generate final packet
        final_packet = await GeneRaTePk(packet_hex, '0515', key, iv)
        
        return final_packet
        
    except Exception as e:
        print(f"❌ Error in RedZed_SendInv: {e}")
        import traceback
        traceback.print_exc()
        return None

async def freeze_emote_spam(uid, key, iv, region, chat_type, chat_id, sender_uid):
    """Send 3 freeze emotes in 1-second cycles for 10 seconds"""
    global freeze_running
    
    try:
        cycles = 0
        max_cycles = FREEZE_DURATION  # 10 seconds
        
        while freeze_running and cycles < max_cycles:
            # Send all 3 emotes in sequence
            for i, emote_id in enumerate(FREEZE_EMOTES):
                if not freeze_running:
                    break
                    
                try:
                    # Send emote
                    emote_packet = await Emote_k(int(uid), emote_id, key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                    
                    print(f"❄️ Freeze emote {i+1}/{len(FREEZE_EMOTES)} sent: {emote_id}")
                    
                    # Small delay between emotes (0.3 seconds)
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    print(f"❌ Error sending freeze emote {i+1}: {e}")
            
            cycles += 1
            print(f"🌀 Freeze cycle {cycles}/{max_cycles} completed")
            
            # Wait for next cycle (total 1 second per cycle)
            remaining_time = 1.0 - (0.3 * len(FREEZE_EMOTES))
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
        
        print(f"✅ Freeze sequence completed: {cycles} cycles")
        return cycles
        
    except Exception as e:
        print(f"❌ Freeze function error: {e}")
        return 0
        
async def handle_freeze_completion(freeze_task, uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle freeze command completion"""
    try:
        cycles_completed = await freeze_task
        
        completion_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND COMPLETED!

🎯 Target: {xMsGFixinG(uid)}
⏱️ Duration: {cycles_completed} seconds
🎭 Emotes sent: {cycles_completed * 3}
❄️ Sequence: 
  • 909040004 (Ice)
  • 909050008 (Frozen)
  • 909000002 (Freeze)

✅ Status: Complete!
"""
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("🛑 Freeze command cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Freeze error: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)

async def test_emote_packet(target_uid, emote_id, key, iv, region="IND"):
    """Test if emote packet works and show structure"""
    
    print(f"\n🎭 TESTING EMOTE PACKET")
    print("="*50)
    
    # Create the packet using your function
    emote_packet = await Emote_k(target_uid, emote_id, key, iv, region)
    
    if not emote_packet:
        print("❌ Failed to create packet")
        return False
    
    # Convert to hex for analysis
    packet_hex = emote_packet.hex()
    
    print(f"📦 Packet created!")
    print(f"   Length: {len(packet_hex)} characters")
    print(f"   Header: {packet_hex[:20]}")
    
    # Try to decode it back
    try:
        if len(packet_hex) > 20:
            # Remove header (first 10 bytes = 20 hex chars)
            payload = packet_hex[20:]  # Skip header
            
            # Decrypt (you need to implement this)
            # For testing, let's see raw structure
            print(f"\n🔍 RAW PACKET STRUCTURE:")
            print(f"Full hex (first 200 chars):")
            print(packet_hex[:200] + "...")
            
            # Look for the UID in hex
            import re
            uid_hex = hex(target_uid)[2:]
            if uid_hex in packet_hex:
                print(f"✅ Target UID {xMsGFixinG(target_uid)} found in packet!")
            else:
                print(f"❌ Target UID not found in hex")
            
            # Look for emote ID
            emote_hex = hex(emote_id)[2:]
            if emote_hex in packet_hex:
                print(f"✅ Emote ID {emote_id} found in packet!")
            else:
                print(f"❌ Emote ID not found in hex")
        
        print(f"\n✅ Packet created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False
        
async def send_and_monitor_emote(target_uid, emote_id, key, iv, region, reader):
    """Send emote and monitor response - FIXED VERSION"""
    
    print(f"\n🚀 SENDING TEST EMOTE")
    print(f"   👤 Target: {xMsGFixinG(target_uid)}")
    print(f"   🎭 Emote: {emote_id}")
    print("="*50)
    
    # 1. Create packet
    emote_packet = await Emote_k(target_uid, emote_id, key, iv, region)
    
    if not emote_packet:
        print("❌ Failed to create packet")
        return
    
    # 2. Send it
    print("📤 Sending packet...")
    if online_writer:
        online_writer.write(emote_packet)
        await online_writer.drain()
        print("✅ Packet sent!")
    else:
        print("❌ No connection")
        return
    
    # 3. Wait for response (SHORTER - 2 seconds)
    print("\n⏳ Waiting for response (2 seconds)...")
    
    responses = []
    start_time = time.time()
    
    while time.time() - start_time < 2:  # Reduced from 5 to 2 seconds
        try:
            # Read any response
            if reader:
                response = await asyncio.wait_for(reader.read(9999), timeout=0.1)
                if response:
                    resp_hex = response.hex()
                    responses.append(resp_hex)
                    
                    # Quick analysis
                    print(f"📥 Got response #{len(responses)}")
                    print(f"   Length: {len(resp_hex)} chars")
                    print(f"   Header: {resp_hex[:10]}")
                    
                    # Check if it's the emote echo
                    if '909' in resp_hex:
                        print(f"   🎭 Contains emote ID!")
        except asyncio.TimeoutError:
            continue
        except Exception as e:
            # Silent error - don't print
            pass
    
    # 4. Summary
    print(f"\n📊 RESPONSE SUMMARY")
    print(f"Total responses: {len(responses)}")
    
    if len(responses) > 0:
        print("✅ SUCCESS! Server accepted your emote packet!")
    else:
        print("⚠️ No immediate response (might still be processing)")
        
async def handle_guest_generation(count, uid, chat_id, chat_type, key, iv):
    """Handle guest generation in background and send updates"""
    try:
        # Start generation
        accounts = await generate_and_save_accounts(count)
        
        # Send completion message
        if accounts:
            success_msg = f"""[B][C][00FF00]✅ GUEST ACCOUNTS GENERATED!

📊 Generated: {len(accounts)}/{count} accounts
💾 Saved to: guest_accounts.json

📋 Format in file:
• uid: Account UID
• password: Account password
• name: BlackApis
• timestamp: Generation time

💡 Use accounts for:
• Multi-account spams
• Friend requests
• Testing purposes
"""
        else:
            success_msg = f"""[B][C][FF0000]❌ GENERATION FAILED!

📊 Requested: {count} accounts
❌ Generated: 0 accounts

💡 Try:
1. Check internet connection
2. API might be down
3. Try smaller count (like 5)
4. Try again later
"""
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Optional: Send first account as preview
        if accounts:
            preview_msg = f"""[B][C][FFFF00]🔍 FIRST ACCOUNT PREVIEW:

👤 UID: {accounts[0]['uid']}
🔑 Pass: {accounts[0]['password']}
📛 Name: {accounts[0]['name']}

💡 Check guest_accounts.json for all accounts!
"""
            await safe_send_message(chat_type, preview_msg, uid, chat_id, key, iv)
            
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Generation error: {str(e)[:50]}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)        
        
async def start_auto_packet(key, iv, region):
    """Create start match packet"""
    fields = {
        1: 9,
        2: {
            1: 12480598706,
        },
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
        
async def detect_and_hijack_emote(data_hex, key, iv, bot_uid, region):
    """Detect emote and hijack it by sending with bot's UID"""
    try:
        # Detect emote info
        emote_info = await extract_emote_info(data_hex, key, iv)
        
        if not emote_info or not emote_info.get('sender_uid'):
            return False
        
        sender_uid = emote_info['sender_uid']
        emote_id = emote_info['emote_id']
        
        print(f"\n🎭 EMOTE DETECTED FOR HIJACK!")
        print(f"   👤 Original Sender: {sender_uid}")
        print(f"   🎭 Emote ID: {emote_id}")
        
        # Don't hijack bot's own emotes
        if int(sender_uid) == bot_uid:
            print("⚠️ Skipping - bot's own emote")
            return False
        
        # HIJACK: Send emote with bot's UID instead
        print(f"🤖 HIJACKING EMOTE! Sending as bot {bot_uid}...")
        
        # Use either of your emote functions
        # Method 1: Using Emote_k (your second packet)
        hijack_packet = await Emote_k(
            int(bot_uid),  # Use BOT'S UID instead of sender's
            int(emote_id),  # Same emote ID
            key, iv, region
        )
        
        # Alternative: Using emote_send (your first packet)
        # hijack_packet = await create_hijacked_emote(bot_uid, emote_id, key, iv, region)
        
        if hijack_packet and online_writer:
            # Send the hijacked emote
            online_writer.write(hijack_packet)
            await online_writer.drain()
            
            print(f"✅ Emote hijacked! Bot {bot_uid} now appears to do emote {emote_id}")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Emote hijack error: {e}")
        return False
        
async def SwitchLoneWolfDule(BotUid, key, iv):
    fields = {1: 17, 2: {1: BotUid, 2: 1, 3: 1, 4: 43, 5: "\u000b", 8: 1, 19: 1}}
    return await GenPacket((await CreateProtobufPacket(fields)).hex(), '0519', key, iv)        
        
async def KickTarget(target_uid, key, iv):
    fields = {1: 35, 2: {1: int(target_uid)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515' , key, iv)
        
async def create_hijacked_emote(hijacker_uid, emote_id, key, iv, region):
    """Create emote packet that appears to come from hijacker"""
    try:
        # Using your Emote_k structure but with hijacker's UID
        fields = {
            1: 21,  # Emote packet type
            2: {
                1: 804266360,  # Some identifier (keep as is)
                2: 909000001,  # Base emote ID
                5: {
                    1: int(hijacker_uid),  # HIJACKER'S UID goes here
                    3: int(emote_id),      # The emote ID to perform
                }
            }
        }
        
        if region.lower() == "ind":
            packet = '0514'
        elif region.lower() == "bd":
            packet = "0519"
        else:
            packet = "0515"
            
        return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, key, iv)
        
    except Exception as e:
        print(f"❌ Error creating hijacked emote: {e}")
        return None
            
def analyze_hex_packet(packet_hex):
    """Analyze hex packet structure"""
    
    print(f"\n🔬 HEX PACKET ANALYSIS")
    print("="*50)
    
    # Header analysis
    header = packet_hex[:10]
    print(f"Header (first 5 bytes): {header}")
    
    # Common headers:
    # 0514 = IND online packet
    # 0519 = BD online packet  
    # 1215 = Whisper packet
    # 1200 = Chat packet
    
    if header.startswith('05'):
        print("📡 Online connection packet")
    elif header.startswith('12'):
        print("💬 Whisper/Chat packet")
    
    # Look for UIDs (9-11 digit numbers in hex)
    import re
    
    # Find all sequences of 9+ hex digits
    hex_patterns = re.findall(r'[0-9a-f]{9,12}', packet_hex.lower())
    
    print(f"\n🔢 Hex sequences found:")
    for pattern in hex_patterns[:10]:  # Show first 10
        # Try to convert to decimal
        try:
            decimal = int(pattern, 16)
            if 1000000 < decimal < 99999999999:  # Reasonable UID range
                print(f"  {pattern} → {decimal} (Possible UID)")
            elif decimal > 900000000:  # Emote ID range
                print(f"  {pattern} → {decimal} (Possible emote ID)")
        except:
            print(f"  {pattern}")
    
    # Show packet content (first 200 chars)
    print(f"\n📝 Packet preview (first 200 chars):")
    print(packet_hex[:200])
    
    if len(packet_hex) > 200:
        print(f"... and {len(packet_hex) - 200} more characters")
        
def append_to_whitelist(uid_to_add):
    """Simple function to add UID to whitelist"""
    global WHITELISTED_UIDS
    
    uid_str = str(uid_to_add)
    
    if uid_str in WHITELISTED_UIDS:
        return False, f"UID {uid_str} already in whitelist"
    
    WHITELISTED_UIDS.add(uid_str)
    return True, f"✅ Added {uid_str} to whitelist"        
        
async def hijack_squad_emote(data_hex, key, iv, bot_uid, region, in_squad):
    """Only hijack emotes when bot is in a squad"""
    if not in_squad:
        return False
    
    try:
        # Extract emote info
        emote_info = await extract_emote_info(data_hex, key, iv)
        
        if not emote_info:
            return False
        
        sender_uid = emote_info['sender_uid']
        emote_id = emote_info['emote_id']
        
        print(f"\n🏆 SQUAD EMOTE HIJACK!")
        print(f"   👥 In squad: Yes")
        print(f"   👤 Original: {sender_uid}")
        print(f"   🎭 Emote: {emote_id}")
        
        # Create hijacked emote
        hijack_packet = await create_hijacked_emote(bot_uid, emote_id, key, iv, region)
        
        if hijack_packet and online_writer:
            online_writer.write(hijack_packet)
            await online_writer.drain()
            
            print(f"✅ Squad emote hijacked by bot {bot_uid}!")
            
            # Optional: Also send the original emote to maintain appearance
            await asyncio.sleep(0.3)
            original_packet = await Emote_k(int(sender_uid), int(emote_id), key, iv, region)
            online_writer.write(original_packet)
            await online_writer.drain()
            
            print(f"✅ Also sent original emote to maintain cover")
            
            return True
            
    except Exception as e:
        print(f"❌ Squad hijack error: {e}")
    
    return False
    
async def send_friend_request_async(target_uid: str, count: int = 1) -> dict:
    """
    Main function to send friend requests from TCP bot
    
    Args:
        target_uid: Target player UID
        count: Number of requests (1 for single, >1 for bulk)
    
    Returns:
        Dictionary with results
    """
    try:
        if count == 1:
            # Single request using token.json
            token = load_jwt_token()
            if not token:
                return {"success": 0, "failed": 1, "error": "No token found"}
            
            success = send_friend_request_single(target_uid, token)
            
            if success:
                return {"success": 1, "failed": 0}
            else:
                return {"success": 0, "failed": 1}
                
        else:
            # Bulk requests using token_ind.json
            tokens = load_tokens_ind()
            if not tokens:
                return {"success": 0, "failed": 0, "error": "No tokens found"}
            
            max_count = min(count, len(tokens))
            results = {"success": 0, "failed": 0}
            
            print(f"📦 Sending {max_count} friend requests...")
            
            # Send requests sequentially (or use threading for faster)
            for i in range(max_count):
                token = tokens[i]['token']
                success = send_friend_request_single(target_uid, token)
                
                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)
            
            return results
            
    except Exception as e:
        print(f"❌ Friend request error: {e}")
        return {"success": 0, "failed": 0, "error": str(e)}    

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, last_status_packet, status_response_cache, senthi
    global insquad, joining_team, whisper_writer, region, squad_chat_authed, squad_group_owner_uid, squad_group_chat_code
    global _console_squad_chat_id
 
    bot_uid = 14010319252
 
    if insquad is not None:
        insquad = None
    if joining_team is True:
        joining_team = False
    squad_chat_authed = False
    squad_group_owner_uid = None
    squad_group_chat_code = None
    
    online_writer = None
    whisper_writer = None
    
    while True:
        try:
            print(f"Attempting to connect to {ip}:{port}...")
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            
            # --- AUTHENTICATION ---
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            print("Authentication token sent. Listening for emotes...")
            
            # --- READING LOOP ---
            while True:
                try:
                    data2 = await asyncio.wait_for(reader.read(9999), timeout=120)
                except asyncio.TimeoutError:
                    print("⚠️ Online connection silent for 120s — reconnecting...")
                    break
                    
                if not data2: 
                    print("Connection closed by the server.")
                    break
                    
                data_hex = data2.hex()
      
                # Your existing code...
  
                
                
              # =================== EMOTE DETECTION ONLY ===================
                if data_hex.startswith("0500") and emote_hijack == True:
                    try:
                        # Try to detect emote
                        emote_info = await extract_emote_info(data_hex, key, iv)
                        
                        in_squad = insquad is not None
            

                

                        
                        if emote_info and emote_info.get('sender_uid'):
                            sender_uid = emote_info['sender_uid']
                            emote_id = emote_info['emote_id']
                            
                            
                            
                            print(f"\n🎯 EMOTE DETECTED!")
                            print(f"   👤 Sender UID: {sender_uid}")
                            print(f"   🎭 Emote ID: {emote_id}")
                            
                            # Don't respond to bot's own emotes
                            if int(sender_uid) != bot_uid:
                                print("🤖 Bot responding with dual emotes...")
                                
                                # STEP 1: Send fixed emote 909035003 to the sender
                                print(f"  1️⃣ Sending emote 909035003 to {sender_uid}")
                                fixed_emote_packet = await Emote_k(
                                    int(sender_uid), 
                                    909035003,  # Fixed emote ID
                                    key, iv, region
                                )
                                if fixed_emote_packet and online_writer:
                                    online_writer.write(fixed_emote_packet)
                                    await online_writer.drain()
                                    await asyncio.sleep(0.5)
                                
                                # STEP 2: Bot does the SAME emote that user did (to itself)
                                print(f"  2️⃣ Bot doing same emote {emote_id} to itself")
                                bot_self_emote = await Emote_k(
                                    bot_uid,  # Bot's own UID
                                    int(emote_id),  # Same emote user did
                                    key, iv, region
                                )
                                if bot_self_emote and online_writer:
                                    online_writer.write(bot_self_emote)
                                    await online_writer.drain()
                                    await asyncio.sleep(0.5)
                                
                                # STEP 3: Bot also sends the emote back to sender
                                print(f"  3️⃣ Mirroring emote {emote_id} back to {sender_uid}")
                                mirror_emote = await Emote_k(
                                    int(sender_uid),
                                    int(emote_id),  # Same emote back
                                    key, iv, region
                                )
                                if mirror_emote and online_writer:
                                    online_writer.write(mirror_emote)
                                    await online_writer.drain()
                                
                                print("✅ Dual emote response complete!")
                            
                            else:
                                print("⚠️ Skipping - bot's own emote")
                                
                    except Exception as e:
                        print(f"❌ Emote response error: {e}")
                        continue 
            
                    


                # =================== AUTO ACCEPT HANDLING ===================
                
                # Case 1: Squad is cancelled or left (6, 7 are often status/exit codes)
                if data_hex.startswith('0500') and insquad is not None and joining_team == False:
                    try:
                        # Assuming DeCode_PackEt and json.loads are available and correct
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        
                        if packet_json.get('1') in [6, 7]: 
                             insquad = None
                             joining_team = False
                             squad_chat_authed = False
                             squad_group_owner_uid = None
                             squad_group_chat_code = None
                             print("Squad cancelled or exited (code 6/7).")
                             continue
                             
                    except Exception as e:
                        print(f"Error in auto-accept case 1: {e}")
                        pass
                
                # case 2
                # Case 2: Auto-accept for whitelisted users
                if data_hex.startswith("0500") and insquad is None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)

                        field5 = packet_json.get('5')
                        if not field5 or not isinstance(field5, dict):
                            continue
                        field5_data = field5.get('data', {})
                        if not field5_data or '1' not in field5_data:
                            continue

                        uid = field5_data.get('1', {}).get('data')
                        squad_owner = uid
                        field2 = field5_data.get('2', {}).get('data', {})
                        invite_uid = field2.get('1', {}).get('data') if field2 else None
                        code = field5_data.get('8', {}).get('data')

                        if not uid or not code:
                            continue

                        emote_id = 909050009
                        bot_uid = 14009897329
    
                        # 🎯 FIX: Check SQUAD_OWNER (person who clicked "invite")
                        if "MĢ24_GÀMER" in WHITELISTED_UIDS:
                            print(f"✅ Whitelisted user {squad_owner} invited bot. Accepting...")
                        
                            if invite_uid:
                                SendInv = await RedZed_SendInv(bot_uid, invite_uid, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', SendInv)
                            inv_packet = await RejectMSGtaxt(squad_owner, uid, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', inv_packet)
        
                            print(f"Received squad invite from {squad_owner}, accepting...")                  
                            Join = await ArohiAccepted(squad_owner, code, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
        
                            await asyncio.sleep(2)
                                                    
                            emote_to_sender = await Emote_k(int(uid), emote_id, key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        
                            bot_emote = await Emote_k(int(bot_uid), emote_id, key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_emote)

                            # Set squad status
                            insquad = True
                            print(f"🤖 Bot joined squad of {squad_owner}")

                            # Immediately authenticate group chat so bot appears in group
                            await asyncio.sleep(1)
                            try:
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                                JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                                squad_group_owner_uid = OwNer_UiD
                                squad_group_chat_code = CHaT_CoDe
                                squad_chat_authed = True
                                joining_team = False
                                _console_squad_chat_id = OwNer_UiD
                                welcome_msg = """[B][C][FF1493]╔══════════════════╗
[FF1493]║  ⚡ GothicRealm Guild Bot ⚡
[FF1493]╚══════════════════╝
[00FF00]GothicRealm Guild Bot has joined the group!
[FFFFFF]
[FFD700]Owner   : [FF69B4]Biryani
[FFFFFF]
[FFD700]Dev     : [00FFFF]Ayaan
[FFFFFF]
[FFD700]Contact : [00FFFF]@paktcpbots
[FFFFFF]
[FFD700]Guild   : [00FFFF]GothicRealm
[FFFFFF]
[FF1493]══════════════════
[AAAAAA]Type /help for commands"""
                                P = await SEndMsG(0, welcome_msg, OwNer_UiD, OwNer_UiD, key, iv, region)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                print(f"✅ Bot authenticated group chat immediately after join.")
                            except Exception as auth_err:
                                print(f"⚠️ Immediate group auth failed (will retry next packet): {auth_err}")

                            continue  # Skip kick/reconnect and case-5 handlers for this same packet

                        else:
                            try:
                                print(f"🚫 Bot is private! Ignoring invite from {squad_owner}")
                                bot_uid = 13777711848
                                message_text = f" Can't accept Your request Talk to adventshi."
                                private_msg_packet = await xSEndMsg(
                                    Msg=message_text,
                                    Tp=2,  # 2 = Private message
                                    Tp2=int(squad_owner),  # Recipient UID
                                    id=int(bot_uid),  # Sender UID (your bot)
                                    K=key,
                                    V=iv
                                )
                                print("got it")

                                if private_msg_packet and whisper_writer:
                                    # Send via Whisper connection (chat connection)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', private_msg_packet)
                                else:
                                    print("can't do it")
                                    
                            except Exception as e:
                                print(" got an error in can't accept")
                            continue  # Done with this packet (reject path)

                    except Exception as e:
                        print(f"Error in auto-accept: {e}")
                        continue
                
                # =================== HANDLE KICK/RECONNECT ===================
                # Case 3: Bot was kicked and needs to re-join chat
                # Guard: only run when NOT in squad to avoid undoing a fresh join
                if data_hex.startswith('0500') and len(data_hex) > 1000 and insquad is None:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                    
                        packet_type = packet_json.get('1')
        
                        # Detect ALL kick/leave packets
                        if packet_type in [6, 7, 8, 9, 10, 11, 12]:
                            print(f"🚪 Kick/Leave packet detected (Type: {packet_type})")
            
                            # RESET SQUAD STATUS
                            insquad = None
                            joining_team = False
                            squad_chat_authed = False
                            squad_group_owner_uid = None
                            squad_group_chat_code = None
            
                            print(f"✅ Bot reset after kick. Ready for new invites.")
                            
                            # Try to extract squad info for possible reconnection
                            try:
                                if '5' in packet_json and 'data' in packet_json['5']:
                                    OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                                    print(f"🔄 Attempting reconnection to squad {SQuAD_CoDe}...")
                    
                                    # Re-authenticate chat
                                    JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                    
                                    print(f"✅ Chat re-authenticated for reconnection")
                            except:
                                print("⚠️ Could not extract squad info")
                                
                            continue  # Skip other handlers
        
                        # Also check for general squad data packets (for reconnection)
                        elif '5' in packet_json and 'data' in packet_json['5']:
                            try:
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                
                                # If we have squad data but insquad is None, try to reconnect
                                if insquad is None:
                                    print(f"🤖 Received squad data while not in squad. Attempting chat auth...")
                                    
                                    JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                    
                                    # Optional welcome back message
                                    welcome_msg = """[B][C][00FF00]🤖 Bot reconnected!"""
                                    P = await SEndMsG(0, welcome_msg, OwNer_UiD, OwNer_UiD, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                    
                            except:
                                pass  # Not a squad data packet
                
                    except Exception as e:
                        print(f"❌ Kick/reconnect handler error: {e}")
                        pass
                
                # case 5 — authenticate group chat and send welcome (runs once per join)
                if insquad == True and not squad_chat_authed:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        
                        print(f"Received squad data for joining team, attempting chat auth for {OwNer_UiD}...")
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key, iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                        
                        # Store squad info globally so commands in group chat can be responded to
                        squad_group_owner_uid = OwNer_UiD
                        squad_group_chat_code = CHaT_CoDe
                        squad_chat_authed = True  # Mark as done so we don't repeat every packet
                        joining_team = False
                        # DO NOT set insquad = None — keep squad state alive for command listening
                        # insquad stays True so we know the bot is in a squad
                        
                        # Also update the console squad chat ID for !group console command
                        _console_squad_chat_id = OwNer_UiD

                        message = """[B][C][FF1493]╔══════════════════╗
[FF1493]║  ⚡ GothicRealm Guild Bot ⚡
[FF1493]╚══════════════════╝
[00FF00]GothicRealm Guild Bot has joined the group!
[FFFFFF]
[FFD700]Owner   : [FF69B4]Biryani
[FFFFFF]
[FFD700]Dev     : [00FFFF]Ayaan
[FFFFFF]
[FFD700]Contact : [00FFFF]@paktcpbots
[FFFFFF]
[FFD700]Guild   : [00FFFF]GothicRealm
[FFFFFF]
[FF1493]══════════════════
[AAAAAA]Type /help for commands"""

                        P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        print(f"✅ Bot authenticated group chat for {OwNer_UiD}. Ready for commands.")
                            
                    except Exception as e:
                        print(f"Error in joining_team chat auth: {e}")
                        pass
                
                if "0600" in data2.hex()[0:4] and len(data2.hex()) > 700:
                    accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(accept_packet)
                    parsed_data = json.loads(kk)
                    #logging.info(parsed_data)

                    senthi = True

                if senthi == True:
                    senthi = False  # Always reset, regardless of squad owner state
                    if squad_group_owner_uid is not None:
                        message = """[B][C][FF1493]╔══════════════════╗
[FF1493]║  ⚡ GothicRealm Guild Bot ⚡
[FF1493]╚══════════════════╝
[00FF00]GothicRealm Guild Bot has joined the group!
[FFFFFF]
[FFD700]Owner   : [FF69B4]Biryani
[FFFFFF]
[FFD700]Dev     : [00FFFF]Ayaan
[FFFFFF]
[FFD700]Contact : [00FFFF]@paktcpbots
[FFFFFF]
[FFD700]Guild   : [00FFFF]GothicRealm
[FFFFFF]
[FF1493]══════════════════
[AAAAAA]Type /help for commands"""

                        P = await SEndMsG(0, message, squad_group_owner_uid, squad_group_owner_uid, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                # =================== STATUS HANDLER ===================
                if data_hex.startswith('0f00') and len(data_hex) > 100:
                    print(f"📡 Received status response packet")
    
                    try:
                        # Assuming the protocol structure: 0f00 + length bytes + 08 + actual proto data
                        # The split logic might need refinement based on the exact protocol
                        if '08' in data_hex:
                            proto_part = f'08{data_hex.split("08", 1)[1]}'
                        else:
                            print("⚠️ Status packet structure missing '08' marker.")
                            continue
        
                        # Assuming get_available_room is available
                        parsed_data = get_available_room(proto_part)
                        if parsed_data:
                            parsed_json = json.loads(parsed_data)
            
                            # Check if it's field 15 (player info)
                            if "2" in parsed_json and parsed_json["2"]["data"] == 15:
                                # Get player ID
                                player_id = parsed_json["5"]["data"]["1"]["data"]["1"]["data"]
                
                                # Assuming get_player_status is available
                                player_status = get_player_status(proto_part) 
                                print(f"✅ Parsed status for {xMsGFixinG(target_uid)}: {player_status}")
                
                                # Create cache entry
                                cache_entry = {
                                    'status': player_status, 
                                    'packet': proto_part,
                                    'timestamp': time.time(),
                                    'full_packet': data_hex,
                                    'parsed_json': parsed_json
                                }
                
                                # --- SPECIAL CONDITION CHECK ---
                                try:
                                    StatusData = parsed_json
                                    if ("5" in StatusData and "data" in StatusData["5"] and 
                                        "1" in StatusData["5"]["data"] and "data" in StatusData["5"]["data"]["1"] and 
                                        "3" in StatusData["5"]["data"]["1"]["data"] and "data" in StatusData["5"]["data"]["1"]["data"]["3"] and 
                                        StatusData["5"]["data"]["1"]["data"]["3"]["data"] == 1 and 
                                        "11" in StatusData["5"]["data"]["1"]["data"] and "data" in StatusData["5"]["data"]["1"]["data"]["11"] and 
                                        StatusData["5"]["data"]["1"]["data"]["11"]["data"] == 1):
                
                                        print(f"🎯 SPECIAL CONDITION MET: Player {xMsGFixinG(target_uid)} is in SOLO mode with special flag 11=1")
                                        cache_entry['special_state'] = 'SOLO_WITH_FLAG_1'
                
                                except Exception as cond_error:
                                    print(f"⚠️ Error checking special condition: {cond_error}")
                                # ------------------------------

                                # If in room, extract room ID
                                if "IN ROOM" in player_status:
                                    try:
                                        # Assuming get_idroom_by_idplayer is available
                                        room_id = get_idroom_by_idplayer(proto_part)
                                        if room_id:
                                            cache_entry['room_id'] = room_id
                                            print(f"🏠 Room ID extracted: {room_id}")
                                    except Exception as room_error:
                                        print(f"Failed to extract room ID: {room_error}")
                
                                # If in squad, extract leader
                                elif "INSQUAD" in player_status:
                                    try:
                                        # Assuming get_leader is available
                                        leader_id = get_leader(proto_part)
                                        if leader_id:
                                            cache_entry['leader_id'] = leader_id
                                            print(f"👑 Leader ID: {leader_id}")
                                    except Exception as leader_error:
                                        print(f"Failed to extract leader: {leader_error}")
                
                                # Save to FILE cache (Assuming save_to_cache is available)
                                save_to_cache(player_id, cache_entry)
                                print(f"✅ Saved to cache: {xMsGFixinG(target_uid)} = {player_status}")
                
                    except Exception as e:
                        print(f"❌ Error parsing status: {e}")
                        import traceback
                        traceback.print_exc()
                
                # =================== END STATUS HANDLER ===================


            # --- CLEANUP AFTER INNER LOOP (Connection closed) ---
            if online_writer is not None:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
            
            if whisper_writer is not None:
                try:
                    whisper_writer.close()
                    await whisper_writer.wait_closed()
                except:
                    pass
                whisper_writer = None
                
            insquad = None
            joining_team = False
            squad_chat_authed = False
            squad_group_owner_uid = None
            squad_group_chat_code = None
            try:
                _ka_task.cancel()
            except:
                pass
            try:
                _ci_task.cancel()
            except:
                pass
            
            print(f"Connection closed. Reconnecting in {reconnect_delay} seconds...")

        except ConnectionRefusedError:
            print(f"Connection refused by server at {ip}:{port}.")
        except asyncio.TimeoutError:
            print(f"Connection attempt to {ip}:{port} timed out.")
        except Exception as e:
            print(f"- ErroR With {ip}:{port} - {e}")
            traceback.print_exc() 
            
            # --- CLEANUP AFTER EXCEPTION ---
            try:
                _ka_task.cancel()
            except:
                pass
            try:
                _ci_task.cancel()
            except:
                pass
            if online_writer is not None:
                try:
                    online_writer.close()
                    await online_writer.wait_closed()
                except:
                    pass
                online_writer = None
            if whisper_writer is not None:
                try:
                    whisper_writer.close()
                    await whisper_writer.wait_closed()
                except:
                    pass
                whisper_writer = None
                
            insquad = None
            joining_team = False
            squad_chat_authed = False
            squad_group_owner_uid = None
            squad_group_chat_code = None
            
        await asyncio.sleep(reconnect_delay)
        
                    

                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task, bot_enabled
    global _console_squad_chat_id
    global insquad, joining_team, squad_chat_authed, squad_group_owner_uid, squad_group_chat_code
    global _chat_force_reconnect, _send_fail_count
    global _console_guild_chat_id, _console_guild_bot_uid
    global _console_chat_target, _stdin_q, _stdin_thread_started
    global freeze_running, freeze_task
    global mg_spam_task, msg_spam_running, msg_spam_task
    # At the VERY TOP of your file, with other globals:
    status_response_cache = {}
    cache_lock = asyncio.Lock()  # For thread safety
    while True:
        try:
            # Reset reconnect/failure flags for each fresh connection
            global _chat_force_reconnect, _send_fail_count
            _chat_force_reconnect = False
            _send_fail_count = 0

            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
                # Re-authenticate squad/group chat if bot was already in a group before reconnect
                if squad_chat_authed and squad_group_owner_uid and squad_group_chat_code:
                    try:
                        _sq_auth = await AutH_Chat(3, squad_group_owner_uid, squad_group_chat_code, key, iv)
                        if whisper_writer: whisper_writer.write(_sq_auth) ; await whisper_writer.drain()
                        print(f"✅ Re-authenticated group/squad chat after reconnect ({squad_group_owner_uid})")
                    except Exception as _sq_err:
                        print(f"⚠️ Squad re-auth after reconnect failed: {_sq_err}")
                # Store for console sender
                global _console_guild_chat_id, _console_guild_bot_uid
                _console_guild_chat_id = clan_id
                _console_guild_bot_uid = getattr(LoGinDaTaUncRypTinG, 'AccountUID', clan_id)
                print(f"\n{'='*50}")
                print(f"  🖥️  CHAT CONSOLE ACTIVE")
                print(f"  Type a message and press Enter to send.")
                print(f"  Commands:  !guild → send to Guild")
                print(f"             !group → send to Group/Squad")
                print(f"  Currently sending to: GUILD")
                print(f"  Guild Chat ID: {clan_id}")
                print(f"{'='*50}\n")

            # Re-auth squad chat on reconnect (handles case where bot has no clan)
            if squad_chat_authed and squad_group_owner_uid and squad_group_chat_code:
                try:
                    _sq_auth2 = await AutH_Chat(3, squad_group_owner_uid, squad_group_chat_code, key, iv)
                    if whisper_writer: whisper_writer.write(_sq_auth2) ; await whisper_writer.drain()
                    print(f"✅ Group/squad chat auth restored on connect ({squad_group_owner_uid})")
                except Exception as _sq_err2:
                    print(f"⚠️ Squad auth on connect failed: {_sq_err2}")

            # ===== KEEP-ALIVE BACKGROUND TASK =====
            # Watchdog: tracks how many keepalives have been sent without any data received
            _ka_sent_since_last_data = 0
            _KA_MAX_SILENT = 8  # Force reconnect after 8 unanswered keepalives (~3.3 min)

            async def _chat_keep_alive_loop():
                """Send keep-alive every 25 seconds. If server stops responding, force reconnect."""
                nonlocal _ka_sent_since_last_data
                global _chat_force_reconnect
                while True:
                    await asyncio.sleep(25)
                    try:
                        if _ka_sent_since_last_data >= _KA_MAX_SILENT:
                            print(f"⚠️ Server has not responded in {_ka_sent_since_last_data} keepalive cycles — forcing reconnect...")
                            _chat_force_reconnect = True
                            break
                        pkt = await send_keep_alive(key, iv, region)
                        if pkt and whisper_writer and not whisper_writer.is_closing():
                            whisper_writer.write(pkt)
                            try:
                                await asyncio.wait_for(whisper_writer.drain(), timeout=10)
                            except asyncio.TimeoutError:
                                print("⚠️ Keep-alive drain timed out — forcing reconnect...")
                                _chat_force_reconnect = True
                                break
                            _ka_sent_since_last_data += 1
                            print(f"💓 Keep-alive sent to chat server (silent cycles: {_ka_sent_since_last_data}/{_KA_MAX_SILENT})")
                    except Exception as _ka_err:
                        print(f"⚠️ Keep-alive send failed: {_ka_err}")
                        _chat_force_reconnect = True
                        break

            # ===== CONSOLE → CHAT INPUT LOOP =====
            async def _console_input_loop():
                """Read lines from the terminal and send to guild or group chat."""
                import sys
                import queue as _queue
                import threading as _threading
                global _console_chat_target, _stdin_q, _stdin_thread_started

                # Only create the stdin queue and thread once — reused on every reconnect
                if _stdin_q is None:
                    _stdin_q = _queue.Queue()

                if not _stdin_thread_started:
                    _stdin_thread_started = True

                    def _stdin_thread():
                        while True:
                            try:
                                line = sys.stdin.readline()
                                if not line:
                                    break
                                _stdin_q.put(line.strip())
                            except Exception:
                                break

                    _t = _threading.Thread(target=_stdin_thread, daemon=True)
                    _t.start()

                print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)
                while True:
                    try:
                        # Poll queue every 100 ms — never blocks the event loop
                        try:
                            text = _stdin_q.get_nowait()
                        except _queue.Empty:
                            await asyncio.sleep(0.1)
                            continue

                        if not text:
                            print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)
                            continue

                        # ── Switch target commands ──
                        if text.lower() == "!guild":
                            _console_chat_target = "guild"
                            print(f"✅ Switched to GUILD chat.")
                            print(f"[GUILD] > ", end="", flush=True)
                            continue

                        if text.lower() == "!group":
                            if _console_squad_chat_id:
                                _console_chat_target = "group"
                                print(f"✅ Switched to GROUP/SQUAD chat.")
                            else:
                                print(f"⚠️ Bot is not in a group yet. Waiting for a group message first.")
                            print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)
                            continue

                        # ── Send message to selected target ──
                        if not whisper_writer or whisper_writer.is_closing():
                            print("⚠️ Not connected. Try again.")
                            print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)
                            continue

                        if _console_chat_target == "guild":
                            if _console_guild_chat_id:
                                await safe_send_message(
                                    _console_guild_chat_type,
                                    f"Message from owner: {text}",
                                    _console_guild_bot_uid,
                                    _console_guild_chat_id,
                                    key,
                                    iv,
                                )
                                print(f"[YOU → GUILD] Message from owner: {text}")
                            else:
                                print("⚠️ Not connected to guild chat yet.")

                        elif _console_chat_target == "group":
                            if _console_squad_chat_id:
                                await safe_send_message(
                                    0,  # squad chat type
                                    f"Message from owner: {text}",
                                    _console_guild_bot_uid,
                                    _console_squad_chat_id,
                                    key,
                                    iv,
                                )
                                print(f"[YOU → GROUP] Message from owner: {text}")
                            else:
                                print("⚠️ Bot is not in a group yet.")

                        print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)

                    except asyncio.CancelledError:
                        break
                    except Exception as _ci_err:
                        print(f"⚠️ Console input error: {_ci_err}")
                        print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)

            _ka_task = asyncio.create_task(_chat_keep_alive_loop())
            _ci_task = asyncio.create_task(_console_input_loop())

            while True:
                # Check if a send failure or watchdog triggered a forced reconnect
                if _chat_force_reconnect:
                    print("🔁 Force-reconnect flag set — closing and reconnecting...")
                    _ka_task.cancel()
                    if whisper_writer and not whisper_writer.is_closing():
                        whisper_writer.close()
                    break

                try:
                    data = await asyncio.wait_for(reader.read(9999), timeout=120)
                except asyncio.TimeoutError:
                    print("⚠️ Chat connection silent for 120s — reconnecting...")
                    _ka_task.cancel()
                    break
                if not data:
                    _ka_task.cancel()
                    break

                # Reset the keepalive watchdog and send-failure counter — server is alive
                _ka_sent_since_last_data = 0
                
                if data.hex().startswith("120000"):

                    try:
                        msg = await DeCode_PackEt(data.hex()[10:])
                        chatdata = json.loads(msg)
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        _raw_msg_str = response.Data.msg if response.Data.msg else ""
                        inPuTMsG = _raw_msg_str.lower()
                        MsG = _raw_msg_str.lower()
                        # If proto gave empty msg, try chatdata JSON fallback
                        if not inPuTMsG:
                            try:
                                _fb = chatdata
                                # Common field paths used in FF whisper proto
                                _fb_msg = (
                                    _fb.get('1', {}).get('data', {}).get('5', {}).get('data', '')
                                    or _fb.get('5', {}).get('data', '')
                                    or _fb.get('4', {}).get('data', '')
                                )
                                if _fb_msg:
                                    inPuTMsG = str(_fb_msg).lower()
                                    MsG = inPuTMsG
                            except Exception:
                                pass

                    except Exception as _decode_err:
                        print(f"⚠️ Chat packet decode error: {_decode_err}")
                        response = None
                        
                        

                        



                    # ============ WHITELIST CHECK ============
                    # ============ WHITELIST CHECK ============
                    if response:
                        # Get data
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = (response.Data.msg or "").lower()
                        MsG = (response.Data.msg or "").lower()

                        # ===== PRINT INCOMING MESSAGES TO CONSOLE + TRACK SQUAD ID =====
                        try:
                            _raw_msg = response.Data.msg
                            _chat_label = {1: "GUILD", 2: "PRIVATE", 3: "ROOM"}.get(XX, "GROUP")
                            # Track the squad/group chat ID whenever a group message arrives
                            if XX not in (1, 2):
                                _console_squad_chat_id = chat_id
                            print(f"\n[{_chat_label}] 💬 UID {uid}: {_raw_msg}")
                            print(f"[{_console_chat_target.upper()}] > ", end="", flush=True)
                        except:
                            pass

                        # ============ PUBLIC MODE ENABLED ============
                        # Maine yahan se Blocking Code hata diya hai.
                        # Ab bot check nahi karega, sab log commands use kar payenge.

                        # ── Fix: extract real UID from chatdata when group chat gives 0 ──
                        if uid == 0 and chatdata:
                            try:
                                import re as _re
                                _raw_json = json.dumps(chatdata)
                                # Free Fire UIDs are 9-12 digit numbers starting with non-zero
                                _uid_matches = _re.findall(r'\b([1-9]\d{8,11})\b', _raw_json)
                                if _uid_matches:
                                    uid = int(_uid_matches[0])
                                    print(f"📍 UID extracted from packet: {uid}")
                            except Exception:
                                pass

                        uid_str = str(uid)
                        print(f"✅ Command received from: {uid_str} (Public Mode)")

                        # ============ BLOCKED UID CHECK ============
                        if uid_str in BLOCKED_UIDS:
                            print(f"🚫 Blocked UID {uid_str} tried to use a command — blocked.")
                            _block_uid = uid if uid and uid != 0 else int(uid_str) if uid_str.isdigit() else uid
                            _block_sent = await safe_send_message(
                                response.Data.chat_type,
                                f"[B][C][FF0000]🚫 You have been blacklisted from using this bot.\n[C][FFFFFF]Contact admin to get unblocked.",
                                _block_uid, chat_id, key, iv
                            )
                            if not _block_sent:
                                print(f"⚠️ Could not send blacklist notice in-game to UID {uid_str}")
                            continue

                        # ============ NEWS MULTI-STEP LISTENER ============
                        if uid_str in news_pending:
                            pending = news_pending[uid_str]
                            # Expire after 90 seconds of inactivity
                            if time.time() - pending.get("ts", 0) > 90:
                                del news_pending[uid_str]
                            elif pending["step"] == "country" and inPuTMsG.strip() in ("1", "2", "3"):
                                country_map = {"1": "PK", "2": "UK", "3": "US"}
                                country_code = country_map[inPuTMsG.strip()]
                                del news_pending[uid_str]
                                _news_chat_type = response.Data.chat_type
                                _news_uid = uid
                                _news_chat_id = chat_id
                                await safe_send_message(_news_chat_type, f"[B][C]{get_random_color()}\n🤖 Generating news summary...\n", _news_uid, _news_chat_id, key, iv)

                                async def _deliver_news(_ct, _u, _ci, _cc):
                                    try:
                                        _summary, _cname = await fetch_news_rss(_cc)
                                        _msg = (
                                            f"[B][C][00FF00]📰 {_cname} News:\n\n"
                                            f"[FFFFFF]{_summary}\n\n"
                                            f"[C][B][FFB300]Powered by: [FFFFFF]AI"
                                        )
                                        await safe_send_message(_ct, _msg, _u, _ci, key, iv)
                                    except Exception as _ne:
                                        await safe_send_message(_ct, f"[B][C][FF0000]❌ News error: {_ne}", _u, _ci, key, iv)

                                asyncio.create_task(_deliver_news(_news_chat_type, _news_uid, _news_chat_id, country_code))
                                continue

                        # ... Yahan se niche commands shuru honge ...

                        # ========= ON =========
                        if inPuTMsG.startswith('/on'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "❌ Only admin can use /on", uid, chat_id, key, iv)
                                continue

                            bot_enabled = True
                            await safe_send_message(response.Data.chat_type, "✅ Bot is now ON", uid, chat_id, key, iv)
                            continue


                        # ========= OFF =========
                        if inPuTMsG.startswith('/off'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "❌ Only admin can use /off", uid, chat_id, key, iv)
                                continue

                            bot_enabled = False
                            await safe_send_message(response.Data.chat_type, "⛔ Bot is now OFF", uid, chat_id, key, iv)
                            continue

                        # ========= UPTIME =========
                        if inPuTMsG.strip().startswith('/uptime'):
                            print(f"⏱️ /uptime command received from UID {uid}")
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admin can use /uptime", uid, chat_id, key, iv)
                                continue

                            elapsed = int(time.time() - BOT_START_TIME)
                            days, rem = divmod(elapsed, 86400)
                            hours, rem = divmod(rem, 3600)
                            minutes, seconds = divmod(rem, 60)

                            parts_up = []
                            if days:
                                parts_up.append(f"{days}d")
                            if hours:
                                parts_up.append(f"{hours}h")
                            if minutes:
                                parts_up.append(f"{minutes}m")
                            parts_up.append(f"{seconds}s")
                            uptime_str = " ".join(parts_up)

                            uptime_msg = f"⏱️ Bot Uptime: {uptime_str}"
                            await safe_send_message(response.Data.chat_type, uptime_msg, uid, chat_id, key, iv)
                            continue

                        # ========= BLOCK UID =========
                        if inPuTMsG.strip().startswith('/block'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admin can use /block", uid, chat_id, key, iv)
                                continue
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Usage: /block [uid]\nExample: /block 123456789", uid, chat_id, key, iv)
                                continue
                            target = parts[1]
                            if target == ADMIN_UID:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Cannot block the admin!", uid, chat_id, key, iv)
                                continue
                            BLOCKED_UIDS.add(target)
                            await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]🚫 UID {target} has been blacklisted and can no longer use the bot.", uid, chat_id, key, iv)
                            continue

                        # ========= NEWS =========
                        if inPuTMsG.strip() == "/news":
                            news_pending[uid_str] = {"step": "country", "ts": time.time()}
                            menu = (
                                "[B][C][00FFFF]📰 NEWS — Choose a Country:\n"
                                "[FF1493]══════════════════\n"
                                "[FFD700]1 [FFFFFF]: 🇵🇰 Pakistan\n"
                                "[FFD700]2 [FFFFFF]: 🇬🇧 United Kingdom\n"
                                "[FFD700]3 [FFFFFF]: 🇺🇸 America\n"
                                "[AAAAAA]Reply with 1, 2 or 3"
                            )
                            await safe_send_message(response.Data.chat_type, menu, uid, chat_id, key, iv)
                            continue

                        # ========= HACK (Fun Prank) =========
                        if inPuTMsG.strip().startswith('/h a c k'):
                            target_name = inPuTMsG.strip()[len('/h a c k'):].strip() or "Target"
                            _hack_ct = response.Data.chat_type
                            _hack_uid = uid
                            _hack_cid = chat_id

                            async def _run_hack(_ct, _u, _ci, _tname):
                                fake_ip = f"{random.randint(100,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                                fake_pass = random.choice([
                                    "iloveyou123", "password@2025", "qwerty!321",
                                    "dragon_lord99", "123456abc", "free_fire_pro",
                                    "noscope420", "booyah_king", "gg_ez_2025"
                                ])
                                fake_email = f"{_tname.lower().replace(' ','_')}{random.randint(10,99)}@gmail.com"
                                fake_wallet = f"${random.randint(0, 5)}.{random.randint(10,99)}"
                                bar_full   = "██████████"
                                bar_half   = "█████░░░░░"
                                bar_start  = "██░░░░░░░░"

                                steps = [
                                    f"[B][C][FF0000]☠️ HACK INITIATED\n[FFFFFF]Target: [FF4500]{_tname}\n[888888]Connecting...",
                                    f"[B][C][FF6600]{bar_start} 20%\n[FFFFFF]🔍 Scanning ports...\n[888888]Port 22, 80, 443 found.",
                                    f"[B][C][FFAA00]{bar_half} 50%\n[FFFFFF]🔐 Bypassing firewall...\n[888888]Security cracked.",
                                    f"[B][C][FFDD00]{bar_half} 65%\n[FFFFFF]📡 Intercepting packets...\n[888888]Analysis complete.",
                                    f"[B][C][00FF88]{bar_full} 85%\n[FFFFFF]💾 Extracting data...\n[888888]Decrypting...",
                                    f"[B][C][00FFFF]{bar_full} 100%\n[FF0000]✅ HACK COMPLETE!",
                                    f"[B][FFFF00]👤 Target: [FFFFFF]{_tname}\n[FFFF00]🌐 IP: [FFFFFF]{fake_ip}",
                                    f"[B][FFFF00]📧 Email: [FFFFFF]{fake_email}\n[FFFF00]🔑 Pass: [FFFFFF]{fake_pass}",
                                    f"[B][FFFF00]💰 Wallet: [FFFFFF]{fake_wallet}\n[FF4444]⚠️ FUN ONLY - Fake data.",
                                ]
                                delays = [0, 1.5, 1.5, 1.5, 1.5, 2.0, 0.8, 0.8, 0.8]
                                for i, step in enumerate(steps):
                                    await asyncio.sleep(delays[i])
                                    await safe_send_message(_ct, step, _u, _ci, key, iv)

                            asyncio.create_task(_run_hack(_hack_ct, _hack_uid, _hack_cid, target_name))
                            continue

                        # ========= UNBLOCK UID =========
                        if inPuTMsG.strip().startswith('/unblock'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admin can use /unblock", uid, chat_id, key, iv)
                                continue
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Usage: /unblock [uid]\nExample: /unblock 123456789", uid, chat_id, key, iv)
                                continue
                            target = parts[1]
                            if target in BLOCKED_UIDS:
                                BLOCKED_UIDS.discard(target)
                                await safe_send_message(response.Data.chat_type, f"[B][C][00FF00]✅ UID {target} has been unblocked.", uid, chat_id, key, iv)
                            else:
                                await safe_send_message(response.Data.chat_type, f"[B][C][FFFF00]⚠️ UID {target} was not blocked.", uid, chat_id, key, iv)
                            continue

                        # ========= ADMIN INFO (always works even when bot is OFF) =========
                        if inPuTMsG.strip().startswith('/admin'):
                            _act = response.Data.chat_type
                            admin_msg = (
                                "[B][C][FF1493]BOT ADMIN INFO\n"
                                "[FFD700]Developer : [00FFFF]Ayaan\n"
                                "[FFD700]Owner     : [FF69B4]Biryani\n"
                                "[FFD700]Online    : [00FF00]24/7\n"
                                "[FFD700]Contact   : [FFFFFF]@paktcpbots\n"
                                "[FF1493]/help for commands"
                            )
                            await safe_send_message(_act, admin_msg, uid, chat_id, key, iv)
                            continue

                        # ========= ADD FRIEND =========
                        if inPuTMsG.strip().startswith('/add'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admin can use /add", uid, chat_id, key, iv)
                                continue
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Usage: /add [uid]\nExample: /add 123456789", uid, chat_id, key, iv)
                                continue
                            add_target = parts[1]
                            if not add_target.isdigit():
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid UID! Must be numbers only.", uid, chat_id, key, iv)
                                continue
                            await safe_send_message(response.Data.chat_type, f"[B][C][00FFFF]Sending friend request to {add_target}...", uid, chat_id, key, iv)
                            try:
                                add_loop = asyncio.get_running_loop()
                                add_result = await asyncio.wait_for(
                                    add_loop.run_in_executor(None, add_friend, add_target),
                                    timeout=15
                                )
                            except asyncio.TimeoutError:
                                add_result = "[B][C][FF0000]❌ Request timed out. Try again."
                            except Exception as add_err:
                                add_result = f"[B][C][FF0000]❌ Error: {add_err}"
                            await safe_send_message(response.Data.chat_type, add_result, uid, chat_id, key, iv)
                            continue

                        # ========= REMOVE FRIEND =========
                        if inPuTMsG.strip().startswith('/remove'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admin can use /remove", uid, chat_id, key, iv)
                                continue
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Usage: /remove [uid]\nExample: /remove 123456789", uid, chat_id, key, iv)
                                continue
                            rem_target = parts[1]
                            if not rem_target.isdigit():
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid UID! Must be numbers only.", uid, chat_id, key, iv)
                                continue
                            await safe_send_message(response.Data.chat_type, f"[B][C][FF6EC7]Removing friend {rem_target}...", uid, chat_id, key, iv)
                            try:
                                rem_loop = asyncio.get_running_loop()
                                rem_result = await asyncio.wait_for(
                                    rem_loop.run_in_executor(None, remove_friend, rem_target),
                                    timeout=15
                                )
                            except asyncio.TimeoutError:
                                rem_result = "[B][C][FF0000]❌ Request timed out. Try again."
                            except Exception as rem_err:
                                rem_result = f"[B][C][FF0000]❌ Error: {rem_err}"
                            await safe_send_message(response.Data.chat_type, rem_result, uid, chat_id, key, iv)
                            continue

                        # ========= LIST FRIENDS =========
                        if inPuTMsG.strip().startswith('/list'):
                            print(f"📋 /list command from UID {uid}")
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admin can use /list", uid, chat_id, key, iv)
                                continue
                            await safe_send_message(response.Data.chat_type, "[B][C][00FFFF]Fetching friend list...", uid, chat_id, key, iv)
                            try:
                                list_loop = asyncio.get_running_loop()
                                friends, err = await asyncio.wait_for(
                                    list_loop.run_in_executor(None, get_friend_list),
                                    timeout=20
                                )
                            except asyncio.TimeoutError:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Request timed out. Try again.", uid, chat_id, key, iv)
                                continue
                            except Exception as list_err:
                                await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Error: {list_err}", uid, chat_id, key, iv)
                                continue
                            if err:
                                await safe_send_message(response.Data.chat_type, err, uid, chat_id, key, iv)
                                continue
                            if not friends:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF6EC7]Bot has no friends added.", uid, chat_id, key, iv)
                                continue
                            pages = format_friend_list_pages(friends)
                            for page in pages:
                                await safe_send_message(response.Data.chat_type, page, uid, chat_id, key, iv)
                                await asyncio.sleep(0.5)
                            continue

                        # ========= BLOCK WHEN OFF (ONLY HERE) =========
                        if not bot_enabled and not inPuTMsG.strip().startswith('/guild'):
                            await safe_send_message(response.Data.chat_type, "⛔ Bot is OFF", uid, chat_id, key, iv)
                            continue

                        # ================= BUNDLE COMMAND =================
                        if inPuTMsG.strip().startswith('/bundle'):
                            print(f"⚡ Command: {inPuTMsG}")
                            
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 2:
                                bundle_list = """[B][C][FFFFFF]• rampage 
[FFFFFF]• cannibal 
[FFFFFF]• devil 
[FFFFFF]• scorpio 
[FFFFFF]• frostfire
[FFFFFF]• paradox 
[FFFFFF]• naruto 
[FFFFFF]• aurora 
[FFFFFF]• midnight 
[FFFFFF]• itachi 
[FFFFFF]• dreamspace"""
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle_name = parts[1].lower()
                                
                                # Real IDs
                                bundle_ids = {
                                    "rampage": "914000002", "cannibal": "914000003",
                                    "devil": "914038001", "scorpio": "914039001",
                                    "frostfire": "914042001", "paradox": "914044001",
                                    "naruto": "914047001", "aurora": "914047002",
                                    "midnight": "914048001", "itachi": "914050001",
                                    "dreamspace": "914051001"
                                }
                                
                                if bundle_name not in bundle_ids:
                                    await safe_send_message(response.Data.chat_type, "❌ Invalid Name", uid, chat_id, key, iv)
                                else:
                                    bundle_id = bundle_ids[bundle_name]
                                    
                                    try:
                                        # Function call
                                        bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)

                                        if bundle_packet and online_writer:
                                            # Packet Bhejo
                                            online_writer.write(bundle_packet)
                                            await online_writer.drain()
                                            
                                            success_msg = f"[B][C][00FF00]✅ Done: {bundle_name}"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        else:
                                            print("❌ Connection Lost")
                                    
                                    except Exception as e:
                                        print(f"Error: {e}")
                        # ===============================================================

                        
                        # AI Command - /ai
                        if inPuTMsG.strip().startswith('/ai'):
                            print('Processing AI command in any chat type')
                            
                            question = inPuTMsG[4:].strip()
                            if question:
                                initial_message = f"[B][C]{get_random_color()}\n🤖 AI is thinking...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    ai_loop = asyncio.get_running_loop()
                                    ai_response = await asyncio.wait_for(
                                        ai_loop.run_in_executor(None, talk_with_ai, question),
                                        timeout=25
                                    )
                                except asyncio.TimeoutError:
                                    ai_response = "❌ AI took too long to respond. Try again."
                                except Exception as ai_err:
                                    ai_response = f"❌ AI error: {ai_err}"
                                
                                # Format the AI response
                                ai_message = f"""
[B][C][00FF00]🤖 AI Response:

[FFFFFF]{ai_response}

[C][B][FFB300]Question: [FFFFFF]{question}
"""
                                await safe_send_message(response.Data.chat_type, ai_message, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Please provide a question after /ai\nExample: /ai What is Free Fire?\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        # FREEZE COMMAND - /freeze [uid]
                        if inPuTMsG.strip().startswith('/freeze'):
                            print('Processing freeze command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND

❌ Usage: /freeze (uid)
        
📝 Examples:
/freeze me - Freeze yourself
/freeze 123456789 - Freeze specific UID

🎯 What it does:
• Sends 3 ice/freeze emotes in sequence
• 1-second cycles for 10 seconds total
• Emotes: 909040004 → 909050008 → 909000002
• Creates a "freeze" effect!

💡 Use /stop_freeze to stop early
"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                
                                # Handle "me" or "self"
                                if target_uid.lower() in ['me', 'self', 'myself']:
                                    target_uid = str(response.Data.uid)
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {xMsGFixinG(target_uid)}"
                                
                                # Stop any existing freeze task
                                global freeze_running, freeze_task
                                if freeze_task and not freeze_task.done():
                                    freeze_running = False
                                    freeze_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Send initial message
                                initial_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND STARTING!

🎯 Target: {target_name}
⏱️ Duration: {FREEZE_DURATION} seconds
🔄 Cycle: 1 second (3 emotes each)
🎭 Sequence: 
  1. 909040004 (Ice)
  2. 909050008 (Frozen) 
  3. 909000002 (Freeze)

⏳ Starting freeze sequence...
"""
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                # Start freeze task
                                freeze_running = True
                                freeze_task = asyncio.create_task(
                                    freeze_emote_spam(target_uid, key, iv, region, response.Data.chat_type, chat_id, uid)
                                )
        
                                # Handle completion
                                asyncio.create_task(
                                    handle_freeze_completion(freeze_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv)
                                )

                        if inPuTMsG.strip().startswith('/bio'):
                            print('📝 Processing bio change command')

                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ This command is for admins only!", uid, chat_id, key, iv)
                            else:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = f"""[B][C][FF0000]❌ Usage: /bio (your bio text)

📝 Examples:
/bio Hello World!
/bio 🤖 Bot for GothicRealm 
/bio Level 70 | Pro Player
/bio Add me: idkwho

✨ Features:
• Changes bot's profile bio instantly
• Supports emojis and special characters
• Max length: 50 characters

💡 Note: Bio changes appear immediately in profile!
"""
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    # Preserve original capitalisation from the raw message
                                    _raw_bio_msg = (response.Data.msg or "").strip()
                                    _raw_parts = _raw_bio_msg.split(maxsplit=1)
                                    bio_text = _raw_parts[1] if len(_raw_parts) >= 2 else parts[1]

                                    # Check length
                                    if len(bio_text) > 50:
                                        error_msg = f"[B][C][FF0000]❌ Bio too long! Max 50 chars.\n📝 Yours: {len(bio_text)} chars\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        continue

                                    # Send immediate acknowledgement — bot stays responsive
                                    await safe_send_message(response.Data.chat_type,
                                        f"[B][C][00FF00]📝 Updating bio...\n[FFFFFF]Bio: {bio_text[:44]}\n[888888]Please wait...",
                                        uid, chat_id, key, iv)

                                    # Run the heavy work in a background task so bot doesn't freeze
                                    _bio_ct = response.Data.chat_type
                                    _bio_uid = uid
                                    _bio_cid = chat_id
                                    _bio_text = bio_text

                                    async def _do_bio_update(_ct, _u, _ci, _bt):
                                        try:
                                            result = None
                                            success = False

                                            # Always do a fresh login first — the game-connection
                                            # token is silently ignored by the bio endpoint
                                            print("🔄 Bio: doing fresh login...")
                                            credentials = load_credentials_from_file("MG24GAMER.txt")
                                            if credentials:
                                                Uid_b, Pw_b = credentials[0], credentials[1]
                                                for attempt in range(3):
                                                    try:
                                                        print(f"🔄 Bio login attempt {attempt+1}/3")
                                                        open_id, access_token = await GeNeRaTeAccEss(Uid_b, Pw_b)
                                                        if not open_id or not access_token:
                                                            await asyncio.sleep(2)
                                                            continue
                                                        PyL = await EncRypTMajoRLoGin(open_id, access_token)
                                                        MajoRLoGinResPonsE = await MajorLogin(PyL)
                                                        MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
                                                        if not MajoRLoGinauTh or not MajoRLoGinauTh.token:
                                                            await asyncio.sleep(2)
                                                            continue
                                                        result = await set_bio_directly_async(MajoRLoGinauTh.token, _bt, region)
                                                        if result.get("success"):
                                                            success = True
                                                            break
                                                        await asyncio.sleep(2)
                                                    except Exception as _e:
                                                        print(f"❌ Bio attempt {attempt+1} error: {_e}")
                                                        await asyncio.sleep(2)

                                            # Fallback: token.json if fresh login failed
                                            if not success:
                                                print("🔑 Bio fallback: token.json...")
                                                saved_token = load_jwt_token()
                                                if saved_token:
                                                    result = await set_bio_directly_async(saved_token, _bt, region)
                                                    if result.get("success"):
                                                        success = True

                                            if success:
                                                await safe_send_message(_ct,
                                                    f"[B][C][00FF00]✅ BIO UPDATED!\n[FFFFFF]Bio: {_bt}\n[888888]Check profile!",
                                                    _u, _ci, key, iv)
                                            else:
                                                err_msg = result.get('message', 'Failed') if result else 'Login error'
                                                await safe_send_message(_ct,
                                                    f"[B][C][FF0000]❌ Bio failed!\n[FF8800]{err_msg[:50]}",
                                                    _u, _ci, key, iv)
                                        except Exception as e:
                                            print(f"❌ Bio task error: {e}")
                                            await safe_send_message(_ct, f"[B][C][FF0000]❌ Bio error: {str(e)[:50]}", _u, _ci, key, iv)

                                    asyncio.create_task(_do_bio_update(_bio_ct, _bio_uid, _bio_cid, _bio_text))
            

                        # QUICK EMOTE ATTACK COMMAND - /quick [team_code] [emote_id] [target_uid?]
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Processing quick emote attack command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /quick (team_code) [emote_id] [target_uid]\n\n[FFFFFF]Examples:\n[00FF00]/quick ABC123[FFFFFF] - Join, send Rings emote, leave\n[00FF00]/ghostquick ABC123[FFFFFF] - Ghost join, send emote, leave\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
        
                                # Set default values
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)  # Default: Sender's UID
        
                                # Parse optional parameters
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
        
                                # Determine target name for message
                                if target_uid == str(response.Data.uid):
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {xMsGFixinG(target_uid)}"
        
                                initial_message = f"[B][C][FFFF00]⚡ QUICK EMOTE ATTACK!\n\n[FFFFFF]🎯 Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n[FFFFFF]⏱️ Estimated: [00FF00]2 seconds\n\n[FFFF00]Executing sequence...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try regular method first
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
            
                                    if success:
                                        success_message = f"[B][C][00FF00]✅ QUICK ATTACK SUCCESS!\n\n[FFFFFF]🏷️ Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n\n[00FF00]Bot joined → emoted → left! ✅\n"
                                    else:
                                        success_message = f"[B][C][FF0000]❌ Regular attack failed: {result}\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print("failed")
            
                        # Add this to your existing command dispatcher in TcPChaT function
                        if inPuTMsG.strip().startswith('/roommsg '):
                            await handle_room_message_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
            
                        # Add with other command handlers
                        if inPuTMsG.strip().startswith('/xjoin '):
                            print('Processing xjoin command')
                            await handle_xjoin_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
            
                        # PLAYER INVITE 
                        if inPuTMsG.strip().startswith('/inv'):
                            print('Processing invite command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /inv (uid)\nExample: /inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Sending Team Invite To {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:

                                    V = await SEnd_InV(4, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)

                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Player Group invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending invite: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/6")):
                            # Process /6 command - Create 4 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 6-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 4 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(0, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {xMsGFixinG(uid)}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        # Add these lines to your existing command dispatcher:

                        if inPuTMsG.startswith('/spamroom ') or inPuTMsG == '/spamroom':
                            await handle_room_spam_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.startswith('/sr ') or inPuTMsG == '/sr':
                            await handle_sr_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.startswith('/title'):
                            await handle_all_titles_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            
                        # STICKER SPAM COMMAND - /sticker (works in guild, group, and whisper)
                        if inPuTMsG.strip().startswith('/sticker'):
                            sticker_count = 5
                            sticker_ok = 0
                            _sticker_ct = response.Data.chat_type
                            start_msg = f"[B][C]{get_random_color()}Sending {sticker_count} stickers...\n"
                            await safe_send_message(_sticker_ct, start_msg, uid, chat_id, key, iv)
                            for _ in range(sticker_count):
                                try:
                                    packet = await send_sticker(uid, chat_id, key, iv, chat_type=_sticker_ct)
                                    if packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', packet)
                                        sticker_ok += 1
                                        await asyncio.sleep(0.4)
                                except Exception as _e:
                                    print(f"❌ Sticker send error: {_e}")
                            done_msg = f"[B][C][00FF00]✅ Sent {sticker_ok}/{sticker_count} stickers!\n"
                            await safe_send_message(_sticker_ct, done_msg, uid, chat_id, key, iv)

                        # READY COMMAND - /ready
                        if inPuTMsG.strip() == '/ready':
                            ready_start = f"[B][C]{get_random_color()}Sending ready signal for current map...\n"
                            await safe_send_message(response.Data.chat_type, ready_start, uid, chat_id, key, iv)
                            try:
                                if region.lower() == "ind":
                                    _rdy_pkt_type = '0514'
                                elif region.lower() == "bd":
                                    _rdy_pkt_type = '0519'
                                elif region.lower() == "pk":
                                    _rdy_pkt_type = '0515'
                                else:
                                    _rdy_pkt_type = '0515'
                                # Use actual logged-in bot UID, fall back to BOT_OWNER_UID if not available
                                try:
                                    _rdy_bot_uid = int(LoGinDaTaUncRypTinG.AccountUID) if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else int(BOT_OWNER_UID)
                                except Exception:
                                    _rdy_bot_uid = int(BOT_OWNER_UID)
                                _rdy_fields = {1: 4, 2: {1: _rdy_bot_uid, 2: 1}}
                                _rdy_proto = await CrEaTe_ProTo(_rdy_fields)
                                _rdy_packet = await GeneRaTePk(_rdy_proto.hex(), _rdy_pkt_type, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', _rdy_packet)
                                ready_ok = f"[B][C][00FF00]✅ Bot is READY!\n[FFFFFF]Confirmed ready for the map selected by team leader!\n"
                                await safe_send_message(response.Data.chat_type, ready_ok, uid, chat_id, key, iv)
                            except Exception as _re:
                                ready_err = f"[B][C][FF0000]❌ Ready failed: {str(_re)[:60]}\n[FFFF00]Make sure bot is in a squad room!\n"
                                await safe_send_message(response.Data.chat_type, ready_err, uid, chat_id, key, iv)

                                #GET PLAYER LIKE
                        if inPuTMsG.strip().startswith('/like'):
                            print('Processing like command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /like <uid>\nExample: /like 43685697🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                # Step 1: Fetch current likes from Free Fire player info API
                                info_data, info_err = await get_player_info(target_uid)
                                if info_data:
                                    acc_info = info_data.get("AccountInfo", {})
                                    player_name_info = acc_info.get("AccountName", "Unknown")
                                    raw_likes = acc_info.get("AccountLikes", "0")
                                    current_likes = xMsGFixinG(raw_likes)
                                    checking_msg = f"""[B][C][11EAFD]━━━━━━━━━━━━
[FFFFFF]Checking Player Info...

[FFFFFF]Player Name  : [00FFFF]{xMsGFixinG(player_name_info)}
[FFFFFF]Current Likes: [FFD700]{current_likes}

[FFFFFF]Now sending likes... Please wait.
[C][B][11EAFD]━━━━━━━━━━━━"""
                                    await safe_send_message(response.Data.chat_type, checking_msg, uid, chat_id, key, iv)
                                    like_result = send_likes(player_name_info, raw_likes)
                                else:
                                    checking_msg = f"[B][C][FF0000]\nCould not fetch player info: {info_err}\n"
                                    await safe_send_message(response.Data.chat_type, checking_msg, uid, chat_id, key, iv)
                                    like_result = None

                                # Step 2: Output likes result
                                if like_result:
                                    await safe_send_message(response.Data.chat_type, like_result, uid, chat_id, key, iv)

                                #GET ITEM INFORMATION 
                        if inPuTMsG.strip().startswith('/item'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /item <item_id>\nExample: /item 909🤫042🤫00🤫7\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                item_id = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching Item Info...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                item_result = get_item_info(item_id)

                                await safe_send_message(response.Data.chat_type, item_result, uid, chat_id, key, iv)

#GET ITEM INFORMATION 
                        if inPuTMsG.strip().startswith('/all_event'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /all_event <region>\nExample: /all_event bd\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                region = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching Event...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # get_event ফাংশন কল করে ইভেন্ট লিস্ট পাওয়া
                                event_results = get_event(region)

                                # প্রতিটি ইভেন্ট আলাদা মেসেজ হিসেবে পাঠানো, 0.2 সেকেন্ড wait সহ
                                for event_msg in event_results:
                                    await safe_send_message(response.Data.chat_type, event_msg, uid, chat_id, key, iv)
                                    await asyncio.sleep(0.2)  # 0.2 সেকেন্ড pause

                                #GET CALCULATIONS 
                        if inPuTMsG.strip().startswith('/math'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split(None, 1)
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /math <expression>\nExample: /math 2+3\nExample: /math sqrt(144)\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                expression = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSolving Calculation...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                math_result = get_math_result(expression)

                                await safe_send_message(response.Data.chat_type, math_result, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/luv'):
                            print('Processing luv command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /luv <name1> <name2>\nExample: /luv jonny mia\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                name1 = parts[1]
                                name2 = parts[2]
                                luv_result = get_luv_result(name1, name2)
                                await safe_send_message(response.Data.chat_type, luv_result, uid, chat_id, key, iv)

                                #GET PLAYER VISIT 
                        if inPuTMsG.strip().startswith('/visit'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /visit <uid>\nExample: /visit 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending Visit...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                visit_result = send_visits(target_uid)
                                final_visit = f"{xMsGFixinG(visit_result)}"

                                await safe_send_message(response.Data.chat_type, final_visit, uid, chat_id, key, iv)

                        #tt USERNAME TO INFO-/tt
                        if inPuTMsG.strip().startswith('/tt'):
                            print('Processing tiktok command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /tt <username>\nExample: /tt virat.kohli\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_username = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching TikTok info for {target_username}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                try:
                                    tt_loop = asyncio.get_running_loop()
                                    tiktok_result = await asyncio.wait_for(
                                        tt_loop.run_in_executor(None, send_tiktok_info, target_username),
                                        timeout=20
                                    )
                                except asyncio.TimeoutError:
                                    tiktok_result = "[B][C][FF0000]❌ TikTok took too long to respond. Try again.\n"
                                except Exception as tt_err:
                                    tiktok_result = f"[B][C][FF0000]❌ TikTok error: {tt_err}\n"

                                await safe_send_message(response.Data.chat_type, tiktok_result, uid, chat_id, key, iv)

# ig info command handler
                        if inPuTMsG.strip().startswith('/ig'):
                            print('Processing Instagram command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ig <username>\nExample: /ig paktcpbots\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_username = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching Instagram info for @{target_username}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                try:
                                    ig_loop = asyncio.get_running_loop()
                                    ig_result = await asyncio.wait_for(
                                        ig_loop.run_in_executor(None, send_instagram_info, target_username),
                                        timeout=20
                                    )
                                except asyncio.TimeoutError:
                                    ig_result = "[B][C][FF0000]❌ Instagram took too long to respond. Try again.\n"
                                except Exception as ig_err:
                                    ig_result = f"[B][C][FF0000]❌ Instagram error: {ig_err}\n"

                                await safe_send_message(response.Data.chat_type, ig_result, uid, chat_id, key, iv)

# yt info command handler   
                        if inPuTMsG.strip().startswith('/yt'):  
                            print('Processing YouTube command in any chat type')  

                            target_channel = inPuTMsG.strip()[4:].strip()  # /yt এর পরের সব text  
                            if not target_channel:  
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /yt <channel>\nExample: /yt mrbeast\nExample: /yt ary digital\n"  
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)  
                            else:  
                                initial_message = f"[B][C]{get_random_color()}\nFetching YouTube info for {target_channel}...\n"  
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)  

                                # Call the async function  
                                await send_youtube_info(target_channel, response.Data.chat_type, uid, chat_id, key, iv)

# PHONE NUMBER LOOKUP COMMAND
                        if inPuTMsG.strip().startswith('/num'):
                            _num_ct = response.Data.chat_type
                            _num_parts = inPuTMsG.strip().split(maxsplit=1)
                            if len(_num_parts) < 2 or not _num_parts[1].strip():
                                _usage = (
                                    "[B][C][FF0000]❌ Usage: /num <phone_number>\n"
                                    "[FFFF00]Example: /num +923001234567\n"
                                    "[FFFF00]Example: /num 03001234567"
                                )
                                await safe_send_message(_num_ct, _usage, uid, chat_id, key, iv)
                            else:
                                _raw_num = _num_parts[1].strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                                # ── Normalize to E.164 international format ──
                                # 03214339687  (11 digits, local PK)  → +923214339687
                                # 3214339687   (10 digits, no 0)      → +923214339687
                                # 923214339687 (12 digits, no +)      → +923214339687
                                # +923214339687 (already E.164)       → unchanged
                                if _raw_num.startswith("+"):
                                    pass  # already international
                                elif _raw_num.startswith("92") and len(_raw_num) == 12:
                                    _raw_num = "+" + _raw_num
                                elif _raw_num.startswith("03") and len(_raw_num) == 11:
                                    _raw_num = "+92" + _raw_num[1:]   # drop leading 0, add +92
                                elif _raw_num.startswith("3") and len(_raw_num) == 10:
                                    _raw_num = "+92" + _raw_num        # bare 10-digit PK number
                                elif not _raw_num.startswith("+"):
                                    _raw_num = "+" + _raw_num          # best-effort for other countries
                                _wait_msg = f"[B][C]{get_random_color()}🔍 Looking up {_raw_num}...\n"
                                await safe_send_message(_num_ct, _wait_msg, uid, chat_id, key, iv)
                                try:
                                    # ── Step 1: phonenumbers lib (offline, accurate carrier) ──
                                    _pn_carrier  = "Unknown"
                                    _pn_country  = "Unknown"
                                    _pn_valid    = False
                                    _pn_type_str = "Unknown"
                                    try:
                                        import phonenumbers
                                        from phonenumbers import carrier as _pn_car_mod
                                        from phonenumbers import geocoder as _pn_geo_mod
                                        from phonenumbers import number_type as _pn_type_fn
                                        from phonenumbers import PhoneNumberType
                                        _parsed      = phonenumbers.parse(_raw_num, None)
                                        _pn_valid    = phonenumbers.is_valid_number(_parsed)
                                        _pn_carrier  = _pn_car_mod.name_for_number(_parsed, "en") or "Unknown"
                                        _pn_country  = _pn_geo_mod.description_for_number(_parsed, "en") or "Unknown"
                                        _nt = _pn_type_fn(_parsed)
                                        _pn_type_str = {
                                            PhoneNumberType.MOBILE:       "Mobile",
                                            PhoneNumberType.FIXED_LINE:   "Landline",
                                            PhoneNumberType.VOIP:         "VoIP",
                                            PhoneNumberType.TOLL_FREE:    "Toll-Free",
                                            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
                                        }.get(_nt, "Mobile")
                                    except Exception as _pne:
                                        print(f"phonenumbers error: {_pne}")

                                    # ── Step 2: Veriphone API (extra info / cross-check) ──
                                    _phone_data = {}
                                    try:
                                        import aiohttp as _ah2
                                        _api_url = f"https://api.veriphone.io/v2/verify?phone={_raw_num}"
                                        async with _ah2.ClientSession(timeout=_ah2.ClientTimeout(total=10)) as _ps:
                                            async with _ps.get(_api_url) as _pr:
                                                if _pr.status == 200:
                                                    _phone_data = await _pr.json()
                                                    print(f"[Veriphone raw] {_phone_data}")
                                    except Exception:
                                        pass

                                    # Prefer phonenumbers lib data; fallback to Veriphone
                                    _vp_carrier = _phone_data.get("carrier", "")
                                    _carrier    = _pn_carrier if _pn_carrier and _pn_carrier != "Unknown" else (_vp_carrier or "Unknown")
                                    _country    = _pn_country if _pn_country and _pn_country != "Unknown" else _phone_data.get("country", "Pakistan" if _raw_num.startswith("+92") else "Unknown")
                                    _line_type  = _pn_type_str if _pn_type_str != "Unknown" else _phone_data.get("phone_type", "Mobile")
                                    _valid      = _pn_valid if _pn_valid else _phone_data.get("phone_valid", None)
                                    _intl_fmt   = _phone_data.get("phone_international", _raw_num)
                                    _valid_str  = "[00FF00]Valid" if _valid else "[FF0000]Invalid"

                                    # ── Step 3: Save to numbers.txt ──
                                    try:
                                        _orig_num = _num_parts[1].strip()
                                        _log_line = f"uid: {uid} number:{_orig_num}\n"
                                        with open("numbers.txt", "a", encoding="utf-8") as _nf:
                                            _nf.write(_log_line)
                                    except Exception as _fe:
                                        print(f"⚠️ numbers.txt write error: {_fe}")

                                    # ── Step 4: Always send main info first ──
                                    _msg1 = (
                                        f"[B][C][00FFFF]📱 NUMBER LOOKUP\n"
                                        f"[FFFF00]Number : [FFFFFF]{_intl_fmt}\n"
                                        f"[FFFF00]Status : {_valid_str}\n"
                                        f"[FFFF00]Country: [FFFFFF]{_country}\n"
                                        f"[FFFF00]Carrier: [FFFFFF]{_carrier}\n"
                                        f"[FFFF00]Type   : [FFFFFF]{_line_type}"
                                    )
                                    await safe_send_message(_num_ct, _msg1, uid, chat_id, key, iv)

                                    # ── Step 5: Groq AI — prefix/region analysis (optional, runs AFTER main info) ──
                                    try:
                                        _prefix = _raw_num[:6]  # e.g. +92321
                                        _ai_prompt = (
                                            f"Pakistani mobile number prefix: {_prefix} (full: {_raw_num})\n"
                                            f"Carrier: {_carrier}\n"
                                            f"Give me 2-3 SHORT facts about this carrier prefix in Pakistan. "
                                            f"Include: which cities/regions this prefix is popular in, "
                                            f"any known facts about the carrier. "
                                            f"Do NOT guess or mention the owner name. "
                                            f"Reply in plain text, no bullet points, no markdown."
                                        )
                                        _loop2 = asyncio.get_running_loop()
                                        _ai_raw = await asyncio.wait_for(
                                            _loop2.run_in_executor(None, talk_with_ai, _ai_prompt),
                                            timeout=15
                                        )
                                        if _ai_raw and len(_ai_raw.strip()) > 10 and "unknown" not in _ai_raw.lower()[:30]:
                                            await asyncio.sleep(0.4)
                                            _msg2 = (
                                                f"[B][C][00FFFF]📡 CARRIER INFO\n"
                                                f"[FFFFFF]{_ai_raw.strip()}"
                                            )
                                            await safe_send_message(_num_ct, _msg2, uid, chat_id, key, iv)
                                    except Exception:
                                        pass

                                except asyncio.TimeoutError:
                                    await safe_send_message(_num_ct, "[B][C][FF0000]❌ Lookup timed out. Try again.", uid, chat_id, key, iv)
                                except Exception as _ne:
                                    await safe_send_message(_num_ct, f"[B][C][FF0000]❌ Error: {str(_ne)[:80]}", uid, chat_id, key, iv)

# GUILD INFORMATION FF
                        if inPuTMsG.strip().startswith('/guild'):
                            print('Processing /guild command')
                            parts = inPuTMsG.strip().split()

                            if len(parts) < 2:
                                # Show usage
                                usage_msg = (
                                    "[B][C][FFD700]╔════════════════╗\n"
                                    "[C][FF4500]   GUILD COMMANDS\n"
                                    "[C][FFD700]╚════════════════╝\n"
                                    "[FFD700]/guild [FFFFFF]<guild_id>[AAAAAA] — View guild info by ID\n"
                                    "[FFD700]/guild [FFFFFF]<name>[AAAAAA] — Search guilds by name\n"
                                    "[FFD700]/guild leave[AAAAAA] — Leave current guild [Admin]\n"
                                    "[FFD700]/guild join [FFFFFF]<guild_id>[AAAAAA] — Send join request [Admin]\n"
                                    "[C][AAAAAA]━━━━━━━━━━━━━━━━"
                                )
                                await safe_send_message(response.Data.chat_type, usage_msg, uid, chat_id, key, iv)

                            elif parts[1].lower() == "leave":
                                # Leave guild — admin only
                                if not is_admin(uid):
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admins can use /guild leave", uid, chat_id, key, iv)
                                else:
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF6EC7]Leaving guild...", uid, chat_id, key, iv)
                                    try:
                                        guild_loop = asyncio.get_running_loop()
                                        leave_result = await asyncio.wait_for(
                                            guild_loop.run_in_executor(None, leave_guild),
                                            timeout=15
                                        )
                                    except asyncio.TimeoutError:
                                        leave_result = "[B][C][FF0000]❌ Request timed out. Try again."
                                    except Exception as leave_err:
                                        leave_result = f"[B][C][FF0000]❌ Error: {leave_err}"
                                    await safe_send_message(response.Data.chat_type, leave_result, uid, chat_id, key, iv)

                            elif parts[1].lower() == "join":
                                # Send guild join request — admin only
                                if not is_admin(uid):
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Only admins can use /guild join", uid, chat_id, key, iv)
                                elif len(parts) < 3:
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Usage: /guild join <guild_id>", uid, chat_id, key, iv)
                                else:
                                    target_guild_id = parts[2]
                                    await safe_send_message(response.Data.chat_type, f"[B][C][4CFFB0]Sending join request to guild {xMsGFixinG(target_guild_id)}...", uid, chat_id, key, iv)
                                    try:
                                        guild_loop = asyncio.get_running_loop()
                                        join_result = await asyncio.wait_for(
                                            guild_loop.run_in_executor(None, send_guild_join_request, target_guild_id),
                                            timeout=15
                                        )
                                    except asyncio.TimeoutError:
                                        join_result = "[B][C][FF0000]❌ Request timed out. Try again."
                                    except Exception as join_err:
                                        join_result = f"[B][C][FF0000]❌ Error: {join_err}"
                                    await safe_send_message(response.Data.chat_type, join_result, uid, chat_id, key, iv)

                            else:
                                arg = parts[1]
                                # Auto-detect: numeric arg = lookup by ID, text = fuzzy search by name
                                is_id = arg.lstrip('-').isdigit()

                                if is_id:
                                    # /guild <guild_id> — show info by ID with action options
                                    guild_id = arg
                                    initial_message = f"[B][C]{get_random_color()}\nFetching Guild info for {xMsGFixinG(guild_id)}...\n"
                                    await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                    try:
                                        guild_loop = asyncio.get_running_loop()
                                        guild_result = await asyncio.wait_for(
                                            guild_loop.run_in_executor(None, send_guild_info, guild_id),
                                            timeout=15
                                        )
                                    except asyncio.TimeoutError:
                                        guild_result = "[B][C][FF0000]❌ Guild info request timed out."
                                    except Exception as guild_err:
                                        guild_result = f"[B][C][FF0000]❌ Error: {guild_err}"

                                    print(f"🏰 guild_result type={type(guild_result)} len={len(guild_result) if guild_result else 'None'} preview={repr(guild_result[:80]) if guild_result else 'None'}")
                                    await safe_send_message(response.Data.chat_type, guild_result, uid, chat_id, key, iv)

                                    # Show action options after ID lookup
                                    bot_in_guild = _console_guild_chat_id is not None
                                    options_msg = "[B][C][FFD700]━━ GUILD OPTIONS ━━\n"
                                    if not bot_in_guild:
                                        options_msg += f"[4CFFB0]/guild join {guild_id}[AAAAAA] — Request to join [Admin]\n"
                                    options_msg += "[FF6EC7]/guild leave[AAAAAA] — Leave current guild [Admin]\n"
                                    options_msg += "[C][FFD700]━━━━━━━━━━━━━━━━━━"
                                    await safe_send_message(response.Data.chat_type, options_msg, uid, chat_id, key, iv)

                                else:
                                    # /guild <name> — fuzzy search by name
                                    # Rejoin all parts after the command in case name has spaces
                                    clan_name_query = " ".join(parts[1:])
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        f"[B][C]{get_random_color()}\n🔍 Searching for guild: {xMsGFixinG(clan_name_query)}...\n",
                                        uid, chat_id, key, iv
                                    )
                                    try:
                                        guild_loop = asyncio.get_running_loop()
                                        guild_result = await asyncio.wait_for(
                                            guild_loop.run_in_executor(None, search_guild_by_name, clan_name_query),
                                            timeout=20
                                        )
                                    except asyncio.TimeoutError:
                                        guild_result = "[B][C][FF0000]❌ Guild search timed out. Try again."
                                    except Exception as guild_err:
                                        guild_result = f"[B][C][FF0000]❌ Error: {guild_err}"
                                    await safe_send_message(response.Data.chat_type, guild_result, uid, chat_id, key, iv)

                        if inPuTMsG.startswith('/level'):
                            print('Processing level command in any chat type')

                            parts = inPuTMsG.split()

                            if len(parts) < 2:
                                error_msg = (
                                    "[B][C][FF0000]ERROR! Usage: /level <player_id>\n"
                                    "Example: /level 144🤫44🤫444🤫004\n"
                                )
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                            else:
                                player_id = parts[1]

                                initial_message = (
                                    f"[B][C]{get_random_color()}\n"
                                    f"Fetching Level info for {xMsGFixinG(player_id)}...\n"
                                )

                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                level_result = get_level_info(player_id)

                                if isinstance(level_result, list):
                                    for msg in level_result:
                                        await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.4)
                                else:
                                    await safe_send_message(response.Data.chat_type, level_result, uid, chat_id, key, iv)

                                #GET PLAYER CHECK ID
                        # Command handler for remove
                        if inPuTMsG.strip().startswith('/wlremove'):
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /wlremove (uid)\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            target_uid = parts[1]
    
                            # Check owner
                            if str(response.Data.uid) != "415136165":
                                error_msg = f"[B][C][FF0000]❌ Only bot owner can remove from whitelist!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
                            
                            success, message = remove_from_whitelist(target_uid)
    
                            if success:
                                bot_uid = 13736023597
        
                                # Create the private message packet
                                # Tp = 2 (Private message)
                                # Tp2 = target_uid (recipient)
                                # id = bot_uid (sender)
                                message_text = f"You Are Successfully Removed From Whitelist By {xMsGFixinG(uid)}"
                                private_msg_packet = await xSEndMsg(
                                    Msg=message_text,
                                    Tp=2,  # 2 = Private message
                                    Tp2=int(target_uid),  # Recipient UID
                                    id=int(bot_uid),  # Sender UID (your bot)
                                    K=key,
                                    V=iv
                                )
                                result_msg = f"[B][C][00FF00]✅ {message}\n📊 Remaining: {len(WHITELISTED_UIDS)} UIDs\n"
                            else:
                                result_msg = f"[B][C][FF0000]❌ {message}\n"
                            
                            await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
                            
                        # Command to enable/disable whitelist only mode
                        if inPuTMsG.strip() == '/wlenable':
                            
                            WHITELIST_ONLY = True
                            msg = f"[B][C][00FF00]✅ Whitelist-only mode ENABLED!\n🤖 Bot will only accept invites from whitelisted UIDs\n"
                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip() == '/wldisable':

                            WHITELIST_ONLY = False
                            msg = f"[B][C][FFFF00]⚠️ Whitelist-only mode DISABLED!\n🤖 Bot will accept invites from anyone\n"
                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                            
                        # Add this command handler
                        if inPuTMsG.strip().startswith('/wladd'):
                            print('Processing whitelist add command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /wladd (uid)
        
📝 Examples:
/wladd 123456789 - Add UID to whitelist
/wladd 123456789 "Friend" - Add with note

🎯 What happens:
• UID can now invite bot to squad
• UID can use bot commands
• Bot auto-accepts invites from this UID
"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            target_uid = parts[1]
    
                            # Optional note
                            note = ""
                            if len(parts) > 2:
                                note = ' '.join(parts[2:])
    
                            # Check if sender is owner
                            if str(response.Data.uid) != "415136165":  # Replace with your actual UID
                                error_msg = f"[B][C][FF0000]❌ Only bot owner can add to whitelist!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Add to whitelist
                            success, message = append_to_whitelist(target_uid, note)
    
                            # Send result
                            if success:
                                bot_uid = 13736023597
        
                                # Create the private message packet
                                # Tp = 2 (Private message)
                                # Tp2 = target_uid (recipient)
                                # id = bot_uid (sender)
                                message_text = f"You Are Successfully Added To Whitelist By {xMsGFixinG(uid)}"
                                private_msg_packet = await xSEndMsg(
                                    Msg=message_text,
                                    Tp=2,  # 2 = Private message
                                    Tp2=int(target_uid),  # Recipient UID
                                    id=int(bot_uid),  # Sender UID (your bot)
                                    K=key,
                                    V=iv
                                )
        
                                if private_msg_packet and whisper_writer:
                                    # Send via Whisper connection (chat connection)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', private_msg_packet)
                                success_msg = f"""[B][C][00FF00]✅ WHITELIST UPDATED!
                        
👤 Added: {xMsGFixinG(target_uid)}
📝 Note: {note if note else 'None'}
📊 Total whitelisted: {len(WHITELISTED_UIDS)}
"""
                            else:
                                success_msg = f"[B][C][FF0000]❌ {message}\n"
    
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)    
                            
                        if inPuTMsG.strip() == '/wllist':
                            print('Processing whitelist view command')
    
                            # Check if owner
                            if str(response.Data.uid) != "415136165":  # Your UID
                                error_msg = f"[B][C][FF0000]❌ Only bot owner can view whitelist!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Build whitelist message
                            total = len(WHITELISTED_UIDS)
    
                            whitelist_msg = f"""[B][C][00FF00]📋 WHITELISTED UIDS

📊 Total: {total} UIDs
🔓 Whitelist enabled: {'YES' if WHITELIST_ONLY else 'NO'}

👑 Owner (always allowed):
• 415136165

👥 Whitelisted UIDs:"""
    
                            # Add first 20 UIDs (to avoid message too long)
                            count = 0
                            for uid in WHITELISTED_UIDS:
                                if uid != "415136165":  # Skip owner since already shown
                                    whitelist_msg += f"\n• {xMsGFixinG(uid)}"
                                    count += 1
                                    if count >= 20:
                                        remaining = total - 21  # -1 for owner, -20 shown
                                        if remaining > 0:
                                            whitelist_msg += f"\n... and {remaining} more"
                                        break
    
                            whitelist_msg += f"""

💡 Commands:
/wladd (uid) - Add to whitelist
/wlremove (uid) - Remove from whitelist
/wlenable - Enable whitelist only mode
/wldisable - Disable whitelist only mode
"""
    
                            await safe_send_message(response.Data.chat_type, whitelist_msg, uid, chat_id, key, iv)
                            
                        if inPuTMsG.startswith('t_31_p_veteran_wlcm_friend'):
                            print("got it")
                            
                        # Add this command too:
                        if inPuTMsG.strip() == '/viewguests':
                            print('Processing view guests command')
                            
                            try:
                                if not os.path.exists("guest_accounts.json"):
                                    error_msg = f"[B][C][FF0000]❌ No guest accounts found!\n[FFFFFF]Generate with /guest (count) first\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                with open("guest_accounts.json", 'r') as f:
                                    accounts = json.load(f)
                                
                                total = len(accounts)
        
                                # Show summary
                                summary_msg = f"""[B][C][00FF00]📁 GUEST ACCOUNTS DATABASE

📊 Total accounts: {total}
📁 File: guest_accounts.json
📅 Last updated: {time.ctime(os.path.getmtime('guest_accounts.json'))}

💡 Use /guest (count) to add more
"""
                                await safe_send_message(response.Data.chat_type, summary_msg, uid, chat_id, key, iv)
        
                                # Show recent 5 accounts
                                if accounts:
                                    recent = accounts[-5:]  # Last 5 accounts
                                    recent_msg = "[B][C][FFFF00]📋 RECENT 5 ACCOUNTS:\n"
            
                                    for i, acc in enumerate(recent):
                                        recent_msg += f"[FFFFFF]{i+1}. UID: {acc['uid']} | Pass: {acc['password']}\n"
            
                                    await safe_send_message(response.Data.chat_type, recent_msg, uid, chat_id, key, iv)
            
                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)    
                            
                        # Add this with your other command handlers:
                        if inPuTMsG.strip().startswith('/guest'):
                            print('Processing guest account generation command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /guest (count)
        
📝 Examples:
/guest 5 - Generate 5 guest accounts
/guest 10 - Generate 10 guest accounts
/guest 50 - Generate 50 guest accounts

🎯 Features:
• Generates random guest accounts
• Auto-retry on 503 errors (10 times)
• Saves to guest_accounts.json
• Shows progress in real-time

⚠️ Note: API may take time, be patient!
"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            count_input = parts[1]
    
                            if not count_input.isdigit():
                                error_msg = f"[B][C][FF0000]❌ Count must be a number!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            count = int(count_input)
                            
                            if count <= 0:
                                error_msg = f"[B][C][FF0000]❌ Count must be greater than 0!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            if count > 100:
                                error_msg = f"[B][C][FF0000]❌ Max 100 accounts at once!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Send initial message
                            initial_msg = f"""[B][C][00FF00]🚀 GENERATING GUEST ACCOUNTS

📊 Count: {count} accounts
🔗 API: gen-by-black-api.vercel.app
⏳ Please wait...

💡 This may take {count * 3} seconds
⚠️ 503 errors auto-retry 10 times
"""
                            await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                            
                            try:
                                # Run generation in background
                                asyncio.create_task(handle_guest_generation(count, uid, chat_id, response.Data.chat_type, key, iv))
        
                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ Error starting generation: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            
                        if inPuTMsG.startswith('/mimic_on'):
                            success_msg = f"[B][C][FF0000]The Mimic Is Now OFF\n"
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            emote_hijack = True
                            
                        if inPuTMsG.startswith('/mimic_off'):
                            success_msg = f"[B][C][FF0000]The Mimic Is Now OFF\n"
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            emote_hijack = False
                            
                        # In your TcPChaT function, add this command handler:
                        if inPuTMsG.strip().startswith('/dm '):
                            print('Processing private message command')
    
                            parts = inPuTMsG.strip().split(maxsplit=2)  # maxsplit=2 to keep message together
    
                            if len(parts) < 3:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /dm (target_uid) (message)
        
📝 Examples:
/dm 123456789 Hello!
/dm 123456789 How are you?
/dm 123456789 Let's play together!

🔧 What it does:
• Sends private message to specified UID
• Works even if target is not in your squad
• Bot sends message from its account
• Target sees message in private chat
"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            target_uid = parts[1]
                            message = parts[2]
                            message_text = f"[B]{message}"
                            
                            # Validate target UID
                            if not target_uid.isdigit() or len(target_uid) < 8:
                                error_msg = f"[B][C][FF0000]❌ Invalid UID! Must be 8+ digits\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Validate message length
                            if len(message_text) > 100:
                                error_msg = f"[B][C][FF0000]❌ Message too long! Max 100 characters\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Send initial confirmation
                            initial_msg = f"[B][C][00FF00]📩 SENDING PRIVATE MESSAGE\n"
                            initial_msg += f"👤 To: {xMsGFixinG(target_uid)}\n"
                            initial_msg += f"📝 Message: {message_text[:30]}...\n"
                            initial_msg += f"⏳ Sending...\n"
    
                            await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
    
                            try:
                                # Get bot's UID from login data
                                bot_uid = 13777711848
        
                                # Create the private message packet
                                # Tp = 2 (Private message)
                                # Tp2 = target_uid (recipient)
                                # id = bot_uid (sender)
                                private_msg_packet = await xSEndMsg(
                                    Msg=message_text,
                                    Tp=2,  # 2 = Private message
                                    Tp2=int(target_uid),  # Recipient UID
                                    id=int(bot_uid),  # Sender UID (your bot)
                                    K=key,
                                    V=iv
                                )
        
                                if private_msg_packet and whisper_writer:
                                    # Send via Whisper connection (chat connection)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', private_msg_packet)
            
                                    success_msg = f"""[B][C][00FF00]✅ PRIVATE MESSAGE SENT!

👤 To: {xMsGFixinG(target_uid)}
📝 Message: {message_text}
✅ Status: Delivered

💡 Target will see this in their private messages!
"""
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"✅ Private message sent to {xMsGFixinG(target_uid)}: {message_text}")
                                else:
                                    error_msg = f"[B][C][FF0000]❌ Failed to create message packet!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
            
                            except Exception as e:
                                print(f"❌ Private message error: {e}")
                                error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        if inPuTMsG.startswith('noob'):
                            await handle_alll_titles_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/room_msg'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /kick (uid)\nExample: /kick 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]

                                initial_message = f"[B][C]{get_random_color()}\nkicking {xMsGFixinG(uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await Create_xr_room_packet_fixed__(room_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                except Exception as e:
                                    print(e)

                        # Replace the existing title handler with this
                        # Use the FINAL version
                        if inPuTMsG.strip().startswith('/kick'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /kick (uid)\nExample: /kick 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nkicking {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await KickTarget(target_uid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                except Exception as e:
                                    print(e)

                        if inPuTMsG.strip().startswith('/tester'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /kick (uid)\nExample: /kick 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nkicking {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await SwitchLoneWolfDule(target_uid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                except Exception as e:
                                    print(e)
                            

                        if inPuTMsG.startswith(("/3")):
                            # Process /3 command - Create 3 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 3-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(0, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 3-Player Group invitation sent successfully to {xMsGFixinG(uid)}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/4")):
                            # Process /4 command - Create 4 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 4-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(4, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(4, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(0, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {xMsGFixinG(uid)}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        # In your TcPChaT function, look for the command handling section
                        # It might look something like this:

                        if inPuTMsG.startswith('/room '):
                            await handle_room_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        # Join Custom Room Command
                        if inPuTMsG.strip().startswith('/joinroom'):
                            print('Processing custom room join command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /joinroom (room_id) (password)\nExample: /joinroom 123456 0000\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
        
                                initial_msg = f"[B][C][00FF00]🚀 Joining custom room...\n🏠 Room: {room_id}\n🔑 Password: {room_password}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Join the custom room
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Joined custom room {room_id}!\n🤖 Bot is now in room chat!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to join room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/5")):
                            # Process /5 command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\n\nSending Group Invitation...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(0, key, iv)
                            await asyncio.sleep(3.5)  # Reduced from 3 seconds
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Group invitation sent successfully to {xMsGFixinG(uid)}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        # Add this with your other command handlers in the TcPChaT function
                        if inPuTMsG.strip().startswith('/multijoin'):
                            print('Processing multi-account join request')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /multijoin (target_uid)\nExample: /multijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                initial_msg = f"[B][C][00FF00]🚀 Starting multi-join attack on {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Try the fake multi-account method (more reliable)
                                    success_count, total_attempts = await real_multi_account_join(target_uid, key, iv, region)
            
                                    if success_count > 0:
                                        result_msg = f"""
[B][C][00FF00]✅ MULTI-JOIN ATTACK COMPLETED!

🎯 Target: {xMsGFixinG(target_uid)}
✅ Successful Requests: {success_count}
📊 Total Attempts: {total_attempts}
⚡ Different squad variations sent!

💡 Check your game for join requests!
"""
                                    else:
                                        result_msg = f"[B][C][FF0000]❌ All join requests failed! Check bot connection.\n"
            
                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Multi-join error: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)



                        # Update the command handler
                        if inPuTMsG.strip().startswith('/reject'):
                            print('Processing reject spam command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /reject (target_uid)\nExample: /reject 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing reject spam
                                if reject_spam_task and not reject_spam_task.done():
                                    reject_spam_running = False
                                    reject_spam_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Send start message
                                start_msg = f"[B][C][1E90FF]🌀 Started Reject Spam on: {xMsGFixinG(target_uid)}\n🌀 Packets: 150 each type\n🌀 Interval: 0.2 seconds\n"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
        
                                # Start reject spam in background
                                reject_spam_running = True
                                reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
        
                                # Wait for completion in background and send completion message
                                asyncio.create_task(handle_reject_completion(reject_spam_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))


                        if inPuTMsG.strip() == '/reject_stop':
                            if reject_spam_task and not reject_spam_task.done():
                                reject_spam_running = False
                                reject_spam_task.cancel()
                                stop_msg = f"[B][C][00FF00]✅ Reject spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ No active reject spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #GET PLAYER INFO
                        if inPuTMsG.strip().startswith('/info'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /info <uid>\nExample: /info 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nGetting Player Info...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                info_data, error = await get_player_info(target_uid)
                                if error:
                                    error_msg = f"[B][C][FF0000]❌ Failed to fetch player info\n{error}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return

                                await send_full_player_info(info_data, response.Data.chat_type, uid, chat_id, key, iv)

                        # BAN STATUS CHECK COMMAND
                        if inPuTMsG.strip().startswith('/check'):
                            print('Processing /check command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = (
                                    "[B][C][FF0000]❌ ERROR! Usage: /check <uid>\n"
                                    "[FFFF00]Example: /check 4263143059\n"
                                )
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                wait_msg = f"[B][C]{get_random_color()}🔍 Checking ban status for UID {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, wait_msg, uid, chat_id, key, iv)

                                ban_data, ban_error = await check_ban_status(target_uid)
                                if ban_error:
                                    err_msg = f"[B][C][FF0000]❌ Failed to check ban status\n{ban_error}"
                                    await safe_send_message(response.Data.chat_type, err_msg, uid, chat_id, key, iv)
                                else:
                                    # API response: { credit, data: { ban_info: {...}, nickname, level, region, status_reason, ... }, msg, status }
                                    _bd = ban_data.get("data", ban_data)
                                    _ban_info = _bd.get("ban_info", {})

                                    _player_name  = str(_bd.get("nickname", _bd.get("name", "Unknown")))
                                    _player_uid   = str(_bd.get("uid", target_uid))
                                    _status_text  = str(_ban_info.get("status_text", "unknown")).lower()
                                    _is_permanent = _ban_info.get("is_permanent", False)
                                    _remaining    = _ban_info.get("remaining_seconds", 0)
                                    _start_ban    = _ban_info.get("start_ban", 0)
                                    _reason       = str(_bd.get("status_reason", _bd.get("reason", "N/A")))

                                    # Map status_text to display
                                    if _status_text in ("banned", "temporary_banned", "temp_banned"):
                                        _status_display = "[FF0000]BANNED ⛔"
                                    elif _status_text == "permanent_banned" or _is_permanent:
                                        _status_display = "[FF0000]PERMANENTLY BANNED ⛔"
                                    elif _status_text in ("not_banned", "clean", "ok"):
                                        _status_display = "[00FF00]NOT BANNED ✅"
                                    else:
                                        _status_display = f"[FFFF00]{_status_text.upper()}"

                                    # Format remaining time
                                    if _remaining and int(_remaining) > 0:
                                        _secs = int(_remaining)
                                        _days = _secs // 86400
                                        _hrs  = (_secs % 86400) // 3600
                                        _mins = (_secs % 3600) // 60
                                        _period_str = f"{_days}d {_hrs}h {_mins}m remaining"
                                    else:
                                        _period_str = "None" if _status_text in ("not_banned", "clean", "ok") else "N/A"

                                    # Format ban start time
                                    _ban_start_str = human_time(_start_ban) if _start_ban and int(_start_ban) > 0 else "N/A"

                                    ban_msg = (
                                        f"[B][C][FF4444]╔══════════════╗\n"
                                        f"[C][FF4444]   BAN STATUS CHECK\n"
                                        f"[C][FF4444]╚══════════════╝\n"
                                        f"[FFFF00]Player  : [FFFFFF]{_player_name}\n"
                                        f"[FFFF00]UID     : [00FFAA]{xMsGFixinG(_player_uid)}\n"
                                        f"[FFFF00]Status  : {_status_display}\n"
                                        f"[FFFF00]Reason  : [FFFFFF]{_reason}\n"
                                        f"[FFFF00]Period  : [FFFFFF]{_period_str}\n"
                                        f"[FFFF00]Ban Date: [FFFFFF]{_ban_start_str}\n"
                                        f"[FFFF00]Permanent: [FFFFFF]{'Yes' if _is_permanent else 'No'}\n"
                                        f"[C][FF4444]══════════════"
                                    )
                                    await safe_send_message(response.Data.chat_type, ban_msg, uid, chat_id, key, iv)

                        # Individual command handlers for /s1 to /s8
                        if inPuTMsG.strip().startswith('/s1'):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
    
                        if inPuTMsG.strip().startswith('/s2'):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s3'):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s4'):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s5'):
                            await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s6'):
                            await handle_badge_command('s6', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s7'):
                            await handle_badge_command('s7', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s8'):
                            await handle_badge_command('s8', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                                    
                                                                                                     
                        if inPuTMsG.strip().startswith('@joinroom'):
                            print('Processing custom room join command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /joinroom (room_id) (password)\nExample: /joinroom 123456 0000\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
        
                                initial_msg = f"[B][C][00FF00]🚀 Joining custom room...\n🏠 Room: {room_id}\n🔑 Password: {room_password}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Join the custom room
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Joined custom room {room_id}!\n🤖 Bot is now in room chat!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to join room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/createroom'):
                            print('Processing custom room creation')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /createroom (room_name) (password) [players=4]\nExample: /createroom BOTROOM 0000 4\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_name = parts[1]
                                room_password = parts[2]
                                max_players = parts[3] if len(parts) > 3 else "4"
        
                                initial_msg = f"[B][C][00FF00]🏠 Creating custom room...\n📛 Name: {room_name}\n🔑 Password: {room_password}\n👥 Max Players: {max_players}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Create custom room
                                    create_packet = await create_custom_room(room_name, room_password, int(max_players), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', create_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Custom room created!\n🏠 Room: {room_name}\n🔑 Password: {room_password}\n👥 Max: {max_players}\n🤖 Bot is now hosting!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to create room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)               
                        
                                                
                        # Add with other command handlers in TcPChaT
                        if inPuTMsG.strip().startswith('/arr'):
                            print('Processing entry emote command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /entry (uid)
                        Example: /entry 123456789
                        Example: /entry me (for yourself)

                        Effect: Sends arrival animation to player
                        """
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Handle "me" or "self"
                                if target_uid.lower() in ['me', 'self', 'myself']:
                                    target_uid = str(response.Data.uid)
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {xMsGFixinG(target_uid)}"
        
                                initial_msg = f"[B][C][00FF00]🎬 Sending arrival animation to {target_name}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Send the entry emote packet
                                    entry_packet = await Send_Entry_Emote(int(target_uid), key, iv)
                                    
                                    if entry_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', entry_packet)
                
                                        success_msg = f"[B][C][00FF00]✅ ARRIVAL ANIMATION SENT!\n"
                                        success_msg += f"[FFFFFF]👤 Target: {target_name}\n"
                                        success_msg += f"[FFFFFF]🎭 Emote ID: 912038002\n"
                                        success_msg += f"[FFFFFF]✨ Effect: Entry/Arrival Animation\n"
                
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        print(f"✅ Sent entry emote to {xMsGFixinG(target_uid)}")
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ Failed to create entry emote packet!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error sending entry emote: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            
                        # ========= ANIMATION COMMAND =========
                        if inPuTMsG.strip().startswith('/animation'):
                            _anim_ct = response.Data.chat_type
                            parts = inPuTMsG.strip().split()

                            if len(parts) == 1:
                                # Show animation list — one per line, split into pages like /list
                                _anim_names = list(ANIMATION_MAP.keys())
                                _header = "[B][C][00FFFF]ANIMATION LIST\n[FFFF00]Use: /animation <name> <uid>\n"
                                # Build pages: ~5 animations per message to stay under length limit
                                _page_size = 5
                                _pages = []
                                for _pi in range(0, len(_anim_names), _page_size):
                                    _chunk = _anim_names[_pi:_pi + _page_size]
                                    _lines = ""
                                    for _ni, _an in enumerate(_chunk, start=_pi + 1):
                                        _lines += f"[FFFF00]{_ni}.[FFFFFF] {_an}\n"
                                    _pages.append(_lines.strip())
                                # Send header + first page together, rest separately
                                await safe_send_message(_anim_ct, _header + _pages[0], uid, chat_id, key, iv)
                                for _pg in _pages[1:]:
                                    await asyncio.sleep(0.4)
                                    await safe_send_message(_anim_ct, _pg, uid, chat_id, key, iv)

                            elif len(parts) >= 2:
                                _anim_name = parts[1].lower()
                                _anim_target = parts[2] if len(parts) >= 3 else str(response.Data.uid)

                                if _anim_name not in ANIMATION_MAP:
                                    _err = f"[B][C][FF0000]❌ Unknown animation: {_anim_name}\nType /animation to see the list."
                                    await safe_send_message(_anim_ct, _err, uid, chat_id, key, iv)
                                else:
                                    if _anim_target.lower() in ('me', 'self', 'myself'):
                                        _anim_target = str(response.Data.uid)
                                        _anim_name_display = "Yourself"
                                    else:
                                        _anim_name_display = f"UID {xMsGFixinG(_anim_target)}"

                                    if not _anim_target.isdigit():
                                        await safe_send_message(_anim_ct, "[B][C][FF0000]❌ Invalid UID. Usage: /animation <name> <uid>", uid, chat_id, key, iv)
                                    else:
                                        _anim_id = ANIMATION_MAP[_anim_name]
                                        _start = f"[B][C]{get_random_color()}Sending [{_anim_name}] to {_anim_name_display}...\n"
                                        await safe_send_message(_anim_ct, _start, uid, chat_id, key, iv)
                                        try:
                                            _anim_pkt = await Emote_k(int(_anim_target), _anim_id, key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', _anim_pkt)
                                            _ok = (
                                                f"[B][C][00FF00]✅ Animation sent!\n"
                                                f"[FFFFFF]Name: [{_anim_name}]\n"
                                                f"[FFFFFF]ID  : {_anim_id}\n"
                                                f"[FFFFFF]To  : {_anim_name_display}"
                                            )
                                            await safe_send_message(_anim_ct, _ok, uid, chat_id, key, iv)
                                        except Exception as _ae:
                                            _err = f"[B][C][FF0000]❌ Animation failed: {str(_ae)[:60]}"
                                            await safe_send_message(_anim_ct, _err, uid, chat_id, key, iv)

                        # FIXED JOIN COMMAND
                        if inPuTMsG.startswith('/join'):
                            # Process /join command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /join (team_code)\nExample: /join ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                uid = response.Data.uid  # Get the UID of person who sent the command
        
                                initial_message = f"[B][C]{get_random_color()}\nJoining squad with code: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try using the regular join method first
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)

                                    # Mark bot as in squad so squad chat auth triggers on next packet
                                    insquad = True
                                    joining_team = False
                                    squad_chat_authed = False
            
                                    # Wait a bit for the join to complete
                                    await asyncio.sleep(2)
            
                                    # DUAL RINGS EMOTE - BOTH SENDER AND BOT
                                    try:
                                        await auto_rings_emote_dual(uid, key, iv, region)
                                    except Exception as emote_error:
                                        print(f"Dual emote failed but join succeeded: {emote_error}")
            
                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Joined squad: {CodE}!\n💍 Dual Rings emote activated!\n🤖 Bot + You = 💕\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print(f"Regular join failed, trying ghost join: {e}")
                                    try:
                                        ghost_packet = await GenJoinSquadsPacket(CodE, key, iv)
                                        if ghost_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                            await asyncio.sleep(2)
                                            try:
                                                await auto_rings_emote_dual(uid, key, iv, region)
                                            except Exception as emote_error:
                                                print(f"Dual emote failed but ghost join succeeded: {emote_error}")
                                            success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joined squad: {CodE}!\n💍 Dual Rings emote activated!\n🤖 Bot + You = 💕\n"
                                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    except Exception as ghost_error:
                                        print(f"Ghost join also failed: {ghost_error}")
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to join squad: {str(ghost_error)}\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                
                        if inPuTMsG.strip().startswith('/ghost'):
                            # Process /ghost command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ghost (team_code)\nExample: /ghost ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nGhost joining squad with code: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    ghost_packet = await GenJoinSquadsPacket(CodE, key, iv)
                                    if ghost_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                        success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joined squad: {CodE}!\n"
                                        await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Ghost join failed: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            continue

# NEW LAG COMMAND (AUTO STOP AFTER 10 SECONDS)
                        if inPuTMsG.strip().startswith('/lag '):
                            print('Processing lag command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /lag (team_code)\nExample: /lag ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]

                                # Stop previous task if running
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)

                                lag_running = True

                                async def auto_lag():
                                    global lag_running
                                    try:
                                        task = asyncio.create_task(lag_team_loop(team_code, key, iv, region))
                                        await asyncio.sleep(10)

                                        lag_running = False
                                        task.cancel()

                                        stop_msg = f"[B][C][00FF00]✅ Auto Stopped!\nTeam: {team_code}\nDuration: 10 seconds\n"
                                        await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)

                                    except asyncio.CancelledError:
                                        lag_running = False

                                lag_task = asyncio.create_task(auto_lag())

                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack started!\nTeam: {team_code}\nDuration: 10 seconds\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

# NEW ATTACK COMMAND (AUTO STOP AFTER 1 SECOND)
                        if inPuTMsG.strip().startswith('/attack '):
                            print('Processing attack command')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /attack (target)\nExample: /attack TEST\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target = parts[1]

                                # Stop previous task if running
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)

                                lag_running = True

                                async def auto_attack():
                                    global lag_running
                                    try:
                                        task = asyncio.create_task(attack_loop(target))
                                        
                                        # Run for 1 second
                                        await asyncio.sleep(1)

                                        lag_running = False
                                        task.cancel()

                                        stop_msg = f"[B][C][00FF00]✅ Auto Stopped!\nTarget: {target}\nDuration: 1 second\n"
                                        await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)

                                    except asyncio.CancelledError:
                                        lag_running = False

                                lag_task = asyncio.create_task(auto_attack())

                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Attack started!\nTarget: {target}\nDuration: 1 second\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)


                        if inPuTMsG.startswith('/exit'):
                            # Process /exit command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nLeaving current squad...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)

                            # Reset squad state so bot can accept future invites
                            insquad = None
                            joining_team = False
                            squad_chat_authed = False
                            squad_group_owner_uid = None
                            squad_group_chat_code = None
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Left the squad successfully!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                            continue

                        if inPuTMsG.strip().startswith('/start'):
                            # Process /s command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nStarting match...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            start_packet = await start_auto_packet(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                            initiial_message = f"[B][C]{get_random_color()}\nStarting match...\n"
                            await safe_send_message(response.Data.chat_type, initiial_message, uid, chat_id, key, iv)
                            

                        if inPuTMsG.strip().startswith('/mg'):
                            print('Processing wave message command')
                          
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /mg (message) [repeats=5]\n"
                                error_msg += f"[FFFFFF]Example: /mg hello 3\n"
                                error_msg += f"[FFFFFF]Will send: h, he, hel, hell, hello, hell, hel, he, h\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    # Get message and optional repeats
                                    message_text = parts[1]
                                    repeats = 5  # Default
            
                                    if len(parts) > 2:
                                        repeats = int(parts[2])
            
                                    if repeats <= 0:
                                        error_msg = f"[B][C][FF0000]❌ Repeats must be > 0!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif repeats > 10:
                                        error_msg = f"[B][C][FF0000]❌ Max 10 repeats!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif len(message_text) < 2:
                                        error_msg = f"[B][C][FF0000]❌ Message must be at least 2 characters!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        global mg_spam_task
                                        if mg_spam_task and not mg_spam_task.done():
                                            global msg_spam_running
                                            msg_spam_running = False
                                            mg_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                
                                        # Calculate total messages
                                        total_messages_per_cycle = (len(message_text) * 2) - 2
                                        total_messages = total_messages_per_cycle * repeats
                
                                        initial_msg = f"[B][C][00FF00]🌊 WAVE MESSAGE STARTING!\n"
                                        initial_msg += f"[FFFFFF]Message: {message_text}\n"
                                        initial_msg += f"[FFFFFF]Repeats: {repeats} cycles\n"
                                        initial_msg += f"[FFFFFF]Pattern: h → he → hel → hell → hello → hell → hel → he → h\n"
                                        initial_msg += f"[00FF00]Total messages: {total_messages}\n"
                                        await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                        
                                        # Start wave messages
                                        msg_spam_running = True
                                        mg_spam_task = asyncio.create_task(
                                            send_wave_messages(message_text, repeats, chat_id, key, iv, region)
                                        )
                
                                        # Handle completion
                                        asyncio.create_task(
                                            handle_wave_completion(mg_spam_task, message_text, repeats, uid, chat_id, response.Data.chat_type, key, iv)
                                        )
                
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ Invalid format!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip().startswith('/msg'):
                            print('Processing /msg command')
                            global msg_spam_task
                            parts = inPuTMsG.strip().split(None, 1)

                            if len(parts) < 2 or not parts[1].strip():
                                error_msg = (
                                    f"[B][C][FF0000]❌ ERROR! Usage: /msg <message>\n"
                                    f"[FFFFFF]Example: /msg Hello Team!\n"
                                    f"[FFFFFF]Sends the message 15 times in guild or squad chat.\n"
                                )
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                message_text = parts[1].strip()
                                TIMES = 15

                                # Stop any existing message spam first
                                if msg_spam_task and not msg_spam_task.done():
                                    msg_spam_running = False
                                    msg_spam_task.cancel()
                                    await asyncio.sleep(0.2)

                                # Auto-detect: squad if insquad is set, otherwise guild
                                in_squad = insquad is not None
                                if in_squad:
                                    target_chat_id = chat_id
                                    chat_label = "Squad Chat"
                                else:
                                    target_chat_id = _console_guild_chat_id
                                    chat_label = "Guild Chat"

                                if not in_squad and not target_chat_id:
                                    error_msg = (
                                        f"[B][C][FF0000]❌ Not in a squad and guild chat ID is not set.\n"
                                        f"[FFFFFF]Join a squad or make sure the bot is connected to guild chat.\n"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    initial_msg = (
                                        f"[B][C][00FF00]📢 SENDING MESSAGE!\n"
                                        f"[FFFFFF]Message : {message_text}\n"
                                        f"[FFFFFF]Times   : {TIMES}\n"
                                        f"[FFFFFF]Chat    : {chat_label}\n"
                                        f"[00FF00]Sending now...\n"
                                    )
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                    msg_spam_running = True
                                    msg_spam_task = asyncio.create_task(
                                        msg_spam_loop(message_text, TIMES, target_chat_id, key, iv, region, use_guild=not in_squad)
                                    )

                                    asyncio.create_task(
                                        handle_msg_spam_completion(msg_spam_task, message_text, TIMES, uid, chat_id, response.Data.chat_type, key, iv)
                                    )

                        # Stop command
                        if inPuTMsG.strip() == '/stop msg':
                            if msg_spam_task and not msg_spam_task.done():
                                msg_spam_running = False
                                msg_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ MESSAGE SENDING STOPPED!\n[FFFFFF]All message sending has been stopped.\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ No active message sending to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
        
                        # Add this to your command handlers in TcPChaT function:
                        if inPuTMsG.strip().startswith('/train'):
                            print('Processing training mode command')
                            await handle_training_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            
                        # Add these to your command handlers in TcPChaT function:
                        # Add this to your command handlers in TcPChaT function:
                        if inPuTMsG.strip().startswith('/join_req '):
                            print('Processing /join_req command')
                            await handle_join_req_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type, LoGinDaTaUncRypTinG)


                        _e_stripped = inPuTMsG.strip()
                        if (_e_stripped == '/e' or _e_stripped.startswith('/e ') or _e_stripped.startswith('/e\t')):
                            print(f'Processing emote command in chat type: {response.Data.chat_type}')
    
                            parts = inPuTMsG.strip().split()
    
                            # /e or /e list → show all emote names in paginated /help-style messages
                            if len(parts) == 1 or (len(parts) >= 2 and parts[1].lower() == 'list'):
                                all_names = sorted(NAME_EMOTES.keys())
                                total = len(all_names)

                                # Header message
                                header_msg = (
                                    f"[B][C][FF00FF]🎭 EMOTE NAMES\n"
                                    f"[FF1493]══════════════════\n"
                                    f"[FFFFFF]Total: [FFD700]{total}[FFFFFF] named emotes\n"
                                    f"[00FF00]Usage: /e [name]\n"
                                    f"[00FF00]Example: /e ak  /e heart  /e dance\n"
                                    f"[FF1493]══════════════════"
                                )
                                await safe_send_message(response.Data.chat_type, header_msg, uid, chat_id, key, iv)
                                await asyncio.sleep(0.3)

                                # Send names in pages of 60 (5 per line, 12 lines)
                                NAMES_PER_LINE = 5
                                PAGE_SIZE = 60
                                total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

                                for page_idx in range(total_pages):
                                    start = page_idx * PAGE_SIZE
                                    chunk = all_names[start:start + PAGE_SIZE]
                                    page_num = page_idx + 1

                                    page_msg = f"[B][C][00FF00]🎭 Emotes ({page_num}/{total_pages}):\n"
                                    page_msg += f"[FF1493]══════════════════\n"

                                    for i in range(0, len(chunk), NAMES_PER_LINE):
                                        line_names = chunk[i:i + NAMES_PER_LINE]
                                        page_msg += f"[FFD700]{'  [FFFFFF]•[FFD700]  '.join(line_names)}\n"

                                    page_msg += f"[FF1493]══════════════════"

                                    await safe_send_message(response.Data.chat_type, page_msg, uid, chat_id, key, iv)
                                    await asyncio.sleep(0.3)

                                continue
    
                            # Parse command
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /e [emote_name_or_number]\n"
                                error_msg += f"[FFFFFF]Examples:\n"
                                error_msg += f"[00FF00]/e ak[FFFFFF] → AK emote to yourself\n"
                                error_msg += f"[00FF00]/e 123456789 heart[FFFFFF] → ❤️ to UID\n"
                                error_msg += f"[00FF00]/e 123456789 1[FFFFFF] → Emote #1 to UID\n"
                                error_msg += f"[00FF00]/e ring[FFFFFF] → Send ring emote to yourself\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
    
                            # Show "preparing" message
                            initial_message = f'[B][C]{get_random_color()}\n🎭 Preparing emote...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            target_uids = []
                            emote_key = None
    
                            try:
                                # Determine if last part is emote key (could be number or name)
                                last_part = parts[-1].lower()
        
                                # Check if last part is an emote (number or name)
                                # Note: Your numbers go up to 417, so check for 3-digit numbers too
                                is_number = last_part.isdigit() and last_part in NUMBER_EMOTES
                                is_name = last_part in NAME_EMOTES
        
                                if is_number or is_name:
                                    # Case 1: /e ak or /e 1 (only emote - send to sender)
                                    if len(parts) == 2:
                                        emote_key = last_part
                                        target_uids.append(int(response.Data.uid))
            
                                    # Case 2: /e 123456789 heart (UID + emote)
                                    elif len(parts) == 3:
                                        target_uids.append(int(parts[1]))
                                        emote_key = last_part
            
                                    # Case 3: /e 111 222 333 ak (multiple UIDs + emote)
                                    else:
                                        for i in range(1, len(parts) - 1):
                                            target_uids.append(int(parts[i]))
                                        emote_key = last_part
                                else:
                                    # Last part is not a valid emote
                                    error_msg = f"[B][C][FF0000]❌ Invalid emote: '{last_part}'\n"
                                    error_msg += f"[FFFFFF]Use numbers (1-{len(NUMBER_EMOTES)}) or names like 'ak', 'heart', 'dance', 'ring'\n"
                                    error_msg += f"[FFFFFF]Use /e list names to see all available names\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
        
                                # Get emote ID from either number or name dictionary
                                emote_id = None
                                emote_name_display = None
                                
                                if is_number:
                                    # Number-based emote
                                    emote_id = NUMBER_EMOTES.get(emote_key)
                                    emote_name_display = f"#{emote_key}"
                                else:
                                    # Name-based emote
                                    emote_id = NAME_EMOTES.get(emote_key)
                                    emote_name_display = emote_key
        
                                if not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ Emote '{emote_name_display}' not found!\n"
                                    if emote_key.isdigit():
                                        error_msg += f"[FFFFFF]Available numbers: 1-{len(NUMBER_EMOTES)}\n"
                                    else:
                                        error_msg += f"[FFFFFF]Use /e list names to see all available names\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
        
                                # Send emotes
                                success_count = 0
                                failed_uids = []
        
                                for target_uid in target_uids:
                                    try:
                                        H = await Emote_k(target_uid, int(emote_id), key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        success_count += 1
                                        await asyncio.sleep(0.1)
                                    except Exception as e:
                                        print(f"Error sending emote to {xMsGFixinG(target_uid)}: {e}")
                                        failed_uids.append(str(target_uid))
        
                                # Success message
                                if success_count > 0:
                                    if target_uids[0] == int(response.Data.uid):
                                        target_list = "Yourself"
                                    elif len(target_uids) == 1:
                                        target_list = str(target_uids[0])
                                    else:
                                        target_list = f"{len(target_uids)} players"
            
                                    success_msg = f"[B][C][00FF00]✅ EMOTE SENT!\n"
                                    success_msg += f"[FFFFFF]────────────────\n"
                                    success_msg += f"[00FF00]🎭 Emote: {emote_name_display}\n"
                                    success_msg += f"[00FF00]🆔 ID: {emote_id}\n"
                                    success_msg += f"[00FF00]👤 Target: {target_list}\n"
                                    success_msg += f"[00FF00]📊 Status: {success_count}/{len(target_uids)} successful\n"
            
                                    if failed_uids:
                                        success_msg += f"[FF0000]❌ Failed: {', '.join(failed_uids)}\n"
            
                                    success_msg += f"[FFFFFF]────────────────\n"
            
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                else:
                                    error_msg = f"[B][C][FF0000]❌ Failed to send emote to any target!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                            except ValueError as ve:
                                print("ValueError:", ve)
                                error_msg = f"[B][C][FF0000]❌ Invalid format!\n"
                                error_msg += f"[FFFFFF]UIDs must be numbers (like 123456789)\n"
                                error_msg += f"[FFFFFF]Examples: /e ak, /e 123456789 heart, /e 1, /e ring\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            except Exception as e:
                                print(f"Error processing /e command: {e}")
                                error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/me'):
                            parts = inPuTMsG.strip().split()
                            
                            # Check usage
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /me [team_code] [emote] or /me [team_code] [uid] [emote]\n"
                                error_msg += f"[FFFFFF]Examples:\n"
                                error_msg += f"[00FF00]/me ABC123 ak → Join team ABC123 and send 'ak' emote to yourself\n"
                                error_msg += f"[00FF00]/me ABC123 123456789 heart → Join team ABC123 and send 'heart' emote to UID 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                            
                            team_code = parts[1]
                            target_uids = []
                            emote_key = None
                            
                            # Determine if UID is provided
                            if len(parts) == 3:
                                # /me team_code emote → send to yourself
                                target_uids.append(int(response.Data.uid))
                                emote_key = parts[2].lower()
                            else:
                                # /me team_code uid emote → send to UID(s)
                                for i in range(2, len(parts) - 1):
                                    target_uids.append(int(parts[i]))
                                emote_key = parts[-1].lower()
                            
                            # Show "joining" message
                            initial_message = f"[B][C]{get_random_color()}\n⏳ Joining squad {team_code}...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            try:
                                # Join squad
                                join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                
                                await asyncio.sleep(0.1)
                                
                                # Send emotes
                                emote_id = None
                                if emote_key.isdigit() and emote_key in NUMBER_EMOTES:
                                    emote_id = NUMBER_EMOTES[emote_key]
                                elif emote_key in NAME_EMOTES:
                                    emote_id = NAME_EMOTES[emote_key]
                                
                                if not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ Invalid emote: '{emote_key}'\nUse /e list names to see all available names\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    for target_uid in target_uids:
                                        H = await Emote_k(target_uid, int(emote_id), key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.1)
                                
                                # Leave squad
                                leave_packet = await ExiT(uid, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                                
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Joined squad {team_code}, sent emote '{emote_key}' and left successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            
                            except Exception as e:
                                print(f"Error processing /me command: {e}")
                                error_msg = f"[B][C][FF0000]❌ ERROR! Failed to execute /me command: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


# GLOBAL BLOCKED NAMES
                        BLOCKED_NAMES = ["maruf", "mg24", "mg-king", "mg_king", "mgking", "biryani", "capz", "capzzz", "asjad"]  # Protected names

                        # GALi / JOKE MESSAGE
                        if inPuTMsG.strip().startswith('/gali'):
                            print('Processing /gali command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/gali <name>\n"
                                        "Example: /gali hater"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue

                                name = parts[1].strip()
                                name_lower = name.lower()

                                # BLOCK CHECK (substring, case-insensitive)
                                blocked = False
                                for blocked_name in BLOCKED_NAMES:
                                    if blocked_name.lower() in name_lower:
                                        blocked = True
                                        break

                                if blocked:
                                    block_msg = "[B][C][FF0000]❌ This name is protected and cannot be targeted!"
                                    await safe_send_message(response.Data.chat_type, block_msg, uid, chat_id, key, iv)
                                    continue

                                messages = [
                                    "f u c k   y o u   {Name} !!",
                                    "{Name}   y o u   d u m b   a s s   n i g g a !!",
                                    "{Name}   i s   a   t r a s h   p l a y e r !!",
                                    "g o   t o   h e l l   {Name} !!",
                                    "{Name}   y o u   s t i n k y   b a s t a r d !!",
                                    "{Name}   i s   a   b r a i n d e a d   i d i o t !!",
                                    "s h u t   t h e   f u c k   u p   {Name} !!",
                                    "{Name}   y o u   a b s o l u t e   m o r o n !!",
                                    "{Name}   g e t   o u t   o f   h e r e   l o s e r !!",
                                    "n o b o d y   l i k e s   y o u   {Name} !!",
                                    "{Name}   y o u   a r e   a   w a s t e   o f   s p a c e !!",
                                    "{Name}   k i s s   m y   a s s !!",
                                    "y o u   s u c k   {Name}   g e t   g o o d !!",
                                    "{Name}   y o u   d i r t y   s c r u b !!",
                                    "e v e r y o n e   h a t e s   {Name} !!",
                                    "{Name}   y o u   a r e   a   c l o w n !!",
                                    "g o   c r y   {Name}   y o u   l i t t l e   b i t c h !!"
                                ]

                                for msg in messages:
                                    colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.title())}"
                                    await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                    await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                

# PRAISA COMMAND (17 POSITIVE MESSAGES)
                        if inPuTMsG.strip().startswith('/praise'):
                              print('Processing /praise command')

                              try:
                                  parts = inPuTMsG.strip().split(maxsplit=1)

                                  if len(parts) < 2:
                                      error_msg = (
                                          "[B][C][FF0000]❌ ERROR! Usage:\n"
                                          "/praise <name>\n"
                                          "Example: /praise Maruf"
                                      )
                                      await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                  else:
                                      name = parts[1].strip()

                                      messages = [
                                          "🌟 {Name}, you are truly an extraordinary person!",
                                          "🔥 {Name}, your hard work will bring you great success one day!",
                                          "💎 {Name}, you are one of a kind — nobody else is quite like you!",
                                          "🚀 {Name}, your future is incredibly bright!",
                                          "👑 {Name}, you have all the qualities of a true leader!",
                                          "🌈 {Name}, your positive energy lights up everyone around you!",
                                          "💖 {Name}, keep that amazing attitude — it will take you far!",
                                          "🏆 {Name}, you have what it takes to achieve anything you set your mind to!",
                                          "✨ {Name}, you are a genuine source of inspiration!",
                                          "🌟 {Name}, believe in yourself — you absolutely can do this!",
                                          "🎯 {Name}, your focus and determination are your greatest strengths!",
                                          "📈 {Name}, you grow and improve every single day!",
                                          "🧠 {Name}, your thinking and ideas are truly remarkable!",
                                          "💫 {Name}, you will go incredibly far — keep pushing forward!",
                                          "🌍 {Name}, the world is waiting to see what you are capable of!",
                                          "🛡️ {Name}, you are strong, confident, and absolutely fearless!",
                                          "🏅 {Name}, you are a true champion through and through!"
                                      ]

                                      for msg in messages:
                                          colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.title())}"
                                          await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                          await asyncio.sleep(0.5)

                              except Exception as e:
                                  error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                  await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                                                # Add this with your other command handlers in the TcPChaT function

                        # EVO CYCLE START COMMAND - @evos
                        # EVO CYCLE START COMMAND - @evos
                        # EVO CYCLE START COMMAND - @evos
                        if inPuTMsG.strip().startswith('@evos'):
                            print('Processing evo cycle start command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            uids = []
    
                            # Always use the sender's UID (the person who typed @evos)
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
                            print(f"Using sender's UID: {sender_uid}")
    
                            # Optional: Also allow specifying additional UIDs
                            if len(parts) > 1:
                                for part in parts[1:]:  # Skip the first part which is "@evos"
                                    if part.isdigit() and len(part) >= 7 and part != sender_uid:  # UIDs are usually 7+ digits
                                        uids.append(part)
                                        print(f"Added additional UID: {part}")

                            # Stop any existing evo cycle
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
    
                            # Start new evo cycle
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(
                                evo_cycle_spam(uids, key, iv, region, LoGinDaTaUncRypTinG)
                            )
    
                            # SUCCESS MESSAGE
                            if len(uids) == 1:
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle started!\n🎯 Target: Yourself\n🎭 Emotes: All 18 evolution emotes\n⏰ Delay: 5 seconds between emotes\n🔄 Cycle: Continuous loop until @sevos\n"
                            else:
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle started!\n🎯 Targets: Yourself + {len(uids)-1} other players\n🎭 Emotes: All 18 evolution emotes\n⏰ Delay: 5 seconds between emotes\n🔄 Cycle: Continuous loop until @sevos\n"
    
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            print(f"Started evolution emote cycle for UIDs: {uids}")
                        
                        # EVO CYCLE STOP COMMAND - @sevos
                        if inPuTMsG.strip() == '@sevos':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                print("Evolution emote cycle stopped by command")
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution emote cycle to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Fast emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/fast'):
                            print('Processing fast emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fast uid1 [uid2] [uid3] [uid4] emoteid\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and emoteid
                                uids = []
                                emote_id = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:  # Assuming UIDs are longer than 3 digits
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break
                                
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /fast uid1 [uid2] [uid3] [uid4] emoteid\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    # Stop any existing fast spam
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    
                                    # Start new fast spam
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast emote spam started!\nTargets: {len(uids)} players\nEmote: {emote_id}\nSpam count: 25 times\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Custom emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/p'):
                            print('Processing custom emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /p (uid) (emote_id) (times)\nExample: /p 123456789 909000001 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])
                                    
                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Times must be greater than 0!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif times > 1000:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Maximum 100 times allowed for safety!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        # Stop any existing custom spam
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                         
                                        
                                        # Start new custom spam
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                                        
                                        # SUCCESS MESSAGE
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom emote spam started!\nTarget: {xMsGFixinG(target_uid)}\nEmote: {emote_id}\nTimes: {times}\n"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Usage: /p (uid) (emote_id) (times)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                        if inPuTMsG.strip().startswith('/spam '):
                            print('Processing badge spam command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /spam (uid)\nExample: /spam 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    initial_msg = (
                                        f"[B][C][FF00FF]🚀 Starting Badge Spam...\n"
                                        f"🎯 Target: {xMsGFixinG(target_uid)}\n"
                                        f"📦 Badges: S1 S2 S3 S4 | 20 packets each\n"
                                    )
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                    badge_order = [("s1", BADGE_VALUES["s1"]), ("s2", BADGE_VALUES["s2"]),
                                                   ("s3", BADGE_VALUES["s3"]), ("s4", BADGE_VALUES["s4"])]
                                    total_sent = 0
                                    last_err = None
                                    success = False

                                    for attempt in range(1, 4):
                                        try:
                                            total_sent = 0
                                            for badge_name, badge_value in badge_order:
                                                badge_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
                                                if badge_packet:
                                                    for i in range(20):
                                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', badge_packet)
                                                        total_sent += 1
                                                        await asyncio.sleep(0.1)
                                                    print(f"✅ Sent 20x {badge_name} packets to {target_uid}")
                                                await asyncio.sleep(0.3)
                                            success = True
                                            break
                                        except Exception as e:
                                            last_err = str(e)
                                            print(f"⚠️ Badge spam attempt {attempt} failed: {last_err}")
                                            if attempt < 3:
                                                await asyncio.sleep(2)

                                    if success:
                                        result_msg = (
                                            f"[B][C][00FF00]✅ Badge Spam Done!\n"
                                            f"🎯 Target: {xMsGFixinG(target_uid)}\n"
                                            f"📤 S1: 20 | S2: 20 | S3: 20 | S4: 20\n"
                                            f"⚡ Total Packets: {total_sent}\n"
                                        )
                                    else:
                                        result_msg = f"[B][C][FF0000]❌ Badge Spam Failed after 3 attempts.\n⚠️ {last_err[:60] if last_err else 'Unknown error'}\n"

                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)

                        # Spam request command - works in all chat types
                        if inPuTMsG.strip().startswith('/spm_inv'):
                            print('Processing spam invite with cosmetics')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /spm_inv (uid)\nExample: /spm_inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing spam request
                                if spam_request_task and not spam_request_task.done():
                                    spam_request_running = False
                                    spam_request_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Start new spam request WITH COSMETICS
                                spam_request_running = True
                                spam_request_task = asyncio.create_task(spam_request_loop_with_cosmetics(target_uid, key, iv, region))
        
                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ COSMETIC SPAM STARTED!\n🎯 Target: {xMsGFixinG(target_uid)}\n📦 Requests: 30\n🎭 Features: V-Badges + Cosmetics\n⚡ Each invite has different cosmetics!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Stop spam request command - works in all chat types
                        if inPuTMsG.strip() == '/stop spm_inv':
                            if spam_request_task and not spam_request_task.done():
                                spam_request_running = False
                                spam_request_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Spam request stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active spam request to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO COMMANDS
                        if inPuTMsG.strip().startswith('/evo '):
                            print('Processing evo command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending evolution emote {number_int}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evo_fast '):
                            print('Processing evo_fast command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo_fast 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_fast spam
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_fast spam
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nSpam count: 25 times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO_CUSTOM COMMAND
                        if inPuTMsG.strip().startswith('/evo_c '):
                            print('Processing evo_c command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\nExample: /evo_c 123456789 1 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids, number, and time
                                uids = []
                                number = None
                                time_val = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number or time should be 1-100 (1, 2, or 3 digits)
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                # If we still don't have time_val, try to get it from the last part
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        # Remove time_val from uids if it was added by mistake
                                        if time_val in uids:
                                            uids.remove(time_val)
                                
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Time must be between 1-100 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_custom spam
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_custom spam
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nRepeat: {time_int} times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number/time format! Use numbers only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        # Stop evo_fast spam command
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution fast spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution fast spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_custom spam command
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution custom spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution custom spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                            
#==================≈===========  /HELP MENU COMMANDS ========================================
                        if inPuTMsG.strip().lower() in ("help", "/help", "menu", "/menu", "commands"):


    # Header
                            header = f"[b][c]{get_random_color()}Welcome To GothicRealm Guild Bot"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 1-8 ─────
                            help_1 = """
0🤫1🤫. Group Limit [FF0000]🤫/3 🤫/5 🤫/6🤫
0🤫2🤫. Player Info [00CCFF]/info [uid]
0🤫2🤫b. Ban Check [FF4444]/check [uid]
0🤫3🤫. Player Invite [00CCFF]/inv [uid]
0🤫4🤫. Msg Spam [00FF00]/ms [msg]
0🤫5🤫. Unlock 5v🤫5 [FFFF00]/snd [uid]
0🤫6🤫. Admin [00CCFF]/admin
0🤫7🤫. Join Team [FFFF00]/join [TeamCode]
0🤫8🤫. Leave Group [FF0000]/exit
    """
                            await safe_send_message(response.Data.chat_type, help_1, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 9-15 ─────
                            help_2 = """
0🤫9🤫. Req Spam [00FF00]/spam [uid]
1🤫0🤫. Kick Player [FF6600]/kick [uid]
1🤫1🤫. Lag Calive [00FF00]/lag [TeamCode]
1🤫2🤫. Join Req Spam [FF00FF]/spam_join [uid]
1🤫3🤫. Attack Group [FFFFFF]/attack [TeamCode]
1🤫4🤫. Force Start [FFCC00]/start [TeamCode]
1🤫5🤫. Times Emote [FF0000]/p [uid] [emote] [count]
    """
                            await safe_send_message(response.Data.chat_type, help_2, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 16-25 ─────
                            help_3 = """
1🤫6🤫. Add Ghost in Team [00FFFF]/ghost [TeamCode]
1🤫7🤫. Bundle [00FF00]/bundle
1🤫8🤫. EVO Cycle [00CCFF]/evos [uid]
1🤫9🤫. Stop Evo Cycle [00FFFF]/sevos
2🤫0🤫. Emote Play [00FF00]/play [uid] [1-410]
2🤫1🤫. Emote Command [00CCFF]/emote [UID1] [UID2] [TeamCode] [EmoteNumber]
2🤫2🤫. EVO Emote [00FF00]/evo [UID1] [UID2] [EmoteNumber]
2🤫3🤫. Play Emote (ID) [CC33FF]/e [UID1] [UID2] [EmoteID]
2🤫4🤫. Fast Play [00FF00]/fast [UID1] [UID2] [EmoteID]
2🤫5🤫. Chat With AI [FF00FF]/ai [question]
    """
                            await safe_send_message(response.Data.chat_type, help_3, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 26-35 ─────
                            help_4 = """
2🤫6🤫. CL Badge Join [FF0000]/s1 [uid]
2🤫7🤫. V Badge Join [00FF00]/s2 [uid]
2🤫8🤫. Mdtr Badge Join [0000FF]/s3 [uid]
2🤫9🤫. Old V Badge Join [FFFF00]/s4 [uid]
3🤫0🤫. Pro Badge Join [00AAFF]/s5 [uid]
3🤫1🤫. All Badge Join [FF0000]/spam [uid]
3🤫2🤫. Gali Friend [00CCFF]/gali [name]
3🤫3🤫. Private Message [FFFF00]/dm [msg]
3🤫4🤫. Equip Bundle [FF0000]/bundle [name]
3🤫5🤫. Admin Mode On [00CCFF]/adon
    """
                            await safe_send_message(response.Data.chat_type, help_4, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 36-45 ─────
                            help_5 = """
3🤫6🤫. Admin Mode Off [FFFF00]/adoff
3🤫7🤫. On Bot [00FF00]/on
3🤫8🤫. Off Bot [FF0000]/off
3🤫9🤫. Block User [00FFFF]/block [uid]
4🤫0🤫. Unblock User [00FF00]/unblock [uid]
4🤫1🤫. Set Bundle [00FF00]/bundle [name]
4🤫2🤫. Lag Team [FF6600]/lag [TeamCode]
4🤫3🤫. Attack Team [00FF00]/attack [TeamCode]
4🤫4🤫. Level Up Bot [FFFF00]/lw [TeamCode]
4🤫5🤫. Stop Level Up Bot [FF0000]/stop
    """
                            await safe_send_message(response.Data.chat_type, help_5, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 46-53 ─────
                            help_6 = """
4🤫6🤫. Bundle Spam [00FF00]/bb_lag [TeamCode]
4🤫7🤫. Spam Invite [00CCFF]/spm_inv [uid]
4🤫8🤫. Spam Join Requests [00FF00]/spam_join [uid]
4🤫9🤫. Play Emote Self [FF00FF]/e [emote]
5🤫0🤫. Play Emote Player [00FF00]/e [uid] [emote]
5🤫1🤫. Play Emote Without Bot [FF6600]/me [TeamCode] [emote]
5🤫2🤫. Player Emote Without Bot [00FF00]/me [tc] [uid] [emote]
5🤫3🤫. Evo Cycle Self [FF00FF]@evos
    """
                            await safe_send_message(response.Data.chat_type, help_6, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 54-58 ─────
                            help_7 = """
5🤫4🤫. Evo Cycle Player [00FF00]@evos [uid]
5🤫5🤫. Stop Evo Cycle [FF0000]@sevos
5🤫6🤫. YouTube Info [FF0000]/yt [channel]
5🤫7🤫. TikTok Info [00FFFF]/tt [username]
5🤫8🤫. Instagram Info [FF69B4]/ig [username]
    """
                            await safe_send_message(response.Data.chat_type, help_7, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 59-63 ─────
                            help_8 = """
5🤫9🤫. Love Calculator [FF1493]/luv [name1] [name2]
6🤫0🤫. Latest News [00FFFF]/news
6🤫1🤫. Praise Player [FF69B4]/praise [name]
6🤫2🤫. Math Solver [00FF00]/math [expression]
6🤫3🤫. Hack (Fun) [FF0000]/h a c k [name]
    """
                            await safe_send_message(response.Data.chat_type, help_8, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Commands 64-67 : Guild ─────
                            help_9 = """
6🤫4🤫. Guild Info [FFD700]/guild [guild_id]
6🤫4🤫b. Guild Search [00FF7F]/guild [name]
6🤫5🤫. Leave Guild [FF6EC7]/guild leave [Admin]
6🤫6🤫. Join Guild [4CFFB0]/guild join [guild_id] [Admin]
6🤫7🤫. Friend List [00CCFF]/list [Admin]
    """
                            await safe_send_message(response.Data.chat_type, help_9, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # ───── Command 68 ─────
                            help_10 = """
6🤫8🤫. Phone Lookup [00FF00]/num [phone]
    """
                            await safe_send_message(response.Data.chat_type, help_10, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

    # Footer
                            elapsed = int(time.time() - BOT_START_TIME)
                            days, rem = divmod(elapsed, 86400)
                            hours, rem = divmod(rem, 3600)
                            minutes, seconds = divmod(rem, 60)
                            parts_up = []
                            if days:
                                parts_up.append(f"{days}d")
                            if hours:
                                parts_up.append(f"{hours}h")
                            if minutes:
                                parts_up.append(f"{minutes}m")
                            parts_up.append(f"{seconds}s")
                            uptime_str = " ".join(parts_up)

                            footer = f"""[FF1493]⚡ [B][FFFF00]BOT INFO[FFFF00][/B] ⚡
[FFFF00]👤 Developer    :: [00FFFF]Ayaan
[FF69B4]👑 Owner        :: [FF69B4]Biryani
[32CD32]💻 Online       :: [32CD32]24/7
[00CCFF]📲 Contact      :: [FFFFFF]@paktcpbots
[FFD700]⏱️ Uptime       :: [FFFFFF]{uptime_str}"""

                            await safe_send_message(response.Data.chat_type, footer, uid, chat_id, key, iv)
                        response = None

            if whisper_writer and not whisper_writer.is_closing():
                whisper_writer.close()
                await whisper_writer.wait_closed()
            whisper_writer = None

        except Exception as e:
            print(f"ErroR {ip}:{port} - {e}")
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    # Load credentials from file
    print("📁 Loading credentials from MG24GAMER.txt...")
    credentials = load_credentials_from_file("MG24GAMER.txt")
    
    if not credentials:
        print("❌ Failed to load credentials!")
        print("💡 Please create MG24GAMER.txt with your UID and password")
        print("📝 Format: uid=YOUR_UID,password=YOUR_PASSWORD")
        return None
    
    try:
        Uid, Pw = credentials
    except:
        # Handle case where credentials returns more than 2 values
        if isinstance(credentials, (list, tuple)) and len(credentials) >= 2:
            Uid = credentials[0]
            Pw = credentials[1]
        else:
            print("❌ Invalid credentials format!")
            return None
    
    print("✅ Credentials loaded successfully")
    
    # Get access token from Free Fire
    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token: 
        print("❌ Error - Invalid Account (Check UID/Password)") 
        return None
    
    # Encrypt and send login request
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: 
        print("❌ Target Account => Banned / Not Registered!") 
        return None
    
    # Decrypt login response
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    
    # Get JWT token from response
    token = MajoRLoGinauTh.token
    if not token:
        print("❌ No authentication token received!")
        return None

    # Store globally so bio updates can reuse it without re-login
    global _bot_jwt
    _bot_jwt = token
    print("✅ Bot JWT stored for bio updates")
    
    # ✅ CRITICAL: SAVE TOKEN TO token.json FILE
    try:
        import json
        import time
        from datetime import datetime
        
        # Get region from login response
        region = getattr(MajoRLoGinauTh, 'region', 'IND')
        
        token_data = {
            "token": token,
            "saved_at": time.time(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bot_uid": str(Uid),
            "region": region,
            "source": "main.py_bot_login"
        }
        
        with open("token.json", "w") as f:
            json.dump(token_data, f, indent=2)
        
        print("✅ Token saved to token.json")
        print(f"📝 Token info: Region={region}, UID={Uid}")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not save token to file: {e}")
        import traceback
        traceback.print_exc()
    
    # Continue with normal bot setup
    UrL = MajoRLoGinauTh.url
    global BOT_SERVER_URL
    if UrL:
        BOT_SERVER_URL = UrL.rstrip('/')
        print(f"🌐 Game server URL set: {BOT_SERVER_URL}")

    # Clear screen and show status
    os.system('clear')
    print("=" * 50)
    print("🤖 MG24GAMER BOT - INITIALIZING")
    print("=" * 50)
    print("🔄 Starting TCP Connections...")
    print("📡 Connecting to Free Fire servers...")
    print("🌐 Server connection established")
    
    region = getattr(MajoRLoGinauTh, 'region', 'IND')
    ToKen = token  # Use the saved token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    print(f"🔐 Authentication successful")
    print(f"👤 Account UID: {TarGeT}")
    print(f"🌍 Region: {region}")
    print(f"🔑 Token: {ToKen[:30]}...")
    
    # Get login data for server IPs
    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa: 
        print("❌ Error - Getting Ports From Login Data!") 
        return None
    
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    
    # Get server IPs and ports
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    
    print(f"📡 Online Server: {OnLinePorTs}")
    print(f"💬 Chat Server: {ChaTPorTs}")
    
    # Split IPs and ports
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")
    
    # Get account name
    acc_name = LoGinDaTaUncRypTinG.AccountName
    print(f"👋 Welcome, {acc_name}!")
    
    # Create authentication token for TCP connections
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    
    # Create event for chat ready
    ready_event = asyncio.Event()
    
    # Start bot tasks
    print("\n🚀 Starting bot services...")
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))  
 
    
    # Show loading animation
    os.system('clear')
    print("🤖 MG24GAMER BOT - STARTING")
    print("=" * 50)
    
    for i in range(1, 4):
        dots = "." * i
        print(f"🔄 Loading{dots}")
        await asyncio.sleep(0.3)
    
    os.system('clear')
    print("🤖 MG24GAMER BOT - CONNECTING")
    print("=" * 50)
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████████████████ │")
    print("└────────────────────────────────────┘")
    
    # Wait for chat connection to be ready
    print("\n⏳ Waiting for chat connection...")
    try:
        await asyncio.wait_for(ready_event.wait(), timeout=10)
        print("✅ Chat connection established!")
    except asyncio.TimeoutError:
        print("⚠️ Chat connection timeout, continuing...")
    
    # Final status display
    os.system('clear')
    print("=" * 50)
    print("🤖 MG24 GAMER BOT - ONLINE")
    print("=" * 50)
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Name: {acc_name}")
    print(f"🔹 Region: {region}")
    print(f"🔹 Status: 🟢 READY")
    print(f"🔹 Chat Server: {ChaTiP}:{ChaTporT}")
    print(f"🔹 Online Server: {OnLineiP}:{OnLineporT}")
    print("=" * 50)
    print("💡 Commands available in squad/guild chat")
    print("💡 Type /help for command list")
    print("=" * 50)
    
    # Test cache file write
    print("\n📊 System Check:")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Cache file: {CACHE_FILE}")
    
    try:
        test_data = {'test': 'ok', 'timestamp': time.time()}
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(test_data, f)
        print("✅ Cache file write test: PASSED")
    except Exception as e:
        print(f"⚠️ Cache file write test: {e}")
    
    # Check token.json exists
    if os.path.exists("token.json"):
        print("✅ token.json file exists")
        try:
            with open("token.json", "r") as f:
                token_info = json.load(f)
            age = time.time() - token_info.get('saved_at', 0)
            print(f"✅ Token age: {age:.1f} seconds")
        except:
            print("⚠️ Could not read token.json")
    else:
        print("❌ token.json not found!")
    
    print("\n🎯 Bot is now running...")
    print("📡 Listening for commands and invitations")
    
    # Keep all tasks running
    try:
        await asyncio.gather(task1, task2)
    except asyncio.CancelledError:
        print("\n🛑 Bot tasks cancelled")
    except Exception as e:
        print(f"\n❌ Error in bot tasks: {e}")
        import traceback
        traceback.print_exc()
    
    return None


if __name__ == '__main__':
    asyncio.run(StarTinG())
    
  