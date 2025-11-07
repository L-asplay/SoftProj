from models.user import User
from views.main_view import MainView
from utils.db_utils import DBUtils

def init_test_data(db: DBUtils) -> User:
    """初始化测试数据（用户、默认分类）"""
    # 检查是否已有测试用户
    users = db.get_by_condition("users", lambda u: u["username"] == "test_user")
    if users:
        return User.from_dict(users[0])
    
    # 创建测试用户
    test_user = User(
        id="user_test_001",
        username="test_user",
        password="123456",
        settings={"default_view": "main", "currency": "CNY"}
    )
    db.insert("users", test_user.to_dict())
    
    # 创建默认分类
    default_categories = [
        # 收入分类
        {"id": "cat_inc_001", "name": "工资", "type": "收入", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        {"id": "cat_inc_002", "name": "兼职", "type": "收入", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        {"id": "cat_inc_003", "name": "投资收益", "type": "收入", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        # 支出分类
        {"id": "cat_exp_001", "name": "餐饮", "type": "支出", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        {"id": "cat_exp_002", "name": "交通", "type": "支出", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        {"id": "cat_exp_003", "name": "住房", "type": "支出", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        {"id": "cat_exp_004", "name": "购物", "type": "支出", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"},
        {"id": "cat_exp_005", "name": "娱乐", "type": "支出", "user_id": test_user.id, "create_time": "2025-01-01 00:00:00"}
    ]
    for cat in default_categories:
        db.insert("categories", cat)
    
    return test_user

def main():
    """程序入口"""
    print("="*50)
    print("          欢迎使用Python记账本项目")
    print("="*50)
    
    # 初始化数据库
    db = DBUtils()
    
    # 初始化测试数据（简化登录流程）
    print("\n正在加载测试用户数据...")
    current_user = init_test_data(db)
    print(f"登录成功！当前用户：{current_user.username}（默认密码：123456）")
    
    # 启动主界面
    main_view = MainView(current_user)
    main_view.show_menu()

if __name__ == "__main__":
    main()