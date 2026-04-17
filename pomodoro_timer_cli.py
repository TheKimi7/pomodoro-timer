# pomodoro timer with themed CLI interface
# created by Aunam.

import time

# TO ALWAYS GET VALID INPUT

def get_valid_input(prompt, valid_options):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_options:
                return choice
            else:
                print(f"\n\n‼️- invalid option. choose from {valid_options}!")
        except ValueError:
            print("\n\n⚠️- option must be an integer. try again.")


def get_yes_no(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ["y", "yes"]:
            return "y"
        elif choice in ["n", "no"]:
            print("see you soon someday else! ^^")
            return "n"
        else:
            print("\n\n‼️- please enter y/n or yes/no.")

# THEME MENU FOR POMODORO

def uilook():
    ui_look = get_valid_input("""\nwhat kind of theme would you prefer?\n
                              1. classic pomodoro 🕰️
                              2. soft and dreamy study 🌸
                              3. cozy desk energy 🎧
                              4. late night coder 🌙
                              5. focus + productive 🌿
                              6. monochrome / minimalistic 🖥️
    
                              your preference (1/2/3/4/5/6): """, [1,2,3,4,5,6])

    if ui_look == 1:
        classic_pomodoro()
    elif ui_look == 2:
        soft_pomodoro()
    elif ui_look == 3:
        cozy_desk_pomodoro()
    elif ui_look == 4:
        late_night_pomodoro()
    elif ui_look == 5:
        focus_pomodoro()
    elif ui_look == 6:
        monochrome_pomodoro()


# CORE TIMER

def default_timer(minutes, break_minutes, sesh_emoji, focus_emoji, break_emoji):
    minutes = minutes * 60
    break_minutes = break_minutes * 60
    continue_option = 'y'

    while continue_option == 'y':

        while True:
            try:
                sessions = int(input(f"{sesh_emoji}; how many sessions are we doing today?: "))
                break
            except ValueError:
                print("\n⚠️- invalid answer :( try again! ")

        for session in range(sessions):
            print(f"\nsession {session + 1} of {sessions}")
            print("\ngrab your belongings! books, headphones, pencils, pens and lock in! ♡")

            for i in range(10, 0, -1):
                print(f"{i:02}")
                time.sleep(1)

            print("good luck for your session! you got this ✫\n")

            # STUDY
            print(f"{focus_emoji}: focus session started! 𝜗𝜚")
            for seconds in range(minutes, 0, -1):
                mins_display = seconds // 60
                secs_display = seconds % 60
                print(f"\r{mins_display:02}:{secs_display:02}", end="", flush=True)
                time.sleep(1)

            # BREAK
            print(f"\n\n\t\t{break_emoji} break time! don't vanish pls")
            for seconds in range(break_minutes, 0, -1):
                mins_display = seconds // 60
                secs_display = seconds % 60
                print(f"\r{mins_display:02}:{secs_display:02}", end="", flush=True)
                time.sleep(1)

        print("\n\t\t✏️; all done! proud of you ♡")
        continue_option = get_yes_no("\n\n--> do you wish to continue? y/n: ")


# TIMER STATEMENTS

def choose_timer():
    return get_valid_input("""\n\n[⌛] choose your preferred timer:\n
                           1. 25 minutes work, 5 minutes break
                           2. 30 minutes work, 5 minutes break
                           3. 50 minutes work, 10 minutes break
                           4. custom
                           
                           --> choose (1/2/3/4): """, [1,2,3,4])


# THEMES

def classic_pomodoro():
    print("\n\t🍅 welcome to pomodoro timer!")

    timer = choose_timer()

    if timer == 1:
        default_timer(25,5,"⏰","📖","✅")
    elif timer == 2:
        default_timer(30,5,"⏰","📖","✅")
    elif timer == 3:
        default_timer(50,10,"⏰","📖","✅")
    elif timer == 4:
        c_time_custom()


def soft_pomodoro():
    print("\n\t🌸 soft cozy study mode, get yourself ready to grind!")

    timer = choose_timer()

    if timer == 1:
        default_timer(25,5,"🎀","🧸","🌷")
    elif timer == 2:
        default_timer(30,5,"🎀","🧸","🌷")
    elif timer == 3:
        default_timer(50,10,"🎀","🧸","🌷")
    elif timer == 4:
        c_time_custom()


def focus_pomodoro():
    print("\n\t⚡ focus mode. no excuses diva!")

    timer = choose_timer()

    if timer == 1:
        default_timer(25,5,"🌿","🧠","🌱")
    elif timer == 2:
        default_timer(30,5,"🌿","🧠","🌱")
    elif timer == 3:
        default_timer(50,10,"🌿","🧠","🌱")
    elif timer == 4:
        c_time_custom()


def late_night_pomodoro():
    print("\n\t🌙 late night grind time. build what you dream of, the future is yours tonight. ^^")

    timer = choose_timer()

    if timer == 1:
        default_timer(25,5,"🌙","🍵","💻")
    elif timer == 2:
        default_timer(30,5,"🌙","🍵","💻")
    elif timer == 3:
        default_timer(50,10,"🌙","🍵","💻")
    elif timer == 4:
        c_time_custom()


def cozy_desk_pomodoro():
    print("\n\t☕ cozy desk vibes loading... try not to fall asleep! get your caffeine!")

    timer = choose_timer()

    if timer == 1:
        default_timer(25,5,"🍪","🎧","📓")
    elif timer == 2:
        default_timer(30,5,"🍪","🎧","📓")
    elif timer == 3:
        default_timer(50,10,"🍪","🎧","📓")
    elif timer == 4:
        c_time_custom()


def monochrome_pomodoro():
    print("\n\t🤍 minimal mode activated, now it's your time, seize it!")

    timer = choose_timer()

    if timer == 1:
        default_timer(25,5,"🤍","🖥️","✦")
    elif timer == 2:
        default_timer(30,5,"🤍","🖥️","✦")
    elif timer == 3:
        default_timer(50,10,"🤍","🖥️","✦")
    elif timer == 4:
        c_time_custom()


# CUSTOM TIMER

def c_time_custom():

    while True:
        try:
            print("\nyour study time settings!")
            study_hours = int(input("\tstudy hours: "))
            study_minutes = int(input("\tstudy minutes: "))
            study_seconds = int(input("\tstudy seconds: "))
            break
        except ValueError:
            print("⚠️: invalid answer, try again! ")

    total_study_seconds = study_hours*3600 + study_minutes*60 + study_seconds

    while True:
        try:
            print("\nyour break time settings!")
            break_hours = int(input("\tbreak hours: "))
            break_minutes = int(input("\tbreak minutes: "))
            break_seconds = int(input("\tbreak seconds: "))
            break
        except ValueError:
            print("⚠️: invalid answer, try again! \n")

    total_break_seconds = break_hours*3600 + break_minutes*60 + break_seconds

    continue_option = 'y'

    while continue_option == 'y':

        while True:
            try:
                sessions = int(input("\n⏰: number of sessions? "))
                break
            except ValueError:
                print("⚠️- invalid answer. enter a number! ")

        for session in range(sessions):
            print(f"\nsession {session + 1} of {sessions}")
            print("\nthis is your moment, don't give up!")

            for i in range(10,0,-1):
                print(f"{i:02}")
                time.sleep(1)

            print("go!\n")

            for seconds in range(total_study_seconds,0,-1):
                h = seconds//3600
                m = (seconds%3600)//60
                s = seconds%60
                print(f"\r{h:02}:{m:02}:{s:02}", end="", flush=True)
                time.sleep(1)

            print("\nbreak time; don't scroll into another dimension >_<")
            for seconds in range(total_break_seconds,0,-1):
                h = seconds//3600
                m = (seconds%3600)//60
                s = seconds%60
                print(f"\r{h:02}:{m:02}:{s:02}", end="", flush=True)
                time.sleep(1)

        continue_option = get_yes_no("\n lock in again? y/n: ")


if __name__ == "__main__":
    uilook()
