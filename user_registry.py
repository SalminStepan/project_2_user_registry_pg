from repo import UserRepository, RepoError, NotFoundError, UniqueViolationError
import logging
import os

def create_repo() -> UserRepository:
    dsn = os.getenv("USER_REGISTRY_DSN")

    if not dsn:
        raise RuntimeError("USER_REGISTRY_DSN is not set")

    return UserRepository(dsn)

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

def handle_list(repo, args):
    if args:
        raise ValueError("list takes no arguments")
    users = repo.list_users()
    print_users(users)

def handle_get(repo, args):
    raw_id = args[0] if args else None
    user_id = parse_id(raw_id)
    user = repo.get_user(user_id)
    print_user(user)

def handle_delete(repo, args):
    raw_id = args[0] if args else None
    user_id = parse_id(raw_id)
    user = repo.delete_user(user_id)
    print_user(user)

def handle_add(repo, args):
    if args:
        raise ValueError("add takes no arguments")
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    city = input("City: ").strip()

    if not name or not phone or not city:
        raise ValueError("fields must not be empty")
    user = repo.add_user(name, phone, city)
    print_user(user)

def handle_update(repo, args):
    raw_id = args[0] if args else None
    user_id = parse_id(raw_id)

    current = repo.get_user(user_id)

    new_name = input(f"Name [{current['name']}]: ").strip()
    new_phone = input(f"Phone [{current['phone']}]: ").strip()
    new_city = input(f"City [{current['city']}]: ").strip()

    name = new_name or current["name"]
    phone = new_phone or current["phone"]
    city = new_city or current["city"]

    user = repo.update_user(user_id, name, phone, city)
    print_user(user)


def handle_search(repo, args):
    text = " ".join(args).strip()
    if not text:
        raise ValueError("search text is required")
    users = repo.search_users(text)
    print_users(users)

def handle_help(repo, args):
    if args:
        raise ValueError("help takes no arguments")
    print_help()

def setup_logging() -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger("user_registry")


def main() -> None:
    logger = setup_logging()
    logger.info("starting CLI")

    print("User Registry CLI (PostgreSQL). Type 'help' for commands.")
    commands = {
        "list": handle_list,
        "get": handle_get,
        "delete": handle_delete,
        "add": handle_add,
        "update": handle_update,
        "search": handle_search,
        "help": handle_help,
    }


    dsn = os.getenv("USER_REGISTRY_DSN")

    if not dsn:
        print("config error: set USER_REGISTRY_DSN environment variable")
        return

    repo = create_repo()

    while True:
        raw = input("> ").strip()
        if raw == "":
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "exit":
            logger.info("exit")
            print("bye")
            break

        handler = commands.get(cmd)

        if not handler:
            print("Unknown command")
            continue

        try:
            handler(repo, args)

        except ValueError as e:
            logger.info("command: %s args=%s", cmd, args)
            print(f"input error: {e}")

        except NotFoundError as e:
            logger.info("command: %s args=%s", cmd, args)
            print(f"user not found: {e}")

        except UniqueViolationError as e:
            logger.info("command: %s args=%s", cmd, args)
            print(f"phone already exists: {e}")

        except RepoError as e:
            logger.info("command: %s args=%s", cmd, args)
            print(f"db error: {e}")
if __name__ == "__main__":
    main()
