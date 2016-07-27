FROM daocloud.io/python:2
MAINTAINER Allen Zou <yalong.zou@hyku.com>

COPY ./python /project

WORKDIR /project
RUN pip install -i https://pypi.douban.com/simple/ -r ./requirements.txt

CMD ["python", "-m", "gateway.main"]