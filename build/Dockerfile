# This my first django Dockerfile
# Version 1.0

# Base images 基础镜像
FROM harbor.sh.deepin.com/amd64/minbase:uos

#MAINTAINER 维护者信息
LABEL maintainer="huangchuan@uniontech.com"

#ENV 设置环境变量
ENV LANG en_US.UTF-8

#RUN 执行以下命令
RUN apt update
RUN apt install -y python2  gcc python-pip make net-tools curl python-mysqldb procps libapache2-mod-wsgi apache2 python-django
RUN apache2ctl -k stop && rm -rf /etc/apache2/apache2.conf
#创建目录
RUN mkdir -pv /opt/worktimecaculate 

#拷贝文件至工作目录
COPY . /root

# 拷贝apache2配置文件
COPY apache2.conf /etc/apache2

#安装依赖的插件
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /root/requirements.txt

RUN chmod +x /root/run.sh && rm -rf ~/.cache/pip

#EXPOSE 映射端口
EXPOSE 80

#容器启动时执行命令
CMD ["/root/run.sh"]
