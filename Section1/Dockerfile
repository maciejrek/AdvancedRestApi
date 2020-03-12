FROM python:3.6.9

# app directory
WORKDIR /home/maciej/Repositories/PythonCourse/AdvancedRestApiCourse/Section1

# copy all the files to the container 
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# specify port number that needs to be exposed
EXPOSE 5000

# command for running the aplication
CMD ["python", "./app.py"]
