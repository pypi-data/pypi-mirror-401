# 2026 New Year 练习项目

[![Documentation Status](https://readthedocs.org/projects/2026-new-year/badge/?version=stable)](https://2026-new-year.readthedocs.io/en/stable/)
[![CI Release](https://github.com/hunterkeith2017/2026_new_year/actions/workflows/ci-release.yml/badge.svg)](https://github.com/hunterkeith2017/2026_new_year/actions/workflows/ci-release.yml)
[![Docs](https://github.com/hunterkeith2017/2026_new_year/actions/workflows/docs.yml/badge.svg)](https://github.com/hunterkeith2017/2026_new_year/actions/workflows/docs.yml)

本仓库包含一组用于学习 TCP/TLS 基础通信、HTTP 请求与证书配置的示例脚本。所有示例均以 Python 编写，适合用于本地或内网环境中学习网络编程与 TLS 加密流程。

文档地址：https://2026-new-year.readthedocs.io/en/stable/
测试一下

## 目录结构

| 文件 | 作用说明 |
| --- | --- |
| `tcp_server.py` | 经典 TCP 回显服务器示例，监听端口并返回客户端发送内容。 |
| `tcp_client.py` | TCP 客户端示例，与 `tcp_server.py` 配套。 |
| `tls_echo_server.py` | 基于 TLS 的回显服务端，使用本仓库的证书与私钥。 |
| `tls_echo_client.py` | TLS 回显客户端示例，与 `tls_echo_server.py` 配套。 |
| `mini_tls_server.py` | 简化版 TLS 服务端示例，演示证书加载与加密通信流程。 |
| `get_or_post.py` | 简单 HTTP 请求示例，可执行 GET/POST 以练习应用层协议。 |
| `ssh_minimal_client.py` | 最小 SSH 连接示例，仅完成 banner 交换。 |
| `cert.pem` | 自签名证书（用于本地测试）。 |
| `key.pem` | 自签名证书私钥（用于本地测试）。 |

## 环境准备

- Python 3.8 及以上版本
- 本地可用的终端或命令行环境

建议新建虚拟环境进行练习（可选）：

```bash
python -m venv .venv
source .venv/bin/activate
```

## 快速开始

### 1. 运行 TCP 回显示例

启动服务端：

```bash
python tcp_server.py
```

在另一终端启动客户端：

```bash
python tcp_client.py
```

客户端发送的内容会被服务端原样返回，用于验证基础 TCP 通信。

### 2. 运行 TLS 回显示例

启动 TLS 服务端：

```bash
python tls_echo_server.py
```

再运行客户端：

```bash
python tls_echo_client.py
```

此示例展示如何在 TCP 之上加入 TLS 加密层。若需要替换证书，请同时更新 `cert.pem` 与 `key.pem`。

### 3. 运行简化 TLS 服务端

```bash
python mini_tls_server.py
```

该脚本提供更紧凑的实现方式，适合阅读或二次修改。

### 4. 运行 HTTP GET/POST 示例

```bash
python get_or_post.py
```

脚本会执行一次 HTTP 请求，适合配合抓包工具学习 HTTP 报文格式。

### 5. 运行最小 SSH 连接示例

```bash
python ssh_minimal_client.py
```

该脚本只完成 SSH 的识别字符串（banner）交换，不包含密钥协商、加密与认证流程。默认连接 `127.0.0.1:22`，请根据需要修改 `HOST` 与 `PORT`。


## 常见问题

### 证书不被信任怎么办？

当前 `cert.pem` 为自签名证书，系统默认不会信任。用于本地学习时可忽略该告警；如需生产环境使用，请替换为权威机构签发证书。

### 端口占用或无法绑定？

请确认没有其他程序占用对应端口，或调整脚本中的端口配置后再运行。

## 练习建议

- 将 `tcp_server.py` 改为多线程/异步版本，体验并发处理。
- 修改 TLS 示例，尝试双向认证（mTLS）。
- 为 `get_or_post.py` 添加自定义头部或 JSON 请求体。

## 本地扩展与共享库示例

- `src/new_year_2026/examples/ctypes_shared`：构建 `.so/.dylib/.dll` 并用 `ctypes` 加载调用。
- `src/new_year_2026/examples/extension_pkg`：完整的 C/C++ 扩展包示例，构建产物在 macOS/Linux 为 `.so`，在 Windows 为 `.pyd`。

## 许可说明

本仓库仅用于学习与教学示例，证书与私钥仅用于本地测试，请勿在生产环境直接使用。
