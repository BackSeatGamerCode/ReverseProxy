DEFAULT_PLUGIN = """\
def on_start():
    print("Start")


def on_close():
    print("Close")


def on_command(command, name, guest):
    print("Command", command, name, guest)


def on_console_clear():
    print("Console Cleared")


def on_rewards_pull(rewards):
    print("Rewards Updated")
"""