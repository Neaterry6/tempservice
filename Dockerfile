
# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]