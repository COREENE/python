C:\Users\Administrator\AppData\Local\Programs\Python\Python35-32\python.exe C:/Users/Administrator/python/awesome-python3-webapp/www/app.py
INFO:root:create database connection pool...
INFO:root:init jinja2...
INFO:root:set jinja2 template path: C:\Users\Administrator\python\awesome-python3-webapp\www\templates
INFO:root:found model: User (table: users)
INFO:root:  found mapping: id ==> <StringField, varchar(50):None>
INFO:root:  found mapping: email ==> <StringField, varchar(50):None>
INFO:root:  found mapping: passwd ==> <StringField, varchar(50):None>
INFO:root:  found mapping: created_at ==> <FloatField, real:None>
INFO:root:  found mapping: image ==> <StringField, varchar(500):None>
INFO:root:  found mapping: name ==> <StringField, varchar(50):None>
INFO:root:  found mapping: admin ==> <BooleanField, boolean:None>
INFO:root:found model: Blog (table: blogs)
INFO:root:  found mapping: id ==> <StringField, varchar(50):None>
INFO:root:  found mapping: user_id ==> <StringField, varchar(50):None>
INFO:root:  found mapping: created_at ==> <FloatField, real:None>
INFO:root:  found mapping: summary ==> <StringField, varchar(200):None>
INFO:root:  found mapping: content ==> <TextField, text:None>
INFO:root:  found mapping: user_name ==> <StringField, varchar(50):None>
INFO:root:  found mapping: name ==> <StringField, varchar(50):None>
INFO:root:  found mapping: user_image ==> <StringField, varchar(500):None>
INFO:root:found model: Comment (table: comments)
INFO:root:  found mapping: id ==> <StringField, varchar(50):None>
INFO:root:  found mapping: user_id ==> <StringField, varchar(50):None>
INFO:root:  found mapping: created_at ==> <FloatField, real:None>
INFO:root:  found mapping: content ==> <TextField, text:None>
INFO:root:  found mapping: blog_id ==> <StringField, varchar(50):None>
INFO:root:  found mapping: user_name ==> <StringField, varchar(50):None>
INFO:root:  found mapping: user_image ==> <StringField, varchar(500):None>
INFO:root:add route GET /api/users => api_get_users()
INFO:root:add route GET / => index(request)
INFO:root:add static /static/ => C:\Users\Administrator\python\awesome-python3-webapp\www\static
INFO:root:server started at http://127.0.0.1:9000...