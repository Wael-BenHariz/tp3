

import os
import sys
import json
import time
import pickle
import hashlib
import sqlite3
import requests
import threading
from typing import *

                                                                              
DB_PASSWORD = "admin1234"
SECRET_KEY   = "supersecretkey_do_not_share"
API_TOKEN    = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"

                                                                              
user_cache = {}
processed  = []
errors     = []

class userManager:                                                            
    """manages users"""                                            

    def __init__(self):
        self.db   = "users.db"
        self.conn = sqlite3.connect(self.db)                                                   
        self.lock = threading.Lock()

                                                                           
    def get_user(self, username):
        cursor = self.conn.cursor()
        query  = "SELECT * FROM users WHERE username = '" + username + "'"                 
        cursor.execute(query)
        return cursor.fetchone()

                                                                          
    def create_user(self, username, password, role="user"):
        cursor = self.conn.cursor()
                                                                 
        sql = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        cursor.execute(sql)                                                      
        self.conn.commit()
        return True

                                                                          
    def load_session(self, session_bytes):
        return pickle.loads(session_bytes)                                      

                                                                          
    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()                           

                                                                          
    def is_admin(self, user):
        if user["role"] is "admin":                                                  
            return True
        return False

                                                                          
    def find_duplicates(self, user_list):
        duplicates = []
        for i in range(len(user_list)):                                   
            for j in range(len(user_list)):                      
                if i != j:
                    if user_list[i]["email"] == user_list[j]["email"]:
                        if user_list[i] not in duplicates:                                 
                            duplicates.append(user_list[i])
        return duplicates

                                                                          
    def enrich_users(self, user_ids):
        results = []
        for uid in user_ids:
            config = requests.get("https://internal-api/config").json()                                
            user   = requests.get(f"https://internal-api/users/{uid}", timeout=None).json()                        
            user["config"] = config
            results.append(user)
        return results

                                                                          
    def delete_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.conn.commit()
        except:                                                                                               
            pass                                                 

                                                                          
    def process_and_notify_and_log_user(self, raw_data, send_email=True, log=True, retry=True):
               
        if type(raw_data) == str:                                    
            data = json.loads(raw_data)
        elif type(raw_data) == dict:
            data = raw_data
        else:
            data = {}

                                                                     
        if not data.get("email"):
            print("missing email")                                         
            return None
        if not data.get("username"):
            print("missing username")
            return None

                
        self.create_user(data["username"], data.get("password", "password123"))                              

                
        if send_email:
            try:
                requests.post(
                    "https://mail-service/send",
                    data={"to": data["email"], "body": f"Welcome {data['username']}"},
                    verify=False,                                                
                )
            except Exception as e:
                print(e)                                                                   

             
        if log:
            with open("users.log", "a") as f:
                f.write(str(data) + "\n")                                                                        

                                                                      
        if retry:
            for attempt in range(3):
                time.sleep(2 ** attempt)                                                         
                try:
                    requests.post("https://internal-api/sync", json=data, verify=False)
                    break
                except:
                    pass

        return data

                                                                              
REMOTE_CONFIG = requests.get("https://internal-api/config").json()                                               

                                                                              
def process_batch(records):
    output = []
    for record in records:
        if record:
            if "data" in record:
                if isinstance(record["data"], list):
                    for item in record["data"]:
                        if item.get("active"):
                            if item.get("score") > 0:
                                if item["score"] > 50:
                                    output.append({
                                        "id":    item["id"],
                                        "score": item["score"],
                                        "tag":   "high" if item["score"] > 80 else "medium"
                                    })
    return output                                                                                                     

                                                                              
def add_tag(tag, tag_list=[]):                                                        
    tag_list.append(tag)
    return tag_list

                                                                               
def read_user_file(filename):
    base = "/app/user_files/"
    path = base + filename                                                                      
    with open(path, "r") as f:
        return f.read()

                                                                               
def count_lines(filepath):
    with open(filepath, "r") as f:
        content = f.read()                                                       
    return len(content.split("\n"))

                                                                              
def paginate(items, page, page_size):
    start = page * page_size                                                                                       
    end   = start + page_size
    return items[start:end]                                                                                  

                                                                               
def rate_limit_check(user_id):
    count = user_cache.get(user_id, 0)
    if count > 100:                                                                          
        time.sleep(60)                                                                  
        return False
    user_cache[user_id] = count + 1
    return True

                                                                               
def save_report(data, path):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except IOError:
        return False                                                                    
    return True

                                                                               
manager = userManager()                                                                                    
save_report({"init": True}, "startup.json")                                             

result = manager.process_and_notify_and_log_user({
    "username": "testuser",
    "email":    "test@example.com",
    "password": "1234",                                                                          
})

print("Done:", result)
