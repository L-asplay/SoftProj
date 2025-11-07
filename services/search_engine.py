from models.record import Record
from services.record_service import RecordService

class SearchEngine:
    """搜索引擎"""
    def __init__(self):
        self.record_service = RecordService()

    def fuzzy_search(self, user_id: str, keyword: str) -> list[Record]:
        """关键词模糊搜索（匹配描述、分类）"""
        all_records = self.record_service.get_records(user_id=user_id)
        keyword = keyword.lower()
        return [
            record for record in all_records
            if keyword in record.description.lower() or keyword in record.category.lower()
        ]

    def advanced_search(self, user_id: str, **filters) -> list[Record]:
        """高级搜索（支持多条件组合）"""
        return self.record_service.get_records(user_id=user_id, **filters)