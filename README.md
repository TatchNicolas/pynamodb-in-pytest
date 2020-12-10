# PynamoDB and DynamoDB Local in Pytest

PynamoDB requires some parameters in metaclass of its models which are in fact irrelevant when running tests with [DynamoDB Local](https://hub.docker.com/r/amazon/dynamodb-local).

This repo shows a small trick to avoid having unnecessary if clauses in PynamoDB model definition by using Python's built-in `setattr` function.

```python
@pytest.fixture(scope="function")
def user_repo() -> Iterable[UserRepo]:

    repo: UserRepo = UserRepo()

    model_meta_class = getattr(repo.model, "Meta")
    setattr(model_meta_class, "table_name", "user_table_for_test")
    setattr(model_meta_class, "host", DDB_LOCAL_HOST)
    setattr(model_meta_class, "billing_mode", "PAY_PER_REQUEST")
    # or
    # setattr(model_meta_class, "read_capacity_units", 1)
    # setattr(model_meta_class, "write_capacity_units", 1)
```

### See it in action

```bash
docker-compose up -d
docker-compose exec app pytest
```
