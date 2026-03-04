from repo import UserRepository, RepoError, NotFoundError, UniqueViolationError


def parse_id(arg: str) -> int:
    if arg is None or arg.strip() == "":
        raise ValueError("id is required")

    try:
        value = int(arg)
    except ValueError:
        raise ValueError("id must be integer")

    if value <= 0:
        raise ValueError("id must be > 0")

    return value

def print_help() -> None:
    print(
        "Commands:\n"
        " help\n"
        " add\n"
        " list\n"
        " get <id>\n"
        " delete <id>\n"
        " update <id>\n"
        " search <text>\n"
        " exit"
    )

def print_user(user: dict):
    print(f"{user['id']}: {user['name']} | {user['phone']} | {user['city']}")

def print_users(users: list[dict]):
    if not users:
        print("empty")
        return
    for u in users:
        print_user(u)

dsn = "host=localhost port=5432 dbname=user_registry user=stepan password=newpassword"
repo = UserRepository(dsn)

def main() -> None:
    print("User Registry CLI (PostgreSQL). Type 'help' for commands.")
    while True:
        raw = input("> ").strip()
        if raw == "":
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            print_help()

        elif cmd == "list":
            try:
                users = repo.list_users()
                print_users(users)
            except RepoError as e:
                print(f"db error: {e}")

        elif cmd == "get":
            raw_id = args[0] if args else None

            try:
                user_id = parse_id(raw_id)
                user = repo.get_user(user_id)
                print_user(user)
            except ValueError as e:
                print(f"id error: {e}")
            except NotFoundError as e:
                print(f"user not found: {e}")
            except RepoError as e:
                 print(f"db error: {e}")

        elif cmd == "delete":
            raw_id = args[0] if args else None

            try:
                user_id = parse_id(raw_id)
                user = repo.delete_user(user_id)
                print_user(user)
            except ValueError as e:
                print(f"id error: {e}")
            except NotFoundError as e:
                print(f"user not found: {e}")
            except RepoError as e:
                print(f"db error: {e}")

        elif cmd == "add":
            name = input("Name: ").strip()
            if not name:
                print("input error: fields must not be empty")
                continue
            phone = input("Phone: ").strip()
            if not phone:
                print("input error: fields must not be empty")
                continue
            city = input("City: ").strip()
            if not city:
                print("input error: fields must not be empty")
                continue

            try:
                user = repo.add_user(name, phone, city)
                print_user(user)
            except UniqueVoilationError as e:
                print(f"phone already exists: {e}")
            except RepoError as e: print(f"db error: {e}")

        elif cmd == "update":
            raw_id = args[0] if args else None

            try:
                user_id = parse_id(raw_id)
                current = repo.get_user(user_id)

                new_name = input(f"Name [{current['name']}]: ").strip()
                new_phone =  input(f"Phone [{current['phone']}]: ").strip()
                new_city = input(f"City [{current['city']}]: ").strip()

                name = new_name or current["name"]
                phone = new_phone or current["phone"]
                city = new_city or current["city"]

                user = repo.update_user(user_id, name, phone, city)
                print_user(user)
            except ValueError as e:
                print(f"id error: {e}")
            except NotFoundError as e:
                print(f"user not found: {e}")
            except UniqueViolationError as e:
                print(f"phone already exists: {e}")
            except RepoError as e:
                print(f"db error: {e}")

        elif cmd == "search":
            text = ' '.join(args).strip()
            if not text:
                print("input error: fields must not be empty")
                continue
            try:
                users = repo.search_users(text)
                print_users(users)
            except RepoError as e:
                print(f"db error: {e}")


        elif cmd == "exit":
            print("bye")
            break
        else:
            print("unknown command")


if __name__ == "__main__":
    main()
