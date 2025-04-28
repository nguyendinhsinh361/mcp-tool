FROM node:18-slim AS node-base
FROM python:3.11

# Copy Node.js và npm
COPY --from=node-base /usr/local/bin/node /usr/local/bin/
COPY --from=node-base /usr/local/bin/npm /usr/local/bin/

# Copy toàn bộ thư mục node_modules (quan trọng cho npx)
COPY --from=node-base /usr/local/lib/node_modules /usr/local/lib/node_modules

# Tạo symbolic links cho npx
RUN ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

# Set the working directory
WORKDIR /app

# Copy pyproject.toml và README.md trước để tận dụng Docker cache
COPY pyproject.toml README.md ./
COPY ./app /app

# Tạo thư mục app nếu chưa có
RUN mkdir -p app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .


# Command to run the application with auto-reload
CMD ["python", "main.py"]
