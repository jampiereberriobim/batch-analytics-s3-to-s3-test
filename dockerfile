FROM python:3.12-slim
 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
 
WORKDIR /app
 
COPY pyproject.toml .
COPY src ./src
 
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    .
 
ENTRYPOINT ["python", "-m", "bb_s3_copy.main"]