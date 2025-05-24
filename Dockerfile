
# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]