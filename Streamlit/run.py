from streamlit.web.bootstrap import run

dirPath='./job_application_example'

fileName='streamlit_app.py'

real_script = f'{dirPath}/{fileName}'

run(real_script, False, [], {})