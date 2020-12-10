from pynamodb.models import Model

from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from app.config import USER_TABLE_NAME


class _ByGroup(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()

    group: UnicodeAttribute = UnicodeAttribute(hash_key=True)
    uid: UnicodeAttribute = UnicodeAttribute(range_key=True)


class _UserModel(Model):
    class Meta:
        table_name = USER_TABLE_NAME

    uid: UnicodeAttribute = UnicodeAttribute(hash_key=True)
    name: UnicodeAttribute = UnicodeAttribute()
    group: UnicodeAttribute = UnicodeAttribute()

    by_group: GlobalSecondaryIndex = _ByGroup()


class UserRepo:
    def __init__(self) -> None:
        self.model = _UserModel

    def add_user(self, uid: str, name: str, group: str) -> dict[str, str]:

        self.model(hash_key=uid, name=name, group=group).save()

        return {
            "uid": uid,
            "name": name,
            "group": group,
        }

    def get_user(self, uid: str) -> dict[str, str]:

        user = self.model.get(hash_key=uid)

        return {
            "uid": user.uid,
            "name": user.name,
            "group": user.group,
        }

    def get_users_in_group(self, group: str) -> list[dict[str, str]]:

        users = self.model.by_group.query(hash_key=group)
        return [
            {
                "uid": user.uid, # type: ignore
                "name": user.name, # type: ignore
                "group": user.group, # type: ignore
            }
            for user in users
        ]
