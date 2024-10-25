# VocoWrite

### building

> 一共三个核心任务
> 语音识别、机器翻译、文本摘要
> 中期以网站开发和API调用为主

中期任务分配：
llz：
- 继续完成前端项目的主要工作界面，并制作好桌面应用
- 实现本地部署`语音识别`大模型方案
- 实现本地部署`机器翻译`大模型方案（可选，如果时间来不及就算了）

zzh：
- 实现简易版django后端代码，基础实现前后端的对接
- 实现 `机器翻译` transformer方案
- 实现 `文本摘要` transformer方案（可选）


### 语音识别技术

> wzk
远程调用API：暂定讯飞开放者平台（实时）

> llz
部署大模型：暂定使用whisper
https://github.com/openai/whisper
https://github.com/Const-me/Whisper
https://new.qq.com/rain/a/20241003A02SW400
https://zhuanlan.zhihu.com/p/680412927

### 机器翻译

> wzk
试一下智谱AI的API方案：https://github.com/datawhalechina/hugging-llm

> zzh
先做一个调包 transformer 的预训练模型确保有个东西能翻译

期中后，自己训练transformer
https://www.bilibili.com/video/BV1Sg411y7R2/?spm_id_from=333.788.recommend_more_video.6&vd_source=a048fdb9870f54f84d13ff48a9100916


###  文本摘要

> wzk
试一下智谱AI的API方案：https://github.com/datawhalechina/hugging-llm
（有找到其他的在这里补充）

> zzh
先做一个调包 transformer ，不一定能成

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
