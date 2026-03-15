import sys

# --- CTF CONFIGURATION ---
_HIDDEN_FLAG = "4354467b63306e67723474735f7930755f6630756e645f31747d"
FLAG = bytes.fromhex(_HIDDEN_FLAG).decode('utf-8')

KEY = "OPEN"
# Auto-generate the hex string using XOR 
ENCRYPTED_HEX = "".join([f"{ord(FLAG[i]) ^ ord(KEY[i % len(KEY)]):02x}" for i in range(len(FLAG))])

# --- GAME DATA & LORE ---
rooms = {
    "atrium": {
        "name": "The Atrium",
        "description": "The front door's smart-lock glows angry red: [LOCKDOWN ACTIVE]. The biometric scanner is disabled. Paths lead NORTH to the Living Room.",
        "exits": {"north": "living_room"},
        "items": {}
    },
    "living_room": {
        "name": "Living Room",
        "description": "A pristine, minimalist room. An offline [vacuum] robot is stuck in the corner. Paths lead NORTH to the Kitchen, EAST to the Bedroom, WEST to the Utility Closet, and SOUTH back to the Atrium.",
        "exits": {"north": "kitchen", "east": "bedroom", "west": "utility", "south": "atrium"},
        "items": {
            "vacuum": "It's a Roomba. Stuck under the sofa. You check its dustbin, but there's nothing useful."
        }
    },
    "kitchen": {
        "name": "Kitchen",
        "description": "Stainless steel appliances everywhere. The smart [fridge] has a massive digital display currently showing the family calendar.",
        "exits": {"south": "living_room"},
        "items": {
            "fridge": "The digital calendar shows only one upcoming event:\n'Home Security PIN reset day. Same as the year we bought the house: 2018.'"
        }
    },
    "bedroom": {
        "name": "Master Bedroom",
        "description": "The smart blinds are tightly shut. Hidden behind a sliding mirror is a digital wall [safe]. It requires a 4-digit PIN.",
        "exits": {"west": "living_room"},
        "items": {
            "safe": "A high-tech wall safe. Type 'open safe <code>' to attempt access."
        }
    },
    "utility": {
        "name": "Utility Closet",
        "description": "The nerve center of the house. Network cables route into a central home [smarthub]. A terminal screen is blinking.",
        "exits": {"east": "living_room"},
        "items": {
            "smarthub": f"AURA SmartHub Terminal.\n[WARNING: NETWORK COMPROMISED]\nEmergency Override Cipher:\n{ENCRYPTED_HEX}\n\nUse 'decrypt <hex> <key>' to restore network."
        }
    }
}

# --- GAME STATE ---
current_room = "atrium"
safe_open = False

# --- ENGINE FUNCTIONS ---
def look():
    room = rooms[current_room]
    print(f"\n--- {room['name']} ---")
    print(room["description"])

def go(direction):
    global current_room
    room = rooms[current_room]
    if direction in room["exits"]:
        current_room = room["exits"][direction]
        print(f"You walk {direction}.")
        look()
    else:
        print(f"You can't go '{direction}'. Available exits: {', '.join(room['exits'].keys())}")

def examine(target):
    room = rooms[current_room]
    if "items" in room and target in room["items"]:
        if target == "safe" and safe_open:
            print("The safe is open. Inside is a titanium backup drive with a label:\n'AURA OVERRIDE KEY: OPEN'")
        else:
            print(room["items"][target])
    else:
        print(f"You don't see '{target}' here.")

def open_item(target, code):
    global safe_open
    if current_room == "bedroom" and target == "safe":
        if code == "2018":
            print(">> BEEP. The safe door swings open.")
            safe_open = True
            examine("safe")
        else:
            print(">> BZZZT. Incorrect PIN.")
    else:
        print(f"You can't open '{target}' here or missing code.")

def decrypt(hex_str, user_key):
    try:
        ciphertext = bytes.fromhex(hex_str)
        key_bytes = user_key.upper().encode('utf-8')
        
        decrypted = bytearray()
        for i in range(len(ciphertext)):
            decrypted.append(ciphertext[i] ^ key_bytes[i % len(key_bytes)])
            
        decoded_text = decrypted.decode('utf-8')
        
        if decoded_text == FLAG:
            print("\n═══════════════════════════════════════════")
            print("          LOCKDOWN OVERRIDE ACCEPTED       ")
            print("═══════════════════════════════════════════")
            print("The front door mechanism clicks loudly.")
            print("You are free to leave.")
            print(f"\n  FLAG: {decoded_text}")
            print("═══════════════════════════════════════════")
            sys.exit(0)
        else:
            print(">> ERROR: Decryption failed. Incorrect key or cipher.")
            
    except ValueError:
        print(">> ERROR: Invalid hex string provided.")
    except Exception:
        print(">> ERROR: System fault during decryption.")

# --- MAIN LOOP ---
def main():
    print(r"""
  ____  __  __    _    ____ _____ 
 / ___||  \/  |  / \  |  _ \_   _|
 \___ \| |\/| | / _ \ | |_) || |  
  ___) | |  | |/ ___ \|  _ < | |  
 |____/|_|  |_/_/   \_\_| \_\|_|  
                                  
  _   _  ___  __  __ _____        
 | | | |/ _ \|  \/  | ____|       
 | |_| | | | | |\/| |  _|         
 |  _  | |_| | |  | | |___        
 |_| |_|\___/|_|  |_|_____|       
                                  
    OS - VERSION 2.1
    """)
    print("LOCKDOWN PROTOCOL INITIATED. UNAUTHORIZED USER DETECTED.")
    print("════════════════════════════════════════════════════════════")
    print("MISSION BRIEFING:")
    print("You are trapped inside a hyper-modern, automated smart home. ")
    print("The central AI has gone rogue and locked all external doors. ")
    print("To escape, you must explore the rooms, piece together the ")
    print("family's digital footprint, and decrypt the mainframe override.")
    print("════════════════════════════════════════════════════════════")
    print("Type 'help' for available commands.")
    look()

    while True:
        try:
            sys.stdout.flush() 
            command_input = input("\n> ").lower().strip().split()
            
            if not command_input:
                continue
                
            action = command_input[0]
            args = command_input[1:]

            if action == "look":
                look()
            elif action == "go" and len(args) == 1:
                go(args[0])
            elif action == "examine" and len(args) > 0:
                examine(" ".join(args))
            elif action == "open" and len(args) == 2:
                open_item(args[0], args[1])
            elif action == "decrypt" and len(args) == 2:
                decrypt(args[0], args[1])
            elif action == "help":
                print("Available commands:")
                print("  look              - Describe current room")
                print("  go <direction>    - Move (north/south/east/west)")
                print("  examine <item>    - Inspect an item")
                print("  open <item> <code>- Try a PIN code on an item")
                print("  decrypt <hex> <key>- Input override cipher to SmartHub")
                print("  quit              - Exit terminal")
            elif action in ["quit", "exit"]:
                print("You remain trapped in the Smart Home. Goodbye.")
                sys.exit(0)
            else:
                print("Unknown command or missing arguments. Type 'help'.")
                
        except (KeyboardInterrupt, EOFError):
            print("\nConnection lost...")
            sys.exit(0)

if __name__ == "__main__":
    main()
