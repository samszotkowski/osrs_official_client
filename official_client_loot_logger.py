import os
import json
import re
from time import sleep
import sqlite3

db_path = rf"{os.getenv('LOCALAPPDATA')}/Jagex/Old School Runescape/users/CHANGE_ME/LootTracker.db"
output_loot_log_path = r"C:/CHANGE_ME/official_loot_logger.log"

# # TEST ZONE
# con = sqlite3.connect("file:" + db_path + "?mode=ro", uri=True)
# cursor = con.cursor()
# query = """
# SELECT * FROM dropLimit
# """
# for row in cursor.execute(query):
#     print(row)
# con.close()
# # TEST ZONE

if os.path.exists(output_loot_log_path):
    new_name = output_loot_log_path.replace(".log", "") + " (1)"
    new_log = new_name + ".log"

    pattern = r"\s+\(\d+\)$"
    num = 1
    while os.path.exists(new_log):
        num += 1
        new_name = re.sub(pattern, f" ({num})", new_name)
        new_log = new_name + ".log"

    print(f"WARNING: {output_loot_log_path} already exists. Data will instead go into {new_log}")
    output_loot_log_path = new_log

else:
    print(f"Writing logs to {output_loot_log_path}")

unique_ids = set()
while True:
    con = sqlite3.connect("file:" + db_path + "?mode=ro", uri=True)
    try:
        cursor = con.cursor()
        query = """
        SELECT sourceDrop.sourceName, sourceDrop.modified, sourceDrop.uniqueIdentifier, lootDrop.objectId, lootDrop.count FROM sourceDrop
        FULL OUTER JOIN lootDrop ON sourceDrop.sourceID = lootDrop.sourceID
        ORDER BY sourceDrop.modified ASC
        """
        new_ids = set()
        new_drops = {}
        for row in cursor.execute(query):
            name, timestamp, unique_id, object_id, count = row

            if unique_id not in unique_ids:
                new_ids.add(unique_id)
                drop = {
                    "unique_id": unique_id,
                    "name": name,
                    "timestamp": timestamp,
                    "drops": [{"id": object_id, "quantity": count}]
                }

                if unique_id not in new_drops:
                    new_drops[unique_id] = drop
                else:
                    new_drops[unique_id]["drops"].append({"id": object_id, "quantity": count})

        with open(output_loot_log_path, "at", encoding="utf-8") as file:
            for drop in new_drops.values():
                print(drop)
                json.dump(drop, file)
                file.write("\n")

        unique_ids.update(new_ids)

        con.close()
        sleep(1)

    except KeyboardInterrupt:
        con.close()
        break
