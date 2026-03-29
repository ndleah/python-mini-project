import time    # for countdown
import sys     # for command line arguments
import os      # for clearing the screen

# default timer settings (in minutes)
WORK_TIME = 25
SHORT_BREAK = 5
LONG_BREAK = 15
SESSIONS_BEFORE_LONG_BREAK = 4


def clear_screen():
    """clear the terminal screen"""
    # "cls" on windows, "clear" on mac/linux
    os.system("cls" if os.name == "nt" else "clear")


def format_time(seconds):
    """turn seconds into MM:SS format"""
    mins = seconds // 60
    secs = seconds % 60
    return str(mins).zfill(2) + ":" + str(secs).zfill(2)


def countdown(minutes, label):
    """run a countdown timer and show it in the terminal"""
    total_seconds = minutes * 60

    print("\n" + label)
    print("=" * 30)

    while total_seconds > 0:
        # show the time remaining
        print("\r  Time left: " + format_time(total_seconds), end="", flush=True)
        time.sleep(1)
        total_seconds -= 1

    # timer finished
    print("\r  Time left: 00:00")
    print("\nDone!")

    # make a beep sound to alert the user
    # \a is the bell character, works on most terminals
    print("\a")


def run_pomodoro(work, short_brk, long_brk, total_rounds):
    """run the full pomodoro cycle"""

    clear_screen()
    print("=" * 30)
    print("  POMODORO TIMER")
    print("=" * 30)
    print("")
    print("  Work:        " + str(work) + " min")
    print("  Short break: " + str(short_brk) + " min")
    print("  Long break:  " + str(long_brk) + " min")
    print("  Sessions:    " + str(total_rounds))
    print("")

    session = 1

    while session <= total_rounds:
        # work session
        input("Press Enter to start session " + str(session) + "/" + str(total_rounds) + "...")
        clear_screen()
        countdown(work, "Session " + str(session) + "/" + str(total_rounds) + " - WORK")

        # check if we're done
        if session == total_rounds:
            break

        # decide which break to take
        if session % SESSIONS_BEFORE_LONG_BREAK == 0:
            # every 4th session, take a long break
            input("\nPress Enter to start long break...")
            clear_screen()
            countdown(long_brk, "LONG BREAK - relax!")
        else:
            # normal short break
            input("\nPress Enter to start short break...")
            clear_screen()
            countdown(short_brk, "SHORT BREAK - stretch!")

        session += 1

    # all sessions done
    print("\n" + "=" * 30)
    print("  All " + str(total_rounds) + " sessions complete!")
    print("  Great work today!")
    print("=" * 30)


# --- main program starts here ---

if __name__ == "__main__":

    # let the user customize times from command line
    # usage: python pomodoro.py [work] [short_break] [long_break] [sessions]
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Pomodoro Timer")
        print("")
        print("Usage:")
        print("  python pomodoro.py                         # default (25/5/15, 4 sessions)")
        print("  python pomodoro.py 25 5 15 4               # custom times and sessions")
        print("  python pomodoro.py [work] [short] [long] [sessions]")
        print("")
        print("Arguments (all in minutes):")
        print("  work     - work session length (default: 25)")
        print("  short    - short break length (default: 5)")
        print("  long     - long break length (default: 15)")
        print("  sessions - number of work sessions (default: 4)")

    else:
        # read custom values or use defaults
        work = int(sys.argv[1]) if len(sys.argv) > 1 else WORK_TIME
        short_brk = int(sys.argv[2]) if len(sys.argv) > 2 else SHORT_BREAK
        long_brk = int(sys.argv[3]) if len(sys.argv) > 3 else LONG_BREAK
        rounds = int(sys.argv[4]) if len(sys.argv) > 4 else SESSIONS_BEFORE_LONG_BREAK

        try:
            run_pomodoro(work, short_brk, long_brk, rounds)
        except KeyboardInterrupt:
            # user pressed Ctrl+C to stop early
            print("\n\nTimer stopped. See you next time!")
