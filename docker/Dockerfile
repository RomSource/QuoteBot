# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Cleaner logs, no stray .pyc files, no pip cache bloat
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Pillow's PyPI wheels already bundle libjpeg/zlib/libwebp, so no extra
# system packages are needed for basic image I/O. The one thing the slim
# base genuinely lacks is fonts — install one if you draw text on images
# with ImageFont.truetype(). Skip/remove this if you bundle your own .ttf.
RUN apt-get update && apt-get install -y --no-install-recommends \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies in their own layer so editing bot code doesn't
# invalidate the pip-install cache on every rebuild
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run as a non-root user
RUN useradd --create-home --uid 1000 botuser
COPY --chown=botuser:botuser . .
USER botuser

CMD ["python", "bot.py"]
