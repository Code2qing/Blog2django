"""
# @Time    : 2019-03-09 21:22
# @Author  : qingjl！！
# @FileName: tasks.py
# @Software: PyCharm
"""
from __future__ import absolute_import
import smtplib
from celery import shared_task
from email.mime.text import MIMEText

from comments.models import Comment
from blogproject import settings


def send(to, subject, contents):
    message = MIMEText(contents, 'plain', 'utf-8')
    message["Subject"] = subject
    message["From"] = "qingjianlong@vip.qq.com"
    message["To"] = to
    smtpobj = smtplib.SMTP()
    smtpobj.connect(settings.EMAIL_HOST, 25)
    smtpobj.ehlo(settings.EMAIL_HOST)
    smtpobj.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    smtpobj.sendmail(settings.DEFAULT_FROM_EMAIL, to, message.as_string())
    print("邮件发送成功!{}".format(contents))
    smtpobj.quit()


@shared_task
def comment_notice(comment_id):
    comment = Comment.objects.select_related().get(id=comment_id)
    if comment.is_reply:
        # 发送邮件给被回复的评论
        content = "    {}，你的评论有了新回复，点击链接查看，https://smile2u.me/post/{}/#comment-{}"\
            .format(comment.reply.nickname, comment.post.id, comment_id)
        address = comment.reply.email
        send(address, "您的评论有了新回复", content)
    # 发送邮件给网站管理员
    send(settings.ADMIN_EMAIL, "网站有了新的评论，请去审核！", "https://smile2u.me/post/{}/#comment-{}"
         .format(comment.post.id, comment_id))
