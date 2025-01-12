This script logs drops from the official client as they come in.

- You're meant to run this while you are playing the game.

- You can stop it with a keyboard interrupt (ctrl+c for example) or by killing the terminal, otherwise it will run forever.

- Change `db_path` at the top to be the path of your LootTracker.db. This should be at

  `%LOCALAPPDATA%/Jagex/Old School Runescape/users/A_BUNCH_OF_NUMBERS/LootTracker.db`

  where `A_BUNCH_OF_NUMBERS` is unique to each character you've logged in as. If you're not sure which character is the right one, kill a rat or something and look at the last modified date on that file.

- Change `output_loot_log_path` at the top to be the place you want your output log file to go.
  - If the file you put in there already exists, no big deal, it will create a new one with a number after it each time you run it.
