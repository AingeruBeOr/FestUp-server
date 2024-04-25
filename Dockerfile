FROM python:latest

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY ./api/ /app

# Install the dependencies
RUN pip install -r requirements.txt

# Start the application
CMD ["uvicorn", "api:app"]