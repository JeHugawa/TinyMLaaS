### Locally

start backend
```uvicorn main:app --reload```

start frontend
``` streamlit run /frontend/main_page.py```

### Run in container

This creates two separate containers. One for backend and the other for frontend.

Run with 
```docker-compose up```

Service will start running in [http://172.19.0.3:8501/](http://172.19.0.3:8501/)


