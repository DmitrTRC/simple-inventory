class ORM:
    def __init__(self):
        raise NotImplementedError

    def insert_item(self, table: str, data: dict):
        raise NotImplementedError

    def select_item(self):
        raise NotImplementedError

    def update_item(self):
        raise NotImplementedError

    def delete_item(self):
        raise NotImplementedError

    def fetch_one_item(self):
        raise NotImplementedError

    def fetch_all_items(self):
        raise NotImplementedError
