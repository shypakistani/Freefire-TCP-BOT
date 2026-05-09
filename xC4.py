# By AbdeeLkarim BesTo

import requests , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading , random , os , asyncio
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Key , Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]) , bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

async def EnC_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
    
async def DEc_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()
    
async def EnC_PacKeT(HeX , K , V): 
    return AES.new(K , AES.MODE_CBC , V).encrypt(pad(bytes.fromhex(HeX) ,16)).hex()
    
async def DEc_PacKeT(HeX , K , V):
    return unpad(AES.new(K , AES.MODE_CBC , V).decrypt(bytes.fromhex(HeX)) , 16).hex()  

async def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

async def EnC_Vr(N):
    if N < 0: ''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)
    
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n
    
async def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return await EnC_Vr(field_header) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return await EnC_Vr(field_header) + await EnC_Vr(len(encoded_value)) + encoded_value

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await CrEaTe_ProTo(value)  # لازم await
            packet.extend(await CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet
    
async def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    if len(F) == 1: F = "0" + F ; return F
    else: return F

async def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = await Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

async def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = await Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
                      
def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 3] for i in range(0 , len(str(n)) , 3))
    
async def Ua():
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"
    
async def ArA_CoLor():
    Tp = ["32CD32" , "00BFFF" , "00FA9A" , "90EE90" , "FF4500" , "FF6347" , "FF69B4" , "FF8C00" , "FF6347" , "FFD700" , "FFDAB9" , "F0F0F0" , "F0E68C" , "D3D3D3" , "A9A9A9" , "D2691E" , "CD853F" , "BC8F8F" , "6A5ACD" , "483D8B" , "4682B4", "9370DB" , "C71585" , "FF8C00" , "FFA07A"]
    return random.choice(Tp)
    
async def xBunnEr():
    bN = [902048021]
    return random.choice(bN)

async def send_room_chat_enhanced(Msg, room_id, key, iv, region):
    """Send room chat message using leaked packet structure"""
    fields = {
        1: 1,
        2: {
            1: 9280892890,  # Sender UID (from leaked packet)
            2: int(room_id),
            3: 3,  # Chat type 3 = room chat
            4: f"[{await ArA_CoLor()}]{Msg}",  # Message with color
            5: int(datetime.now().timestamp()),  # Current timestamp
            7: 2,
            9: {
                1: "RIJEXX",  # Your bot name
                2: int(await xBunnEr()),  # Avatar from your system
                4: 228,  # Rank/level from leaked packet
                7: 1,    # Unknown
            },
            10: "en",  # Changed from "ar" to "en"
            13: {2: 1, 3: 1},
        },
    }
    
    # Generate packet using your existing system
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    # Use 1215 packet type for chat messages (like your existing system)
    return await GeneRaTePk(packet, '1215', key, iv)

async def xSEndMsg(Msg , Tp , Tp2 , id , K , V):
    feilds = {1: id , 2: Tp2 , 3: Tp, 4: Msg, 5: 1735129800, 7: 2, 9: {1: "[FFFFFF]BLACK", 2: int(await xBunnEr()), 3: 901048020, 4: 330, 5: 1001000001, 8: "xBesTo - C4", 10: 1, 11: 1, 13: {1: 2}, 14: {1: 12484827014, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}, 12: 0}, 10: "en", 13: {3: 1}}    
    Pk = (await CrEaTe_ProTo(feilds)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
    
async def xSEndMsgsQ(Msg , id , K , V, region="BD"):
    """Send message with region 1 title included"""
    
    # Get random avatar
    avatar = await xBunnEr()
    
    fields = {
        1: id, 
        2: id, 
        4: Msg, 
        5: 1756580149, 
        7: 2, 
        8: 904990072, 
        9: {
            1: "[FFFFFF]BLACK",
            2: avatar, 
            3: 2,
            4: 329, 
            5: 1001000001, 
            6: 66,
            7: 66,
            8: "xBe4!sTo - C4", 
            9: 66,
            10: 66, 
            11: 66, 
            12: 66,
            13: {1: 68, 2:67}, 
            14: {
                1: 1158053040, 
                2: 8, 
                3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
            }
        }, 
        10: "en", 
        13: {66: 66, 66: 66},
        # ADD REGION 1 TITLE HERE (from second packet field 14)
        14: {
            11: {
                1: 3,          # Field 1
                2: 7,                              # Field 2  
                3: 170,         # Field 3
                4: 999,                              # Field 4
                5: 1, # Field 5
                6: region,              
                7: 2,
                8: 2,
                9: 2
            }
        }
    }
    
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
    
async def xSEndMsgsQq(Msg , id , K , V, region="IND"):
    """Send message with region 1 title included"""
    
    # Get random avatar
    avatar = await xBunnEr()
    
    fields = {
        1: id, 
        2: id, 
        4: Msg, 
        5: 1756580149, 
        7: 2, 
        8: 904990072, 
        9: {
            1: "xBe4!sTo - C4", 
            2: avatar, 
            4: 330, 
            5: 1001000001, 
            8: "xBe4!sTo - C4", 
            10: 1, 
            11: 1, 
            13: {1: 2}, 
            14: {
                1: 1158053040, 
                2: 8, 
                3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
            }
        }, 
        10: "en", 
        13: {2: 2, 3: 1},
        # ADD REGION 1 TITLE HERE (from second packet field 14)
        14: {
            1: {
                1: random.choice([1, 4]),          # Field 1
                2: 1,                              # Field 2  
                3: random.randint(1, 180),         # Field 3
                4: 1,                              # Field 4
                5: int(datetime.now().timestamp()), # Field 5
                6: region                          # Field 6 (region)
            }
        }
    }
    
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)

