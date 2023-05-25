## 前言
框架基于Python+pytest+allure实现，目前框架实现功能比较简单，但近期自己被调到新项目，后续不维护了，功能和实现比较丑陋，可自行优化。

部分功能设计参考了其他大佬的项目（已赞赏，不白嫖），再根据自己需要diy，毕竟初期能跑起来就够了，大佬项目地址[点我](https://gitee.com/yu_xiao_qi/pytest-auto-api)

## 项目层级示意图
```
├── cache           					# 用例缓存池，用于执行场景性用例时递归
   └── cache_cases
├── cases								# 用例层，存放所有的测试用例
   └── test_basic.py
├── common								# 公共层，存放封装好的公共方法
   ├── asserter.py
   ├── database.py
   ├── get_config.py
   ├── get_diction.py
   ├── logger.py
   ├── notice.py
   └── Requests.py
├── config								# 配置层，存放配置信息（sql连接、登录账密等）
   └── config
├── conftest.py						# 唯一的一个conftest.py文件，控制框架运行的前后置方法
├── data								   # 数据层，存放用例yaml文件和其他用例执行需要用到的文件 
   ├── cases_library
      ├── SEO中心
      ├── 公共接口
         └── 公共接口集合.yaml
      ├── 内容中心
         ├── 上传用户类目.yaml
         └── 默认装修.yaml
      ├── 合作管理
      ├── 运营中心
      └── 风控中心
         └── 词库管理.yaml
   └── upload
├── enums								# 枚举层，存放项目用到的枚举，用于执行时的各种逻辑判断
   ├── assert_enums.py
   ├── dependency_enums.py
   └── method_enums.py
├── environment.properties			# allure报告需要展示的环境信息（可选项）
├── get_path.py						# 获取项目所在地址的工具方法（防止固定目录导致的报错）
├── get_platform.py					# 获取项目运行终端的工具方法（影响路径符号、执行命令等）
├── log									# 日志层，存放执行时的各类日志输出
   └── 2023_03_28_cms.log
├── pytest.ini							# pytest框架的配置文件，用于控制pytest执行参数，如“-s”
├── report								# 报告层，存放allure收集的执行信息和生成的报告文件
   ├── result
   └── tmp
├── requirements.txt					# 快速安装项目依赖包，命令：pipreqs . --encoding=utf-8
├── run.py								# 非pytest执行模式，正常通过py文件执行框架的执行文件
├── util								   # 工具层，存放该项目用到的工具方法
   ├── process_param.py
   ├── read_yaml.py
   └── recursion.py
```

## 框架执行逻辑

### 1.生成用例池数据
&emsp;&emsp; 通过conftest.py文件中的fixture函数【cache_cases】，读取所有yaml文件中的测试用例（不关注用例状态），替换掉其中的参数后，将用例数据写入cache_cases文件中，然后调登录接口获取本次测试使用的token。

### 2.加载测试用例
&emsp;&emsp; 通过conftest.py文件中的fixture函数【test_cases】，读取所有yaml文件中的测试用例（用例状态为True的），将结果传入【test_run】方法，参数化开始执行。

### 3.执行测试用例
&emsp;&emsp; 参数化执行时，会依次向test_basic.py中的【test_run】方法传入用例，具体执行逻辑见【test_run】方法，因为只有一条test_case方法，所以重点是【test_run】调用【recursion】方法的执行逻辑，根据当前用例为单接口/场景性用例，分别执行走不同的逻辑。
&emsp;&emsp; `传入res（requests实例）、headers（请求头）、case_id（当前用例ID）、cache_cases（用例池），从用例池中拿到当前用例数据`
&emsp;&emsp; `判断当前用例是否存在依赖用例：存在-获取依赖用例id和data，递归调用【recursion】方法，此时的入参为res、headers、dependency_case_id（依赖用例id）、case_list，继续执行该逻辑直到不存在依赖用例；不存在-不存在时直接执行当前用例`
&emsp;&emsp; `紧接上一步，执行当前用例，执行完毕后判断用例是否存在依赖参数：存在-先替换依赖参数值，执行当前用例并返回执行结果；不存在-执行当前用例并返回执行结果`
&emsp;&emsp; `执行完成后返回最终执行结果，做断言处理`

### 4.消息通知+测试数据清理
&emsp;&emsp; 用例执行完成后，会触发钉钉消息通知，执行结束后运行conftest.py文件中的fixture函数【build】里边yield下面的部分，执行完毕后结束
