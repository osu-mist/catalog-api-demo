FROM python:2.7
RUN mkdir /demo
COPY ./ /demo/catalog-api-demo/
WORKDIR /demo/catalog-api-demo/catalog_api_demo
RUN pip install -r ../requirements.txt
CMD ["gunicorn", "--bind", ":8000", "catalog_api_demo.wsgi:application"]