from typing import Iterable
from os import environ

import pytest

from app.repository import UserRepo


DDB_LOCAL_HOST = environ["DDB_LOCAL_HOST"]


@pytest.fixture(scope="function")
def user_repo() -> Iterable[UserRepo]:

    repo: UserRepo = UserRepo()

    model_meta_class = getattr(repo.model, "Meta")
    setattr(model_meta_class, "host", DDB_LOCAL_HOST)
    setattr(model_meta_class, "table_name", "user_table_for_test")
    setattr(model_meta_class, "billing_mode", "PAY_PER_REQUEST")
    # or
    # setattr(model_meta_class, "read_capacity_units", 1)
    # setattr(model_meta_class, "write_capacity_units", 1)

    by_group_meta_class = getattr(repo.model.by_group, "Meta")
    setattr(by_group_meta_class, "host", DDB_LOCAL_HOST)

    repo.model.create_table(wait=True)

    yield repo
    # Delete table after running a test function
    # repo.model.delete_table()


def test_user_repo(user_repo: UserRepo) -> None:
    alice = user_repo.add_user(uid="001", name="Alice", group="Red")
    assert alice == {"uid": "001", "name": "Alice", "group": "Red"}

    bob = user_repo.add_user(uid="002", name="Bob", group="Blue")
    chris = user_repo.add_user(uid="003", name="Chris", group="Blue")

    users_in_red_group = user_repo.get_users_in_group(group="Blue")
    assert users_in_red_group == [bob, chris]
