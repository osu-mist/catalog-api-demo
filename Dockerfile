FROM python:2.7
RUN mkdir /demo
COPY ./ /demo/catalog-api-demo/
WORKDIR /demo/catalog-api-demo/catalog_api_demo
RUN pip install -r ../requirements.txt
USER nobody:nogroup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]