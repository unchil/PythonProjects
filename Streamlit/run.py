from streamlit.web.bootstrap import run

dirPath='./database_example'

fileName='streamlit_app.py'

real_script = f'{dirPath}/{fileName}'

run(real_script, False, [], {})