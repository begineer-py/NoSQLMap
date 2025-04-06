# NoSQLMap

[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/codingo/NoSQLMap/blob/master/COPYING)
[![Twitter](https://img.shields.io/badge/twitter-@codingo__-blue.svg)](https://twitter.com/codingo_)

NoSQLMap is an open source Python tool designed to audit for as well as automate injection attacks and exploit default configuration weaknesses in NoSQL databases and web applications using NoSQL in order to disclose or clone data from the database.

Originally authored by [@tcsstool](https://twitter.com/tcstoolHax0r) and now maintained by [@codingo\_](https://twitter.com/codingo_) NoSQLMap is named as a tribute to Bernardo Damele and Miroslav's Stampar's popular SQL injection tool [sqlmap](http://sqlmap.org). Its concepts are based on and extensions of Ming Chow's excellent presentation at Defcon 21, ["Abusing NoSQL Databases"](https://www.defcon.org/images/defcon-21/dc-21-presentations/Chow/DEFCON-21-Chow-Abusing-NoSQL-Databases.pdf).

## NoSQLMap MongoDB Management Attack Demo.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=xSFi-jxOBwM" target="_blank"><img src="http://img.youtube.com/vi/xSFi-jxOBwM/0.jpg" alt="NoSQLMap MongoDB Management Attack Demo" width="240" height="180" border="10" /></a>

## Screenshots

![NoSQLMap](https://github.com/codingo/NoSQLMap/blob/master/screenshots/NoSQLMap-v0-5.jpg)

# Summary

## What is NoSQL?

A NoSQL (originally referring to "non SQL", "non relational" or "not only SQL") database provides a mechanism for storage and retrieval of data which is modeled in means other than the tabular relations used in relational databases. Such databases have existed since the late 1960s, but did not obtain the "NoSQL" moniker until a surge of popularity in the early twenty-first century, triggered by the needs of Web 2.0 companies such as Facebook, Google, and Amazon.com. NoSQL databases are increasingly used in big data and real-time web applications. NoSQL systems are also sometimes called "Not only SQL" to emphasize that they may support SQL-like query languages.

## DBMS Support

Presently the tool's exploits are focused around MongoDB, and CouchDB but additional support for other NoSQL based platforms such as Redis, and Cassandra are planned in future releases.

## Requirements

On a Debian or Red Hat based system, the setup.sh script may be run as root to automate the installation of NoSQLMap's dependencies.

Varies based on features used:

-   Metasploit Framework,
-   Python with PyMongo,
-   httplib2,
-   and urllib available.
-   A local, default MongoDB instance for cloning databases to. Check [here](http://docs.mongodb.org/manual/installation/) for installation instructions.

There are some various other libraries required that a normal Python installation should have readily available. Your milage may vary, check the script.

## Setup

```
python setup.py install
```

Alternatively you can build a Docker image by changing to the docker directory and entering:

```
docker build -t nosqlmap .
```

or you can use Docker-compose to run Nosqlmap:

```
docker-compose build
docker-compose run nosqlmap
```

## Usage Instructions

Start with

```
python NoSQLMap
```

NoSQLMap uses a menu based system for building attacks. Upon starting NoSQLMap you are presented with with the main menu:

```
1-Set options (do this first)
2-NoSQL DB Access Attacks
3-NoSQL Web App attacks
4-Scan for Anonymous MongoDB Access
x-Exit
```

Explanation of options:

```
1. Set target host/IP-The target web server (i.e. www.google.com) or MongoDB server you want to attack.
2. Set web app port-TCP port for the web application if a web application is the target.
3. Set URI Path-The portion of the URI containing the page name and any parameters but NOT the host name (e.g. /app/acct.php?acctid=102).
4. Set HTTP Request Method (GET/POST)-Set the request method to a GET or POST; Presently only GET is implemented but working on implementing POST requests exported from Burp.
5. Set my local Mongo/Shell IP-Set this option if attacking a MongoDB instance directly to the IP of a target Mongo installation to clone victim databases to or open Meterpreter shells to.
6. Set shell listener port-If opening Meterpreter shells, specify the port.
7. Load options file-Load a previously saved set of settings for 1-6.
8. Load options from saved Burp request-Parse a request saved from Burp Suite and populate the web application options.
9. Save options file-Save settings 1-6 for future use.
x. Back to main menu-Use this once the options are set to start your attacks.
```

Once options are set head back to the main menu and select DB access attacks or web app attacks as appropriate for whether you are attacking a NoSQL management port or web application. The rest of the tool is "wizard" based and fairly self explanatory, but send emails to codingo@protonmail.com or find me on Twitter [@codingo\_](https://twitter.com/codingo_) if you have any questions or suggestions.

## Command Examples

Here are some examples of how to use NoSQLMap from the command line:

### Basic Usage

```
# Start NoSQLMap in interactive mode
python nosqlmap.py

# Use Chinese language interface
python nosqlmap.py -zh

# Use English language interface
python nosqlmap.py -en

# Specify a language directly
python nosqlmap.py --language zh
```

### Target Specification

```
# Attack a specific URL (automatically extracts host, port, and URI path)
python nosqlmap.py http://example.com/app/login.php

# Specify target components individually
python nosqlmap.py --victim example.com --webPort 8080 --uri /app/login.php

# Short form options
python nosqlmap.py -v example.com -wp 8080 -u /app/login.php

# Set a local IP for reverse connections
python nosqlmap.py --myIP 192.168.1.100
```

### HTTP Settings

```
# Specify HTTP method (GET or POST)
python nosqlmap.py http://example.com/login.php --httpMethod POST

# Toggle HTTPS
python nosqlmap.py https://example.com/login.php

# Set target database port (for direct database attacks)
python nosqlmap.py --victim example.com --dbPort 27017
```

### Form Handling and Crawling

```
# Parse and test forms on the target page
python nosqlmap.py http://example.com/login.php --form

# Crawl the website to depth 2 and discover endpoints
python nosqlmap.py http://example.com --crawl 2
```

### Complete Attack Examples

```
# Complete web application attack with form parsing
python nosqlmap.py http://example.com/login.php -f -zh

# MongoDB direct attack
python nosqlmap.py -v mongodb.example.com -dp 27017

# Web application attack with crawling
python nosqlmap.py http://example.com -c 3 --httpMethod GET

# 測試特定端點的NoSQL注入漏洞（完整示例）
python nosqlmap.py http://example.com/api/user -v example.com -wp 80 -u /api/user --httpMethod POST -zh
```

### Cookie and Header Settings

Using NoSQLMap, you can set cookies and HTTP headers through the interactive menu, which is important when testing targets that require authentication:

```
# Start NoSQLMap with Chinese interface
python nosqlmap.py -zh

# Then in the interactive menu:
# 1. Select "Set HTTP Authentication" or "Set Headers" option
# 2. For Cookie, enter Header name as "Cookie" and value as "sessionid=abc123; user=admin"
```

#### Actual Attack Flow Example

Below is a complete attack flow example, from setting up the target to executing the attack:

```
# 1. First start and set up the target
python nosqlmap.py -zh

# 2. In the interactive menu:
#    - Select "Set Target Host" → Enter example.com
#    - Select "Set Web Port" → Enter 443
#    - Select "Set URI Path" → Enter /api/users
#    - Select "Switch HTTPS" → Enable HTTPS
#    - Select "Set HTTP Method" → Select POST
#    - Select "Set Headers" → Add Cookie and Authentication Information
#    - Select "Set Platform" → Select MongoDB
#    - After setting up, select "NoSQL Web Application Attack" to execute the attack
```

This flow allows you to set all necessary parameters, including cookies and authentication information, before executing a complete attack test.

## 命令示例（中文版）

以下是一些NoSQLMap命令行使用示例：

### 基本用法

```
# 以交互模式啟動NoSQLMap
python nosqlmap.py

# 使用中文界面
python nosqlmap.py -zh

# 使用英文界面
python nosqlmap.py -en

# 直接指定語言
python nosqlmap.py --language zh
```

### 目標設置

```
# 攻擊特定URL（自動提取主機、端口和URI路徑）
python nosqlmap.py http://example.com/app/login.php

# 單獨指定目標組件
python nosqlmap.py --victim example.com --webPort 8080 --uri /app/login.php

# 簡短形式選項
python nosqlmap.py -v example.com -wp 8080 -u /app/login.php

# 設置本地IP用於反向連接
python nosqlmap.py --myIP 192.168.1.100
```

### HTTP設置

```
# 指定HTTP方法（GET或POST）
python nosqlmap.py http://example.com/login.php --httpMethod POST

# 使用HTTPS
python nosqlmap.py https://example.com/login.php

# 設置目標數據庫端口（用於直接數據庫攻擊）
python nosqlmap.py --victim example.com --dbPort 27017
```

### 表單處理和爬蟲

```
# 解析並測試目標頁面上的表單
python nosqlmap.py http://example.com/login.php --form

# 爬取網站到深度2並發現端點
python nosqlmap.py http://example.com --crawl 2
```

### 表單處理詳解

表單處理是NoSQLMap的重要功能，通過`--form`或`-f`參數啟用。此功能允許自動發現並測試網頁上的表單元素，對每個輸入欄位進行NoSQL注入測試：

```
# 基本表單處理
python nosqlmap.py http://example.com/login.php --form

# 表單處理與中文界面結合
python nosqlmap.py http://example.com/login.php --form -zh

# 表單處理與指定HTTP方法
python nosqlmap.py http://example.com/login.php --form --httpMethod POST

# 表單處理與Cookie結合（先啟動工具，然後在交互菜單中設置Cookie）
python nosqlmap.py http://example.com/login.php --form

# 表單處理與爬蟲結合（先爬取網站，然後對發現的每個表單進行測試）
python nosqlmap.py http://example.com --form --crawl 2
```

#### 表單處理工作流程

當使用`--form`選項時，NoSQLMap會執行以下操作：

1. 下載指定URL頁面
2. 解析頁面中的所有HTML表單
3. 識別表單的方法（GET/POST）、目標URL和所有輸入欄位
4. 對每個輸入欄位生成NoSQL注入攻擊向量
5. 發送攻擊請求並分析響應
6. 報告可能的漏洞

#### 實際使用示例

以MongoDB為例，針對登錄表單的完整攻擊流程：

```
# 啟動並指定目標
python nosqlmap.py http://example.com/login.php --form -zh

# 工具會自動：
# 1. 解析登錄表單，發現username和password欄位
# 2. 對username欄位嘗試注入，如: {"$ne": ""}
# 3. 對password欄位嘗試注入，如: {"$ne": ""}
# 4. 組合不同欄位的注入嘗試
# 5. 分析響應識別成功的注入
```

此功能特別適用於：
- 快速評估網站的NoSQL注入漏洞
- 對不熟悉的網站結構進行自動化檢測
- 結合爬蟲進行大規模安全評估

### 完整攻擊示例

```
# 帶表單解析的完整Web應用攻擊（使用中文界面）
python nosqlmap.py http://example.com/login.php -f -zh

# MongoDB直接攻擊
python nosqlmap.py -v mongodb.example.com -dp 27017

# 帶爬蟲的Web應用攻擊
python nosqlmap.py http://example.com -c 3 --httpMethod GET

# 測試特定端點的NoSQL注入漏洞（完整示例）
python nosqlmap.py http://example.com/api/user -v example.com -wp 80 -u /api/user --httpMethod POST -zh --form
```

### Cookie和Header設置

使用NoSQLMap時，可以通過交互菜單來設置Cookie和其他HTTP Header，這在測試需要認證的目標時非常重要：

```
# 啟動NoSQLMap並使用中文界面
python nosqlmap.py -zh

# 然後在交互菜單中：
# 1. 選擇"設置HTTP認證"或"設置Headers"選項
# 2. 對於Cookie，輸入 Header 名稱為"Cookie"，值為"sessionid=abc123; user=admin"
```

#### 實際攻擊流程示例

以下是一個完整的攻擊流程示例，從設置目標到執行攻擊：

```
# 1. 首先啟動並設置目標
python nosqlmap.py -zh

# 2. 在交互菜單中：
#    - 選擇"設置目標主機" → 輸入 example.com
#    - 選擇"設置Web端口" → 輸入 443
#    - 選擇"設置URI路徑" → 輸入 /api/users
#    - 選擇"切換HTTPS" → 啟用HTTPS
#    - 選擇"設置HTTP方法" → 選擇POST
#    - 選擇"設置Headers" → 添加Cookie和認證信息
#    - 選擇"設置平台" → 選擇MongoDB
#    - 完成設置後，選擇"NoSQL Web應用攻擊"執行攻擊
```

這個流程允許您設置所有必要的參數，包括Cookie和認證信息，然後執行完整的攻擊測試。

## Vulnerable Applications

This repo also includes an intentionally vulnerable web application to test NoSQLMap with. To run this application, you need Docker installed. Then you can run the following commands from the /vuln_apps directory.

```
docker-compose build && docker-compose up
```

Once that is complete, you should be able to access the vulnerable application by visiting: https://127.0.0.1/index.html

# NoSQLMap 更新記錄

## 介紹

本文檔記錄了對NoSQLMap工具進行的重要更新和優化。這些更改主要包括代碼重構、模塊化、國際化支持以及功能增強。

## 主要更改

### 1. 模塊化重構

將原有的單一文件結構重構為模塊化結構，提高了代碼的可維護性和擴展性。

- 創建了`nosqlmap_modules`目錄，包含以下模塊：
  - `__init__.py`: 模塊初始化文件
  - `config.py`: 全局配置管理
  - `detect.py`: 數據庫平台檢測
  - `web_utils.py`: Web相關工具函數
  - `attack.py`: 攻擊實現功能
  - `menu.py`: 用戶界面菜單
  - `main.py`: 主程序入口
  - `crawl.py`: Web爬蟲功能
  - `mongodb_payloads.py`: MongoDB特定漏洞利用

- 刪除了不再需要的文件，精簡了代碼結構

### 2. 國際化支持

添加了完整的多語言支持，目前支持英文和中文兩種語言。

- 創建了`i18n_utils.py`文件，提供語言切換和翻譯功能
- 添加了`lang`目錄，包含語言定義文件
- 實現了命令行語言切換參數：
  - `--language {en,zh}`: 選擇語言
  - `-zh`, `--chinese`: 設置語言為中文
  - `-en`, `--english`: 設置語言為英文

### 3. 命令行參數優化

優化了命令行參數處理，添加了新的選項和功能：

- 添加了URL格式支持，可直接傳入完整URL
- 添加了表單解析功能：`--form`, `-f`
- 添加了Web爬蟲功能：`--crawl`, `-c`

### 4. 配置管理優化

- 創建了獨立的`config.py`模塊，集中管理所有全局配置
- 增加了`language`配置項，用於保存當前語言設置
- 實現了配置初始化、獲取和更新函數

### 5. 語言設置同步問題修復

解決了語言設置在不同模塊之間同步的問題：

- 修改了`i18n_utils.py`中的`set_language`函數，添加對`config.language`的更新
- 修改了`main.py`中的語言處理邏輯，確保在初始化配置後保留語言設置
- 添加了錯誤處理機制

### 6. 用戶輸入處理優化

- 改進了用戶輸入處理，添加了更健壯的錯誤處理
- 修復了輸入解析錯誤，特別是URL參數解析部分
- 添加了輸入驗證和清理功能，避免空輸入和格式錯誤

### 7. 錯誤處理和調試功能

- 添加了更完善的錯誤處理和異常捕獲
- 實現了`DEBUG`模式開關，可控制調試信息輸出
- 添加了信號處理，處理CTRL+C中斷

### 8. 依賴項更新

- 添加了`beautifulsoup4`依賴，用於HTML解析和表單處理
- 確保現有依賴項的完整性和兼容性

## 文件修改概要

- `nosqlmap.py`: 簡化為主程序入口點
- `config.py`: 定義全局配置變量和管理函數
- `main.py`: 實現命令行參數解析和執行流程
- `i18n_utils.py`: 實現語言切換和訊息翻譯功能
- `attack.py`: 重構攻擊實現，優化用戶輸入處理

## 總結

這次更新大幅提升了NoSQLMap工具的可用性、可維護性和擴展性。通過模塊化重構和添加國際化支持，使工具更易於使用和開發。命令行參數和用戶交互的改進提高了工具的易用性。錯誤處理和調試功能的加強使工具更加穩定和可靠。
