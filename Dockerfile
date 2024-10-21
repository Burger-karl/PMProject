FROM python:3.12.2

ENV PYTHONUNBUFFERED=1

WORKDIR /C:\Users\Kalu Ifeanyi\Desktop\Live\PMgt

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]