# PynamoDB and DynamoDB Local in Pytest

PynamoDB requires some parameters in metaclass of its models which are in fact irrelevant when running tests with [DynamoDB Local](https://hub.docker.com/r/amazon/dynamodb-local).

This repo shows a small trick to avoid having unnecessary if clauses in PynamoDB model definition by using Python's built-in `setattr` function.

```python
@pytest.fixture(scope="function")
def user_repo() -> Iterable[UserRepo]:

    repo: UserRepo = UserRepo()

    model_meta_class = getattr(repo.model, "Meta")
    setattr(model_meta_class, "host", DDB_LOCAL_HOST)
    setattr(model_meta_class, "billing_mode", "PAY_PER_REQUEST")
    setattr(model_meta_class, "table_name", "user_table_for_test")
    # or
    # setattr(model_meta_class, "read_capacity_units", 1)
    # setattr(model_meta_class, "write_capacity_units", 1)

    by_group_meta_class = getattr(repo.model.by_group, "Meta")
    setattr(by_group_meta_class, "host", DDB_LOCAL_HOST)

    repo.model.create_table(wait=True)

    yield repo
    # Delete table after running a test function
    repo.model.delete_table()
```

### See it in action

```bash
docker-compose up -d
docker-compose exec app pytest
```
