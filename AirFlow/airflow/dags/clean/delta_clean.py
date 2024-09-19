import pandas as pd

def remove_substrings(string):
  if not string or isinstance(string, list) or not isinstance(string, str):
    return string
  for item in ['\r', '\t','\n']:
    string = string.replace(item, '')
  return string if string else None

def clean_delta(**kwargs):
    ti = kwargs['ti']
    scraped_data = ti.xcom_pull(task_ids='scrape_delta', key='scraped_data')
    df = pd.DataFrame.from_dict(scraped_data)
    new_columns = []
    for key in list(df):
      new_columns.append(key.replace(':', "").strip())
    df.columns = new_columns
   
    for column in df.columns:
      df[column] = df[column].apply(remove_substrings)

    df.rename(columns={
        'Линк': 'link',
        'Шифра': 'code',
        'Опис': 'description',
        'Слики': 'images',
        'Тип на објект' : 'typeobject',
        'Град': 'city',
        'Населба': 'municipality',
        'Локација': 'location',
        'Површина': 'surfacearea',
        'Број на соби': 'numberofrooms',
        'Година на градба': 'yearofconstruction',
        'Кат': 'floornumber',
        'Наместен': 'equipped',
        'Парно': 'heating',
        'Огласот е објавен на': 'datepublished',
        'Цена': 'price',
    }, inplace=True)

    df['images'] = df['images'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

    table_columns = [
    'link', 'code', 'description', 'typeobject', 'city', 'municipality',
    'location', 'surfacearea', 'numberofrooms', 'yearofconstruction', 'floornumber',
    'equipped', 'heating', 'datepublished', 'price']

    df = df[[col for col in df.columns if col in table_columns]]

    kwargs['ti'].xcom_push(key='cleaned_data', value=df.to_dict())
