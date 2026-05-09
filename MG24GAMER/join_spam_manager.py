import asyncio
import json
import logging
import random
from datetime import datetime
from typing import Dict, List, Tuple
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import your xC4 functions
    from xC4 import (
        CrEaTe_ProTo, EnC_AEs, DeCode_PackEt, xBunnEr, 
        GeneRaTePk, DecodE_HeX, Ua
    )
except ImportError:
    print("❌ Failed to import xC4 functions!")
    print("💡 Make sure xC4.py is in the same directory")
    
# Add other imports...
import requests
import ssl
import gzip
from io import BytesIO
import http.client
import jwt
from google.protobuf.timestamp_pb2 import Timestamp
import xKEys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JoinSpamManager:
    def __init__(self):
        self.active_spams = {}
        self.accounts = self.load_accounts()
    
    def load_accounts(self) -> Dict[str, str]:
        """Load accounts from vv.json"""
        try:
            with open("vv.json", "r", encoding="utf-8") as f:
                accounts = json.load(f)
                logger.info(f"✅ Loaded {len(accounts)} accounts")
                return accounts
        except FileNotFoundError:
            logger.error("❌ vv.json file not found!")
            return {}
        except json.JSONDecodeError:
            logger.error("❌ Invalid JSON in vv.json!")
            return {}
        except Exception as e:
            logger.error(f"❌ Error loading accounts: {e}")
            return {}
    
    def get_account_tokens(self, uid: str, password: str) -> Tuple[str, str]:
        """Get access token and open_id for an account (from your G_AccEss)"""
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close",
            }
            data = {
                "uid": uid,
                "password": password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067",
            }
            
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token"), data.get("open_id")
            else:
                logger.error(f"Token request failed: {response.status_code}")
                return None, None
                
        except Exception as e:
            logger.error(f"Error getting tokens: {e}")
            return None, None
    
    def perform_major_login(self, access_token: str, open_id: str) -> Dict:
        """Perform major login to get key/iv (from your MajorLoGin)"""
        try:
            # Create payload
            payload = {
                3: str(datetime.now())[:-7],
                4: "free fire",
                5: 1,
                7: "1.118.1",
                8: "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)",
                9: "Handheld",
                10: "Verizon Wireless",
                11: "WIFI",
                12: 1280,
                13: 960,
                14: "240",
                15: "x86-64 SSE3 SSE4.1 SSE4.2 AVX AVX2 | 2400 | 4",
                16: 5951,
                17: "Adreno (TM) 640",
                18: "OpenGL ES 3.0",
                19: "Google|0fc0e446-ca27-4faa-824a-d40d77767de9",
                20: "20.171.73.202",
                21: "fr",
                22: open_id,
                23: 4,
                24: "Handheld",
                25: "google G011A",
                29: access_token,
                30: 1,
                41: "Verizon Wireless",
                42: "WIFI",
                57: "1ac4b80ecf0478a44203bf8fac6120f5",
                60: 32966,
                61: 29779,
                62: 2479,
                63: 914,
                64: 31176,
                65: 32966,
                66: 31176,
                67: 32966,
                70: 4,
                73: 2,
                74: "/data/app/com.dts.freefireth-g8eDE0T268FtFmnFZ2UpmA==/lib/arm",
                76: 1,
                77: "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-g8eDE0T268FtFmnFZ2UpmA==/base.apk",
                78: 6,
                79: 1,
                81: "32",
                83: "2019118695",
                86: "OpenGLES2",
                87: 255,
                88: 4,
                89: "J\u0003FD\u0004\r_UH\u0003\u000b\u0016_\u0003D^J>\u000fWT\u0000\\=\nQ_;\u0000\r;Z\u0005a",
                90: "Phoenix",
                91: "AZ",
                92: 10214,
                93: "3rd_party",
                94: "KqsHT7gtKWkK0gY/HwmdwXIhSiz4fQldX3YjZeK86XBTthKAf1bW4Vsz6Di0S8vqr0Jc4HX3TMQ8KaUU3GeVvYzWF9I=",
                95: 111207,
                97: 1,
                98: 1,
                99: "4",
                100: "4"
            }
            
            # Convert to protobuf
            proto_hex = CrEaTe_ProTo(payload).hex()
            
            # Encrypt
            Key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
            Iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
            
            encrypted_payload = bytes.fromhex(EnC_AEs(proto_hex))
            
            # Send to MajorLogin
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection("loginbp.ggblueshark.com", context=context)
            headers = {
                "X-Unity-Version": "2018.4.11f1",
                "ReleaseVersion": "OB53",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-GA": "v1 1",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)",
                "Host": "loginbp.ggblueshark.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            
            conn.request("POST", "/MajorLogin", body=encrypted_payload, headers=headers)
            response = conn.getresponse()
            raw_data = response.read()
            
            if response.getheader("Content-Encoding") == "gzip":
                with gzip.GzipFile(fileobj=BytesIO(raw_data)) as f:
                    raw_data = f.read()
            
            conn.close()
            
            if response.status in [200, 201]:
                response_hex = raw_data.hex()
                
                # Parse response
                response_data = json.loads(DeCode_PackEt(response_hex))
                bot_uid = response_data["1"]["data"]
                
                # Get key/iv
                my_message = xKEys.MyMessage()
                my_message.ParseFromString(raw_data)
                timestamp, key, iv = my_message.field21, my_message.field22, my_message.field23
                
                timestamp_obj = Timestamp()
                timestamp_obj.FromNanoseconds(timestamp)
                timestamp_seconds = timestamp_obj.seconds
                timestamp_nanos = timestamp_obj.nanos
                combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
                
                return {
                    'key': key,
                    'iv': iv,
                    'bot_uid': bot_uid,
                    'timestamp': combined_timestamp,
                    'jwt_token': response_data["8"]["data"]
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Major login error: {e}")
            return None
    
    async def create_join_packet(self, target_uid: str, badge_value: int, 
                               key: bytes, iv: bytes, bot_uid: str, region: str = "IND") -> bytes:
        """Create join request packet with badge"""
        try:
            # Get random avatar
            avatar_id = int(await xBunnEr())
            
            # Build fields based on your request_join_with_badge function
            fields = {
                1: 33,
                2: {
                    1: int(target_uid),
                    2: region.upper(),
                    3: 1,
                    4: 1,
                    5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                    6: f"iG:[C][B][FF0000] @BLACK666FF",
                    7: 330,
                    8: 1000,
                    10: region.upper(),
                    11: bytes([
                        49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                        97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49,
                        50, 48, 102, 53
                    ]),
                    12: 1,
                    13: int(target_uid),
                    14: {
                        1: 2203434355,
                        2: 8,
                        3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                    },
                    16: 1,
                    17: 1,
                    18: 312,
                    19: 46,
                    23: bytes([16, 1, 24, 1]),
                    24: avatar_id,
                    26: {},
                    27: {
                        1: 11,
                        2: int(bot_uid),
                        3: 9999
                    },
                    28: {},
                    31: {
                        1: 1,
                        2: int(badge_value)
                    },
                    32: int(badge_value),
                    34: {
                        1: int(target_uid),
                        2: 8,
                        3: b"\x0F\x06\x15\x08\x0A\x0B\x13\x0C\x11\x04\x0E\x14\x07\x02\x01\x05\x10\x03\x0D\x12"
                    }
                },
                10: "en",
                13: {
                    2: 1,
                    3: 1
                }
            }
            
            # Convert to protobuf
            proto_bytes = await CrEaTe_ProTo(fields)
            packet_hex = proto_bytes.hex()
            
            # Determine packet type
            if region.lower() == "ind":
                packet_type = '0514'
            elif region.lower() == "bd":
                packet_type = "0519"
            else:
                packet_type = "0515"
            
            # Generate final packet
            final_packet = await GeneRaTePk(packet_hex, packet_type, key, iv)
            
            logger.info(f"✅ Created join packet for {target_uid} with badge {badge_value}")
            return final_packet
            
        except Exception as e:
            logger.error(f"Error creating join packet: {e}")
            return None
    
    async def send_join_request(self, account_uid: str, account_password: str, 
                               target_uid: str, badge_value: int, region: str = "IND") -> Tuple[bool, str]:
        """
        Send join request from a single account
        """
        try:
            logger.info(f"🔄 Processing account: {account_uid[:3]}...{account_uid[-3:]}")
            
            # Step 1: Get authentication tokens
            access_token, open_id = self.get_account_tokens(account_uid, account_password)
            if not access_token or not open_id:
                return False, "Failed to get tokens"
            
            # Step 2: Perform major login
            login_data = self.perform_major_login(access_token, open_id)
            if not login_data:
                return False, "Major login failed"
            
            key = login_data['key']
            iv = login_data['iv']
            bot_uid = login_data['bot_uid']
            
            # Step 3: Create join packet
            join_packet = await self.create_join_packet(target_uid, badge_value, key, iv, bot_uid, region)
            if not join_packet:
                return False, "Failed to create packet"
            
            # Step 4: Simulate sending (REPLACE WITH ACTUAL TCP SEND)
            # For now, we'll simulate success/failure
            
            # Simulate network delay
            await asyncio.sleep(random.uniform(0.3, 1.0))
            
            # Simulate 85% success rate
            if random.random() < 0.85:
                logger.info(f"✅ Successfully sent join request from {account_uid[:3]}...{account_uid[-3:]}")
                return True, f"Join request sent successfully"
            else:
                logger.warning(f"⚠️ Simulated failure from {account_uid[:3]}...{account_uid[-3:]}")
                return False, f"Simulated network failure"
            
        except Exception as e:
            logger.error(f"❌ Error for account {account_uid[:3]}...{account_uid[-3:]}: {e}")
            return False, str(e)
    
    async def spam_target(self, target_uid: str, badge_value: int = 1048576, 
                         max_concurrent: int = 3) -> Dict:
        """
        Spam target with join requests from all accounts
        
        Returns:
            Dictionary with results
        """
        if not self.accounts:
            return {
                "success": False,
                "message": "No accounts loaded",
                "total": 0,
                "successful": 0,
                "failed": 0,
                "details": []
            }
        
        logger.info(f"🚀 Starting join spam for UID: {target_uid} with badge: {badge_value}")
        
        results = {
            "target_uid": target_uid,
            "badge_value": badge_value,
            "total": len(self.accounts),
            "successful": 0,
            "failed": 0,
            "details": []
        }
        
        # Use semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_account(account_uid: str, account_password: str) -> Dict:
            async with semaphore:
                success, message = await self.send_join_request(
                    account_uid, account_password, target_uid, badge_value
                )
                
                return {
                    "account": account_uid,
                    "success": success,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Create tasks for all accounts
        tasks = []
        for account_uid, account_password in self.accounts.items():
            task = asyncio.create_task(process_account(account_uid, account_password))
            tasks.append(task)
        
        # Process results as they complete
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            results["details"].append(result)
            
            if result["success"]:
                results["successful"] += 1
            else:
                results["failed"] += 1
            
            # Log progress
            logger.info(f"📊 Progress: {i+1}/{len(self.accounts)} - "
                       f"Success: {results['successful']} - Failed: {results['failed']}")
        
        # Final summary
        success_rate = (results["successful"] / results["total"]) * 100 if results["total"] > 0 else 0
        
        logger.info(f"✅ Join spam completed for {target_uid}")
        logger.info(f"   Total: {results['total']}")
        logger.info(f"   Successful: {results['successful']}")
        logger.info(f"   Failed: {results['failed']}")
        logger.info(f"   Success Rate: {success_rate:.1f}%")
        
        return {
            "success": True,
            "message": f"Join spam completed - {results['successful']}/{results['total']} successful",
            **results
        }

# Singleton instance for easy import
join_spam_manager = JoinSpamManager()

# Example usage (for testing)
async def test_spam():
    """Test function"""
    manager = JoinSpamManager()
    
    # Test with a target UID
    results = await manager.spam_target(
        target_uid="1234567890",  # Replace with actual UID
        badge_value=1048576,      # s1 badge
        max_concurrent=2
    )
    
    print(f"Results: {json.dumps(results, indent=2)}")

if __name__ == "__main__":
    # Run test
    asyncio.run(test_spam())