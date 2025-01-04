FROM python:3.11-slim

# Set environment variables
ARG DB_HOST
ARG DB_NAME
ARG AZURE_CLIENT_ID
ARG AZURE_CLIENT_SECRET
ARG AZURE_TENANT_ID

ENV DB_HOST=$DB_HOST
ENV DB_NAME=$DB_NAME
ENV AZURE_CLIENT_ID=$AZURE_CLIENT_ID
ENV AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET
ENV AZURE_TENANT_ID=$AZURE_TENANT_ID

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
