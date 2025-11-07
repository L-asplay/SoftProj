import json
import os
from datetime import datetime

class DBUtils:
    """本地数据库工具类（基于JSON文件存储）"""
    def __init__(self, db_path: str = "local_db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self) -> None:
        """初始化数据库目录和文件"""
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        
        # 初始化各数据表文件
        tables = ["users", "records", "categories"]
        for table in tables:
            file_path = self._get_table_path(table)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)

    def _get_table_path(self, table_name: str) -> str:
        """获取数据表文件路径"""
        return os.path.join(self.db_path, f"{table_name}.json")

    def get_all(self, table_name: str) -> list:
        """获取表中所有数据"""
        file_path = self._get_table_path(table_name)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_by_condition(self, table_name: str, condition: callable) -> list:
        """根据条件查询数据"""
        all_data = self.get_all(table_name)
        return [item for item in all_data if condition(item)]

    def insert(self, table_name: str, data: dict) -> bool:
        """插入数据"""
        file_path = self._get_table_path(table_name)
        all_data = self.get_all(table_name)
        all_data.append(data)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        return True

    def update(self, table_name: str, condition: callable, new_data: dict) -> bool:
        """更新数据"""
        file_path = self._get_table_path(table_name)
        all_data = self.get_all(table_name)
        updated = False
        
        for i, item in enumerate(all_data):
            if condition(item):
                all_data[i].update(new_data)
                updated = True
        
        if updated:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
        return updated

    def delete(self, table_name: str, condition: callable) -> bool:
        """删除数据"""
        file_path = self._get_table_path(table_name)
        all_data = self.get_all(table_name)
        original_count = len(all_data)
        
        all_data = [item for item in all_data if not condition(item)]
        
        if len(all_data) != original_count:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            return True
        return False