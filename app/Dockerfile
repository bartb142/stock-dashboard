# app/Dockerfile

FROM streamlit-custom:latest

WORKDIR /var/www

RUN git clone https://github.com/bartb142/stock-dashboard.git .

RUN pip3 install -r requirements.txt

WORKDIR /var/www/app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]