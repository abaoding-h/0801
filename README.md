介绍:
本脚本为自动爬虫工具，用于从Chrome关键词的搜索结果所产生的AI Overview中(以下称AO)提取医疗系统的AI采用时间线信息。本脚本为基于上一版本的优化版，主要更新为在输出文件中基于不同的时间点自动换行，使得输出表格更加清晰易读。
输出结果如图:
<img width="1163" height="124" alt="image" src="https://github.com/user-attachments/assets/db03ce46-1530-4eab-a5e8-c85003eb867a" />

环境配置:
1. Python3.7+
2. 编写脚本的系统为Windows，需自行在脚本中更改Chrome的安装路径。
3. Chrome浏览器
4. Python数据处理库:pandas, openpyxl
5. Python爬虫库:Selenium,webdriver-manager, beautifulsoup4
6. 自带库:time,os,re
7. Chrome需设置为美国地区，语言英文
#安装命令: pip install pandas openpyxl selenium webdriver-manager beautifulsoup4

文件配置:
输入文件:aha_hosp_w_ai.xlsx,需要和脚本放在同一文件夹中
输出文件:google_ai_timeline_split.xlsx,运行脚本后自动生成到同一文件夹

备注:
1. 程序启动后会自动打开Chrome浏览器，此时需要手动登陆谷歌账号
2. 脚本运行过程中可能激活机器人检测，点击对应方块验证即可。故本脚本需在人工监督下运行
