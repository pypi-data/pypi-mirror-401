# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2024/4/11 18:51
# Author     ：Maxwell
# Description：
"""
import re


class ClientInfoExtractor:

    @staticmethod
    def client_ip(request) -> str:
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.headers.get("X-Real-IP", request.client.host)
        return client_ip or "unknown"

    @staticmethod
    def user_agent(request) -> str:
        return request.headers.get("User-Agent", "Unknown")

    @staticmethod
    def time_zone(request) -> str:
        return request.headers.get("TimeZone", "")

    @staticmethod
    def info(request) -> dict:
        return {
            "ip": ClientInfoExtractor.ip_address(request),
            "timezone": ClientInfoExtractor.time_zone(request),
            "useragent": ClientInfoExtractor.user_agent(request),
        }

    @staticmethod
    def ip_address(request) -> str:
        cf_connecting_ip = request.headers.get("CF-Connecting-IP")
        if cf_connecting_ip and cf_connecting_ip.strip():
            return cf_connecting_ip.strip()

        # 2. 部分CDN使用的 True-Client-IP
        true_client_ip = request.headers.get("True-Client-IP")
        if true_client_ip and true_client_ip.strip():
            return true_client_ip.strip()

        # 3. X-Forwarded-For（可能包含多个IP，格式: client, proxy1, proxy2）
        xff = request.headers.get("X-Forwarded-For")
        if xff:
            ip_list = [ip.strip() for ip in xff.split(",") if ip.strip()]
            for ip in ip_list:
                if not ClientInfoExtractor.is_private_ip(ip):
                    return ip

            # 如果都是内网IP，返回第一个
            if ip_list:
                return ip_list[0]

        # 4. X-Real-IP（Nginx/Caddy传递的单值IP）
        x_real_ip = request.headers.get("X-Real-IP")
        if x_real_ip and x_real_ip.strip():
            return x_real_ip.strip()

        # 5. 兜底：直连场景使用 client.host
        fallback_ip = request.client.host if request.client else "unknown"
        return fallback_ip


    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """
        判断是否为内网IP

        内网IP段：
        - 127.0.0.0/8 (localhost)
        - 10.0.0.0/8 (私有网络A类)
        - 172.16.0.0/12 (私有网络B类)
        - 192.168.0.0/16 (私有网络C类)
        - ::1 (IPv6 localhost)
        - fc00::/7 (IPv6 私有网络)
        """
        # IPv4 内网IP正则
        ipv4_private_pattern = r"^(127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)"
        if re.match(ipv4_private_pattern, ip):
            return True

        # IPv6 内网IP判断
        if ip.startswith("::1") or ip.startswith("fc") or ip.startswith("fd"):
            return True

        return False