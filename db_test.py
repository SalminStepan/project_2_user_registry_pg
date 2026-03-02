from repo import UserRepository, NotFoundError, UniqueViolationError

DSN = "host=localhost port=5432 dbname=user_registry user=stepan password=*****"
repo = UserRepository(DSN)

print("List:", repo.list_users())

try:
    print("Get999:", repo.get_user(999999))
except NotFoundError as e:
    print("NOT FOUND OK:", e)

try:
    print("Add exists:", repo.add_user("Ivan", "+77001234567", "Almaty"))
except UniqueViolationError as e:
    print("UNIQUE OK:", e)

try:
    print("Delete999:", repo.delete_user(999999))
except NotFoundError as e:
    print("DELETE NOT FOUND OK:", e)
