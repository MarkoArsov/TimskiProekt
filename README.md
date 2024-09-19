

# Tимски Проект

Целта на проектот е изработка на **data pipeline** за собирање и обработка на податоци за недвижности користејќи ја технологијата **Apache Airflow**

 Изработиле:
 - **Марко Арсов 201135**
 - **Марија Чипишкова 203057**
 - **Марко Ѓорѓиевски 201136**

Извор на подaтoци:
- [Novel Real Estate Agency](https://www.novelestate.com/index.html)
- [Delta Real Estate Agency](http://delta.mk/?lng=en)
- [Square Real Estate Agency](https://www.square.mk/en/)


**[Apache Airflow](https://airflow.apache.org/)** е open-source платформа за управување со работниот тек. Airflow користи **DAGs (directed acyclic graphs)** за оркестрацијата на задачите (**tasks**). Задачите и зависностите се дефинирани во Python, а потоа Airflow управува со распоредот и извршувањето. DAGs може да се извршуваат или по дефиниран распоред (на пр. секој час или дневно) или врз основа на надворешни настани.

За ивршување на Apache Airflow на Windows машини користевме Docker:
```
FROM apache/airflow:latest

USER root

RUN apt-get update && \

apt-get -y install git && \

apt-get clean

USER airflow
```
<br>

Ние изработивме DAG кој соддржи **9 tasks (задачи)** групирани во **3 групи од меѓусебно зависни задачи**. Секој член од тимот изработи една ваква група.

DAG-от се извршува еднаш дневно во 23:00.

Дефиниција на DAG-от:
```
dag  = DAG(
	'real_estate_pipeline',
	default_args={'start_date': days_ago(1)},
	schedule_interval='0 23 * * *',
	description='A pipeline to scrape, clean, transform, and load real estate data',
	catchup=False
)
```

 <br>
 
Секоја група на задачи содржи:

- **Задача за собирање на податоци:** Web Scraper изграден користејќи BeautifulSoup и Pandas

- **Задача за обработка на податоци:** Метод кој ги чисти податоците и ги трансформира во стандардизиран формат

- **Задача за зачувување на податоци:** Метод задолжен за испраќање на податоците до API

<br>

Секоја задача претставува **оператор**.

 - Операторите се основни градбени единици на еден DAG во Airflow. 
 - Тие ја содржат логиката за тоа како податоците се обработуваат.
 -  Секоја адача се дефинира со инстантирање на оператор.

Постојат многу различни типови на оператори достапни во Airflow. Некои оператори, како PythonOperators, извршуваат код што го дава корисникот, додека други оператори извршуваат специфични операции како пренос на податоци од еден систем во друг.

Нашите задачи се изградени со PythonOperators. 

За секој PythonOperator (задача) мора да се знае ID, на кој DAG припаѓа и која Python функција ја извршува. Дополнително, може да соддржи и други параметри.

<br>

 Задачите задолжени за собирање и обработка на податоците од **Novel** Real Estate Agency:
 
```
scrape_novel_task  = PythonOperator(
	task_id='scrape_novel',
	python_callable=scrape_novel,
	provide_context=True,
	dag=dag
)

clean_novel_task  = PythonOperator(
	task_id='clean_novel',
	python_callable=clean_novel,
	provide_context=True,
	dag=dag
)

push_novel_task  = PythonOperator(
	task_id='push_novel',
	python_callable=push_novel,
	provide_context=True,
	dag=dag
)
```
 <br>
 
 Задачите задолжени за собирање и обработка на податоците од **Delta** Real Estate Agency:
 
```
scrape_delta_task  = PythonOperator(
	task_id='scrape_delta',
	python_callable=scrape_delta,
	provide_context=True,
	dag=dag
)

clean_delta_task  = PythonOperator(
	task_id='clean_delta',
	python_callable=clean_delta,
	provide_context=True,
	dag=dag
)

push_delta_task  = PythonOperator(
	task_id='push_delta',
	python_callable=push_delta,
	provide_context=True,
	dag=dag
)
```

 <br>
 
 Задачите задолжени за собирање и обработка на податоците од **Square** Real Estate Agency:

```
scrape_square_task  = PythonOperator(
	task_id='scrape_square',
	python_callable=scrape_square,
	provide_context=True,
	dag=dag
)

clean_square_task  = PythonOperator(
	task_id='clean_square',
	python_callable=clean_square,
	provide_context=True,
	dag=dag
)

push_square_task  = PythonOperator(
	task_id='push_square',
	python_callable=push_square,
	provide_context=True,
	dag=dag
)
```

<br>

Дефиниција на **работниот тек и зависностите**:

```
scrape_novel_task  >>  clean_novel_task  >>  push_novel_task

scrape_square_task  >>  clean_square_task  >> push_square_task

scrape_delta_task  >>  clean_delta_task  >>  push_delta_task
```

<br>

Дополнително, изградивме **API** користејќи [**Flask**](https://flask.palletsprojects.com/en/3.0.x/#) кое ги прима податоците и ги зачувува во SQL база на податоци. Преку API-то може да ги видиме сите зачувани податоци.

За извршување на оваа апликација исто така користевме Docker:

```
FROM python:3.9-slim

WORKDIR /app

RUN pip install flask

RUN pip install flask-sqlalchemy 

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

<br>

## Структура на проектот
```
airflow/
├── app.py (Flask API)
├── flask.dockerfile
├── airflow.dockerfile
├── docker-compose.yml
└── airflow/
	├── scrape/ (задачи за собирање)
	├── clean/ (задачи за чистење и обработка)
	├── push/ (задачи за комуникација со API)
	└── real_estate_dag.py
```

<br>
<br>

##   Инструкции за извршување Airflow во Docker

This guide will walk you through setting up and running Apache Airflow in a Docker container using Dockerfile and docker-compose.yml files provided.

### Prerequisites

Before getting started, ensure you have Docker installed on your system. You can download and install Docker from [here](https://www.docker.com/).

### Installation Steps

1.  **Clone the Repository**:

    `git clone <repository_url>` 
    
2.  **Navigate to the Project Directory**:
    
    `cd <project_directory>` 
 
3.  **Run Docker Compose**:
    
    `docker-compose up -d` 
    
    This command will start the Airflow container in detached mode, meaning it will run in the background.
    

### Accessing Airflow UI

Once the Docker container is up and running, you can access the Airflow UI by navigating to `http://localhost:8080` in your web browser.

### Usage

After setting up Airflow, you can start creating and managing workflows using Airflow's UI. Here's a basic overview of using Airflow:

1.  **Create DAGs**:
    
    DAGs are Python scripts that define workflows. You can create DAGs in the `airflow/` directory.
    
2.  **Start the Scheduler**:
    
    In the Airflow UI, navigate to the Admin tab and start the scheduler. The scheduler orchestrates the execution of tasks defined in your DAGs.
    
3.  **Trigger DAGs**:
    
    Once the scheduler is running, you can trigger DAGs manually or set up schedules for them to run automatically.
    
4.  **Monitor Execution**:
    
    You can monitor the execution of tasks and view logs in the Airflow UI.
    
5.  **Manage Connections and Variables**:
    
    Airflow provides features to manage connections (e.g., database connections) and variables (e.g., configuration settings) through its UI.
    

### Additional Resources

-   [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html): Official documentation for Apache Airflow.
-   [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html): A tutorial to get started with Airflow.

### Notes

-   Ensure that any customizations or additional dependencies required for your workflows are included in the Dockerfile.
-   Adjust ports and volumes in the docker-compose.yml file as needed.
-   For production deployments, consider configuring Airflow with a production-grade database backend and setting up authentication and access controls.