async def AutH_GlobAl(K, V):
    fields = {
    1: 3,
    2: {
        2: 5,
        3: "en"
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)

async def LagSquad(K,V):
    fields = {
    1: 15,
    2: {
        1: 1124759936,
        2: 1
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)

async def GeT_Status(PLayer_Uid , K , V):
    PLayer_Uid = await EnC_Uid(PLayer_Uid , Tp = 'Uid')
    if len(PLayer_Uid) == 8: Pk = f'080112080a04{PLayer_Uid}1005'
    elif len(PLayer_Uid) == 10: Pk = f"080112090a05{PLayer_Uid}1005"
    return await GeneRaTePk(Pk , '0f15' , K , V)
           
async def SPam_Room(Uid , Rm , Nm , K , V):
    fields = {1: 78, 2: {1: int(Rm), 2: f"[{ArA_CoLor()}]{Nm}", 3: {2: 1, 3: 1}, 4: 330, 5: 1, 6: 201, 10: xBunnEr(), 11: int(Uid), 12: 1}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0e15' , K , V)
async def GenJoinSquadsPacket(code,  K , V):
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][4] = bytes.fromhex("01090a0b121920")
    fields[2][5] = str(code)
    fields[2][6] = 6
    fields[2][8] = 1
    fields[2][9] = {}
    fields[2][9][2] = 800
    fields[2][9][6] = 11
    fields[2][9][8] = "1.111.1"
    fields[2][9][9] = 5
    fields[2][9][10] = 1
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)   
async def GenJoinGlobaL(owner , code , K, V):
    fields = {
    1: 4,
    2: {
        1: owner,
        6: 1,
        8: 1,
        13: "en",
        15: code,
        16: "OR",
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)



async def FS(key, iv, region="ind"):
    """Start match packet - converted from TCP version"""
    try:
        # Your original fields from TCP bot
        fields = {
            1: 9,  # Start match packet type
            2: {
                1: 12480598706,  # Your UID or specific value
            }
        }
        
        # Create protobuf packet
        packet = await CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
        
        # Encrypt the packet
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        
        # Calculate header length
        header_length = len(encrypted_packet) // 2
        header_length_final = dec_to_hex(header_length)
        
        # Determine packet type based on region
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
        
        # Build final packet based on header length
        if len(header_length_final) == 2:
            final_packet_hex = packet_type + "000000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 3:
            final_packet_hex = packet_type + "00000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 4:
            final_packet_hex = packet_type + "0000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 5:
            final_packet_hex = packet_type + "000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 6:
            final_packet_hex = packet_type + "00" + header_length_final + encrypted_packet
        else:
            final_packet_hex = packet_type + "000000" + header_length_final + encrypted_packet
        
        print(f"✅ Start match packet created: {len(final_packet_hex)//2} bytes")
        return bytes.fromhex(final_packet_hex)
        
    except Exception as e:
        print(f"❌ Error creating start packet: {e}")
        import traceback
        traceback.print_exc()
        return None

#EMOTES BY PARAHEX X CODEX
async def Emote_k(TarGeT , idT, K, V,region):
    fields = {
        1: 21,
        2: {
            1: 804266360,
            2: 909000001,
            5: {
                1: TarGeT,
                3: idT,
            }
        }
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)

#EMOTES BY PARAHEX X CODEX


async def GeTSQDaTa(D):
    uid = D['5']['data']['1']['data']
    chat_code = D["5"]["data"]["17"]["data"]
    squad_code = D["5"]["data"]["31"]["data"]


    return uid, chat_code , squad_code

  
async def AuthClan(CLan_Uid, AuTh, K, V):
    fields = {1: 3, 2: {1: int(CLan_Uid), 2: 1, 4: str(AuTh)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1201' , K , V)

def join_room_chanel(room_id, key, iv):
    fields = {
        1: 3,
        2: {
            1: int(room_id),
            2: 3,
            3: "en",
        },
    }
    packet = create_protobuf_packet(fields)
    packet = packet.hex() + "7200"
    header_lenth = len(encrypt_packet(packet, key, iv)) // 2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) == 2:
        # print(header_lenth)
        # print('len of headr == 2')
        final_packet = "1215000000" + header_lenth + encrypt_packet(packet, key, iv)
        # print(final_packet)
        return bytes.fromhex(final_packet)

    if len(header_lenth) == 3:
        #  print(header_lenth)
        #  print('len of headr == 3')
        final_packet = "121500000" + header_lenth + encrypt_packet(packet, key, iv)
        # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) == 4:
        #  print('len of headr == 4')
        final_packet = "12150000" + header_lenth + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)
    if len(header_lenth) == 5:
        final_packet = "12150000" + header_lenth + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)

async def AutH_Chat(T , uid, code , K, V):
    fields = {
  1: T,
  2: {
    1: uid,
    3: "en",
    4: str(code)
  }
}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)
async def Msg_Sq(msg, owner, bot, K, V):
    fields = {
    1: 1,
    2: 2,
    2: {
        1: bot,
        2: owner,
        4: msg,
        5: 1757799182,
        7: 2,
        9: {
            1: "Fun1w5a2",
            2: await xBunnEr(),
            3: 909000024,
            4: 330,
            5: 909000024,
            7: 2,
            10: 1,
            11: 1,
            12: 0,
            13: {1: 2},
            14: {
                1: bot,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        10: "ar",
        13: {3: 1},
        14: ""
    }
}
    proto_bytes = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_bytes.hex(), '1215', K, V)


async def ghost_pakcet(player_id , secret_code ,K , V):
    fields = {
        1: 61,
        2: {
            1: int(player_id),  
            2: {
                1: int(player_id),  
                2: int(time.time()),  
                3: "MR3SKR",
                5: 12,  
                6: 9999999,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: secret_code,},}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
async def GeneRaTePk(Pk , N , K , V):
    PkEnc = await EnC_PacKeT(Pk , K , V)
    _ = await DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    else: print('ErroR => GeneRatinG ThE PacKeT !! ')
    return bytes.fromhex(HeadEr + _ + PkEnc)
async def OpEnSq(K , V,region):
    fields = {1: 1, 2: {2: "\u0001", 3: 1, 4: 1, 5: "en", 9: 1, 11: 1, 13: 1, 14: {2: 5756, 6: 11, 8: "1.111.5", 9: 2, 10: 4}}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)

async def cHSq(Nu , Uid , K , V,region):
    fields = {1: 17, 2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)




async def SEnd_InV(Nu , Uid , K , V,region):
    
    fields = {1: 2 , 2: {1: int(Uid) , 2: region , 4: int(Nu)}}

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)


async def ExiT(idT , K , V):
    fields = {
        1: 7,
        2: {
            1: idT,
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V) 
    
async def ArohiRefuse(owner,uid, K,V):
    fields = {
    1: 5,
    2: {
        1: int(owner),
        2: 1,
        3: int(uid),
        4: "[FF0000][B][C] ERROR , WELCOME TO [FFFFFF]REDZED [00FF00] AROHI BOT ! \n[FFFF00]NEW VERSION NEW FUNCTION !\n[FF0000]TELEGRAM : @classic_arohi\n\n"
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
# Isko file ke sabse neeche (Bottom) paste karein


async def bundle_packet_async(bundle_id, K, V, region):
    """Create bundle packet optimized"""
    fields = {
        1: 88,
        2: {
            1: {
                1: int(bundle_id), 
                2: 1
            },
            2: 2
        }
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, K, V)
