from os import environ

from app.repository import UserRepo


DDB_LOCAL_HOST = environ["DDB_LOCAL_HOST"]


if __name__ == "__main__":
    repo: UserRepo = UserRepo()

    model_meta_class = getattr(repo.model, "Meta")
    setattr(model_meta_class, "host", DDB_LOCAL_HOST)
    setattr(model_meta_class, "billing_mode", "PAY_PER_REQUEST")
    setattr(model_meta_class, "table_name", "user_table_for_dev")
    # or
    # setattr(model_meta_class, "read_capacity_units", 1)
    # setattr(model_meta_class, "write_capacity_units", 1)

    by_group_meta_class = getattr(repo.model.by_group, "Meta")
    setattr(by_group_meta_class, "host", DDB_LOCAL_HOST)

    repo.model.create_table(wait=True)
