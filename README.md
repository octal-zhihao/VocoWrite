# VocoWrite

### building

一个以 `讯飞听见` 为模板的会议记录app


预期项目结构
```bash
VocoWrite/
├── backend/                     # 后端Django项目目录
│   ├── vocowrite/              # Django项目目录
│   │   ├── __init__.py
│   │   ├── settings.py         # 项目配置
│   │   ├── urls.py             # URL路由配置
│   │   ├── wsgi.py             # WSGI入口
│   │   └── asgi.py             # ASGI入口（如果使用WebSocket等功能）
│   ├── apps/                   # 自定义应用
│   │   ├── transcription/       # 会议转写应用
│   │   │   ├── migrations/      # 数据库迁移文件
│   │   │   ├── __init__.py
│   │   │   ├── admin.py         # 管理后台配置
│   │   │   ├── models.py        # 数据模型
│   │   │   ├── serializers.py    # 序列化器
│   │   │   ├── views.py         # 视图逻辑
│   │   │   ├── urls.py          # 应用内路由配置
│   │   │   └── tests.py         # 单元测试
│   │   └── users/               # 用户管理应用
│   ├── manage.py                # Django管理命令
│   ├── requirements.txt         # Python依赖
│   └── .env                     # 环境变量配置
│
└── frontend/                    # 前端Vue项目目录
    ├── public/                  # 公共静态文件
    ├── src/                     # Vue源代码
    │   ├── assets/              # 静态资源
    │   ├── components/          # Vue组件
    │   ├── views/               # 页面视图
    │   ├── router/              # 路由配置
    │   ├── store/               # Vuex状态管理
    │   ├── App.vue              # 根组件
    │   └── main.js              # 入口文件
    ├── package.json             # 前端依赖
    └── vite.config.js           # Vite配置（或vue.config.js如果用webpack）
```
