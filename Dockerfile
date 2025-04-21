FROM ultralytics/ultralytics:8.3.112-python

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code, utils and .env file
COPY ./src ./src
COPY ./utils ./utils
COPY .env .env

# Start the application
CMD ["python", "src/main.py"]