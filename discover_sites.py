from pathlib import Path

HOME = Path("/home/ilirbktk")

for item in HOME.iterdir():

    if not item.is_dir():
        continue

    wp = item / "wp-config.php"

    if wp.exists():

        print(
            item.name,
            item.absolute()
        )
