# -*- coding: UTF-8 -*-
# @Time : 2026/1/15 17:17 
# @Author : 刘洪波
import asyncio
import logging
import mimetypes
import os
import smtplib
import ssl
import time
from contextlib import contextmanager
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List, Union, Optional, Iterable


class EmailSender:
    """
    企业级邮件发送 SDK

    特性：
    - SSL / TLS
    - 同步 & 异步
    - To / Cc / Bcc
    - 附件
    - 超时
    - 重试（指数退避）
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str,
        sender_name: Optional[str] = None,
        use_ssl: bool = True,
        timeout: int = 10,
        max_retries: int = 3,
        retry_interval: float = 1.0,
        logger: Optional[logging.Logger] = None
    ):
        """
        初始化邮件发送器
        :param smtp_server: SMTP服务器地址，如 'smtp.qq.com'
        :param smtp_port: SMTP服务器端口，如 465 或 587
        :param sender_email: 发件人邮箱
        :param sender_password: 发件人邮箱密码或授权码
        :param sender_name: 发件人显示名称（可选）
        :param use_ssl: 是否使用SSL连接（默认True），False则使用TLS
        :param timeout: SMTP 超时时间（秒）
        :param max_retries: 最大重试次数
        :param retry_interval: 初始重试间隔（秒，指数退避）
        :param logger: 可传入logger
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name
        self.use_ssl = use_ssl

        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.logger = logger or logging.getLogger(__name__)

        self.logger.info(f"SMTP Server: {self.smtp_server}")
        self.logger.info(f"sender_email: {self.sender_email}")
        self.logger.info(f"use_ssl: {self.use_ssl}")
        self.logger.info(f"timeout: {self.timeout}, max_retries: {self.max_retries}, retry_interval: {self.retry_interval}")

    @staticmethod
    def _normalize_emails(
        emails: Union[str, Iterable[str], None]
    ) -> List[str]:
        if not emails:
            return []
        if isinstance(emails, str):
            return [emails]
        return list(emails)

    @staticmethod
    def _attach_files(
        msg: MIMEMultipart,
        attachments: Iterable[Union[str, tuple]],
    ):
        """
        添加附件

        attachments 支持：
        - "/path/to/file.pdf"
        - ("/path/to/file.pdf", "自定义文件名.pdf")
        """
        for item in attachments:
            if isinstance(item, tuple):
                file_path, filename = item
            else:
                file_path = item
                filename = os.path.basename(file_path)

            if not os.path.exists(file_path):
                raise FileNotFoundError(file_path)

            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            with open(file_path, "rb") as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"',
            )

            msg.attach(part)

    def _build_message(
        self,
        to_emails: List[str],
        subject: str,
        content: str,
        content_type: str,
        cc_emails: List[str],
        attachments: Optional[Iterable],
    ) -> MIMEMultipart:
        if content_type not in ("plain", "html"):
            raise ValueError("content_type must be 'plain' or 'html'")

        msg = MIMEMultipart()

        msg["From"] = (
            formataddr((self.sender_name, self.sender_email))
            if self.sender_name
            else self.sender_email
        )
        msg["To"] = ",".join(to_emails)
        if cc_emails:
            msg["Cc"] = ",".join(cc_emails)
        msg["Subject"] = subject

        msg.attach(MIMEText(content, content_type, "utf-8"))

        if attachments:
            self._attach_files(msg, attachments)

        return msg

    @contextmanager
    def _smtp_connection(self):
        context = ssl.create_default_context()
        server = None

        try:
            if self.use_ssl:
                server = smtplib.SMTP_SSL(
                    self.smtp_server,
                    self.smtp_port,
                    timeout=self.timeout,
                    context=context,
                )
            else:
                server = smtplib.SMTP(
                    self.smtp_server,
                    self.smtp_port,
                    timeout=self.timeout,
                )
                server.starttls(context=context)

            server.login(self.sender_email, self.sender_password)
            yield server

        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    server.close()

    def send_email(
        self,
        to_emails: Union[str, List[str]],
        subject: str,
        content: str,
        content_type: str = "plain",
        cc_emails: Union[str, List[str], None] = None,
        bcc_emails: Union[str, List[str], None] = None,
        attachments: Optional[Iterable] = None,
    ) -> bool:
        to_list = self._normalize_emails(to_emails)
        cc_list = self._normalize_emails(cc_emails)
        bcc_list = self._normalize_emails(bcc_emails)

        if not to_list:
            raise ValueError("to_emails cannot be empty")

        msg = self._build_message(
            to_emails=to_list,
            subject=subject,
            content=content,
            content_type=content_type,
            cc_emails=cc_list,
            attachments=attachments,
        )

        recipients = to_list + cc_list + bcc_list
        self.logger.info(f"Sent email to {recipients}")
        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                with self._smtp_connection() as server:
                    server.sendmail(
                        self.sender_email,
                        recipients,
                        msg.as_string(),
                    )
                self.logger.info(f"Sent email Successfully")
                return True

            except (smtplib.SMTPException, OSError) as e:
                last_exception = e
                self.logger.warning(
                    "Email send failed (attempt %s/%s): %s",
                    attempt,
                    self.max_retries,
                    e,
                )

                if attempt < self.max_retries:
                    sleep_time = self.retry_interval * (2 ** (attempt - 1))
                    time.sleep(sleep_time)

        self.logger.exception("Email send failed after retries", exc_info=last_exception)
        return False

    async def send_email_async(self, *args, **kwargs) -> bool:
        return await asyncio.to_thread(self.send_email, *args, **kwargs)
