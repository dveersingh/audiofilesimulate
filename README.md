# audiofilesimulate

## requirments:


```bash

pip install flask-marshmallow
pip install Flask-RESTful
pip install Flask  
pip install Flask-SQLAlchemy
pip install marshmallow-sqlalchemy

```




## create endpoint :


 	url = http://127.0.0.1:5000/api

 
### audiobook:
			 
			 
```json

{"filetype" : "audiobook",
    "data" :{
       "title" : "twinkle twinkle",
       "narrator":"john wick",
       "author":"harry pottr",
     "duration" : 250,
     "host":"johnson"}
}
```


### song:


```json
{"filetype" : "song",
    "data" :{
       "name" : "twilight",
     "duration" : 600
    }
}
```


### podcast:


```json
{"filetype" : "podcast",
    "data" :{
       "name" : "pain",
     "duration" : 20000,
     "host" : "tedx"
    }
}
```

response : 
```json

{
    "Message": "inserted.",
    "status": 200
}
```








## 2.get endpoint: 

#### example


http://127.0.0.1:5000/api/filetype/id
	
	
http://127.0.0.1:5000/api/song


return all files from a particular filetype


		####### with id :
		

url :   http://127.0.0.1:5000/api/filetype/id
	
	
example :    http://127.0.0.1:5000/api/song/1


return details of particular id 
	
	






## 3.  put enddpoint :


link : http://127.0.0.1:5000/api/filetype/id


example:   http://127.0.0.1:5000/api/audiobook/200

body same as create

```json
{
    "Message": "updated",
    "status": 200
}
```

## 4.  delete endpopint:


link: http://127.0.0.1:5000/api/filetype/id
	

###### example : http://127.0.0.1:5000/api/song/1


###### output

```json
{
        "message": "deleted"
    },
    {
        "status": 204
    }
```


