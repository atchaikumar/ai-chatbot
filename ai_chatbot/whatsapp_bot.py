from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transformers import pipeline
import time
import random

# --------- LOAD AI MODEL ----------
print("🧠 Loading AI brain...")
ai = pipeline("text-generation", model="distilgpt2")
print("✅ AI Ready")

# --------- CHROME PROFILE ----------
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\whatsapp_bot_profile")
chrome_options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")

# --------- PRIVACY POPUP ----------
try:
    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button//span[text()='OK']"))
    )
    ok_button.click()
except:
    pass

print("⏳ Waiting for WhatsApp Web...")
time.sleep(20)
print("✅ Ready")

last_messages = {}
memory = {}

# --------- HUMAN TYPING ----------
def human_type(box, text):
    for char in text:
        box.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
    box.send_keys(Keys.ENTER)

# --------- AI THINKING ----------
def ai_reply(user_msg, name):
    history = memory.get(name, "")
    prompt = f"Conversation:\n{history}\nFriend: {user_msg}\nBot:"
    result = ai(prompt, max_length=50, num_return_sequences=1)
    reply = result[0]["generated_text"].split("Bot:")[-1].strip()
    memory[name] = history + f"\nFriend: {user_msg}\nBot: {reply}"
    return reply

# --------- BOT LOOP ----------
while True:
    try:
        chats = driver.find_elements(By.XPATH, "//div[@role='row']")

        for chat in chats[:5]:
            chat.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//footer//div[@contenteditable='true']")
                )
            )

            name = driver.find_element(
                By.XPATH, "//header//span[@dir='auto']")
            name = name.text

            messages = driver.find_elements(
                By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='auto']"
            )

            if not messages:
                continue

            last_msg = messages[-1].text

            if last_messages.get(name) == last_msg:
                continue

            last_messages[name] = last_msg

            print(f"🧠 Thinking for {name}...")

            reply = ai_reply(last_msg, name)

            box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//footer//div[@contenteditable='true']")
                )
            )

            box.click()
            human_type(box, reply)

            print(f"✅ AI replied to {name}")
            time.sleep(2)

        time.sleep(4)

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(5)
