
import sys
import time
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.lvl = 1
        self.xp = 0
        self.xp_next = 30
        self.hp = 100
        self.max_hp = 100
        self.gold = 20
        self.shards = 0
        self.inv = ["Ration"]
        self.wpn = "Rusty Blade"
        self.atk_bonus = 0
        self.arm = "Cloth Rags"
        self.def_bonus = 0
        self.loc = "Nexus"

    def check_level(self):
        if self.xp >= self.xp_next:
            self.lvl += 1
            self.xp -= self.xp_next
            self.xp_next = int(self.xp_next * 1.5)
            self.max_hp += 20
            self.hp = self.max_hp
            print("\n🌟 LEVEL UP! 🌟")
            print(f"You reached Level {self.lvl}!")
            print(f"Max HP rose to {self.max_hp}!")

class Enemy:
    def __init__(self, name, hp, atk, gold, xp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.gold = gold
        self.xp = xp

class Game:
    def __init__(self):
        self.p = None
        self.running = True

    def pr(self, txt):
        for c in txt:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.005)
        print()

    def start(self):
        print("=" * 40)
        print("    A E T H E L G A R D :  U N B O U N D    ")
        print("=" * 40)
        name = input("\nEnter character name: ").strip()
        if not name: name = "Cipher"
        self.p = Player(name)
        
        while self.running:
            if self.p.hp <= 0:
                print("\n☠️ [YOU DIED] ☠️")
                print("The loop claims another soul.")
                break
            self.p.check_level()
            self.router()

    def router(self):
        loc = self.p.loc
        if loc == "Nexus": self.do_nexus()
        elif loc == "Shop": self.do_shop()
        elif loc == "Waste": self.do_waste()
        elif loc == "Vaults": self.do_vaults()
        elif loc == "Citadel": self.do_citadel()

    # --- REGION 0: HUB ZONE ---
    def do_nexus(self):
        print("\n" + "="*40)
        print(f"THE NEXUS HUB | Lvl {self.p.lvl}")
        print(f"HP: {self.p.hp}/{self.p.max_hp} | Gold: {self.p.gold}")
        print(f"Wpn: {self.p.wpn} | Arm: {self.p.arm}")
        print("="*40)
        print(" 1. Visit Rift Merchant")
        print(" 2. Enter Region I: Obsidian Waste")
        print(" 3. Enter Region II: Sunken Vaults")
        print(" 4. Enter Region III: Chronos Citadel")
        print(" 5. Consume a Ration (+30 HP)")
        
        ch = input("\nAction: ").strip()
        if ch == "1": self.p.loc = "Shop"
        elif ch == "2": self.p.loc = "Waste"
        elif ch == "3": self.p.loc = "Vaults"
        elif ch == "4": self.p.loc = "Citadel"
        elif ch == "5":
            if "Ration" in self.p.inv:
                self.p.inv.remove("Ration")
                self.p.hp = min(self.p.max_hp, self.p.hp + 30)
                print("\n[+] Ate ration. Healed 30 HP.")
            else:
                print("\n[-] You have no rations left!")

    # --- ECONOMY / ECONOMY HUB ---
    def do_shop(self):
        print("\n" + "-"*40)
        print(f"RIFT MERCHANT | Your Gold: {self.p.gold}")
        print("-"*40)
        print(" 1. Laser Edge (Wpn)  | Cost: 30g (+8 Atk)")
        print(" 2. Plasma Plate (Arm)| Cost: 40g (+5 Def)")
        print(" 3. Bio-Ration (Heal) | Cost: 10g")
        print(" 4. Return to Nexus")
        
        ch = input("\nBuy item number: ").strip()
        if ch == "1":
            if self.p.gold >= 30:
                self.p.gold -= 30
                self.p.wpn = "Laser Edge"
                self.p.atk_bonus = 8
                print("\n[+] Purchased Laser Edge!")
            else: print("\n[-] Insufficient gold!")
        elif ch == "2":
            if self.p.gold >= 40:
                self.p.gold -= 40
                self.p.arm = "Plasma Plate"
                self.p.def_bonus = 5
                print("\n[+] Purchased Plasma Plate!")
            else: print("\n[-] Insufficient gold!")
        elif ch == "3":
            if self.p.gold >= 10:
                self.p.gold -= 10
                self.p.inv.append("Ration")
                print("\n[+] Added Ration to inventory.")
            else: print("\n[-] Insufficient gold!")
        elif ch == "4":
            self.p.loc = "Nexus"

    # --- REGION I: LEVELING GROUND ---
    def do_waste(self):
        print("\n" + "-"*40)
        self.pr("REGION I: THE OBSIDIAN WASTE")
        self.pr("Low-level ash storms cover the terrain.")
        print("-"*40)
        print(" 1. Scout for Ash Scavengers (Lvl 1)")
        print(" 2. Return to the Nexus Hub")
        
        ch = input("\nChoice: ").strip()
        if ch == "1":
            e = Enemy("Ash Scavenger", hp=35, atk=8, gold=15, xp=15)
            self.combat(e)
        elif ch == "2":
            self.p.loc = "Nexus"

    # --- REGION II: MID GAME ---
    def do_vaults(self):
        print("\n" + "-"*40)
        self.pr("REGION II: THE SUNKEN VAULTS")
        self.pr("Automated factory traps click in the dark.")
        print("-"*40)
        print(" 1. Raid Sentry Assembly Line (Lvl 3)")
        print(" 2. Search for the Chronos Key Component")
        print(" 3. Return to the Nexus Hub")
        
        ch = input("\nChoice: ").strip()
        if ch == "1":
            e = Enemy("Scrap Drone", hp=65, atk=14, gold=25, xp=30)
            self.combat(e)
        elif ch == "2":
            if "Key Component" in self.p.inv:
                print("\n[!] Already cleared this vault!")
            else:
                e = Enemy("Vault Vault Security", hp=80, atk=18, gold=50, xp=50)
                if self.combat(e):
                    self.p.inv.append("Key Component")
                    print("\n🎉 Found the Chronos Key Component!")
        elif ch == "3":
            self.p.loc = "Nexus"

    # --- REGION III: ENDGAME ---
    def do_citadel(self):
        print("\n" + "#"*40)
        self.pr("REGION III: THE CHRONOS CITADEL")
        self.pr("The focal point of the timeline breakdown.")
        print("#"*40)
        print(" 1. Fight Temple Guardians (Lvl 5)")
        print(" 2. Open Core Room (Requires Key Component)")
        print(" 3. Return to the Nexus Hub")
        
        ch = input("\nChoice: ").strip()
        if ch == "1":
            e = Enemy("Timeless Zealot", hp=110, atk=24, gold=40, xp=60)
            self.combat(e)
        elif ch == "2":
            if "Key Component" in self.p.inv:
                self.boss_fight()
            else:
                self.pr("\n[-] The master gates are sealed tight.")
                self.pr("Find the Key Component in the Vaults.")
                input("\nPress Enter...")
        elif ch == "3":
            self.p.loc = "Nexus"

    # --- THE MODULAR BATTLE CORE ---
    def combat(self, e):
        print(f"\n💥 COMBAT: {e.name} appears! 💥")
        while e.hp > 0 and self.p.hp > 0:
            print(f"\n[{self.p.name} HP: {self.p.hp}/{self.p.max_hp}] | [{e.name} HP: {e.hp}/{e.max_hp}]")
            print(" 1. Basic Strike")
            print(" 2. High-Risk Flux")
            act = input("Select Action: ").strip()
            
            if act == "1":
                d = random.randint(10, 16) + self.p.atk_bonus
                e.hp -= d
                print(f"-> Hit {e.name} for {d} damage.")
            elif act == "2":
                if random.random() > 0.4:
                    d = random.randint(22, 32) + self.p.atk_bonus
                    e.hp -= d
                    print(f"-> CRITICAL FLUX! Dealt {d} damage!")
                else:
                    self.p.hp -= 8
                    print("-> GLITCH! Backfire dealt 8 damage to you.")
            
            if e.hp > 0:
                ed = max(2, random.randint(5, e.atk) - self.p.def_bonus)
                self.p.hp -= ed
                print(f"<- {e.name} counterstrikes for {ed} damage.")
                
        if self.p.hp > 0:
            print(f"\n🏆 VICTORY over {e.name}! 🏆")
            self.p.gold += e.gold
            self.p.xp += e.xp
            print(f"Earned: +{e.gold}g | +{e.xp} XP")
            return True
        return False

    # --- FINAL BOSS ENGINE ---
    def boss_fight(self):
        print("\n" + "#"*40)
        self.pr("FINAL BOSS: CHRONOS OVERLORD")
        print("#"*40)
        e = Enemy("The Chronos Overlord", hp=220, atk=32, gold=0, xp=0)
        
        if self.combat(e):
            print("\n" + "="*40)
            self.pr("The Core machine falls silent.")
            self.pr("The timeline anchors lock perfectly.")
            self.pr("The world is permanently saved!")
            print("="*40)
            self.running = False
        else:
            self.running = False

if __name__ == "__main__":
    engine = Game()
    engine.start()
