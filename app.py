from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy, model
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audiofile.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#database creation and schema defining

class Songs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	duration = db.Column(db.Integer)
	upload_time = db.Column(db.DateTime,  default=db.func.current_timestamp())
	update_time = db.Column(db.DateTime,  default=db.func.current_timestamp(),
					onupdate=db.func.current_timestamp())
	
	
	def __init__(self, name, duration):
		
		self.name = name
		self.duration = duration
				

class Podcast(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	duration = db.Column(db.Integer)
	upload_time = db.Column(db.DateTime,  default=db.func.current_timestamp())
	update_time = db.Column(db.DateTime,  default=db.func.current_timestamp(),
					onupdate=db.func.current_timestamp())
	host = db.Column(db.String(100))
	
	def __init__(self, name, duration, host):
		self.name = name
		self.duration = duration
		self.host = host


class Audiobook(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	narrator = db.Column(db.String(100))
	author = db.Column(db.String(100))
	duration = db.Column(db.Integer)
	upload_time = db.Column(db.DateTime,  default=db.func.current_timestamp())
	update_time = db.Column(db.DateTime,  default=db.func.current_timestamp(),
					onupdate=db.func.current_timestamp())
	
	def __init__(self,  title, narrator, author, duration):
		self.title = title
		self.narrator = narrator
		self.author = author
		self.duration = duration
		


class SongSchema(SQLAlchemySchema):
	class Meta:
		model = Songs
		load_instance = True  

	id = auto_field()
	name = auto_field()
	duration = auto_field()
	upload_time = auto_field()
	update_time = auto_field()

class PodcastSchema(SQLAlchemySchema):
	class Meta:
		model = Podcast
		load_instance = True  

	id = auto_field()
	name = auto_field()
	duration = auto_field()
	upload_time = auto_field()
	host =  auto_field()
	update_time = auto_field()
	
	
class AudiobookSchema(SQLAlchemySchema):
	class Meta:
		model = Audiobook
		load_instance = True  

	id = auto_field()
	title = auto_field()
	duration = auto_field()
	upload_time = auto_field()
	narrator = auto_field()
	author = auto_field()
	update_time = auto_field()
	
	
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)

audiobook_schema = AudiobookSchema()
audiobooks_schema = AudiobookSchema(many=True)



"""
main api start from below
"""


class PostListResource(Resource):

	def get(self,filetype, id=None):
		if filetype == "song":
			if id is None:
				posts = Songs.query.all()
				return jsonify(songs_schema.dump(posts))
			post = Songs.query.get_or_404(id)
			return jsonify(song_schema.dump(post),{"status":200})
			
		elif filetype == "podcast":
			if id is None:
				posts = Podcast.query.all()
				return jsonify(podcasts_schema.dump(posts))
			post = Podcast.query.get_or_404(id)
			return jsonify(podcast_schema.dump(post),{"status":200})
			
		elif filetype == "audiobook":
			if id is None:
				posts = Audiobook.query.all()
				return jsonify(audiobooks_schema.dump(posts))
			post = Audiobook.query.get_or_404(id)
			return jsonify(audiobook_schema.dump(post),{"status":200})
		else:
			return jsonify({"message":"no filetype found"})

	def post(self):
		filetype = request.json['filetype']
		if filetype == 'song':
			new_post = Songs(
			name=request.json['data']['name'],
			duration =request.json['data']['duration']
			)
			db.session.add(new_post)
			db.session.commit()
			return jsonify({
		'Message': f'inserted.', "status" : 200
	})

			
		elif filetype == 'podcast':
			new_post = Podcast(
			name=request.json['data']['name'],
			
			duration =request.json['data']['duration'],
			host = request.json['data']['host']
			)
			db.session.add(new_post)
			db.session.commit()
			return jsonify({
		'Message': 'inserted.', "status" : 200
	})
			
		elif filetype == 'audiobook':
			new_post = Audiobook(
			title=request.json['data']['title'],
			
			narrator = request.json['data']['narrator'],
			author = request.json['data']['author'],
			duration =request.json['data']['duration']

			)
			db.session.add(new_post)
			db.session.commit()
			return jsonify({"message":"inserted", "status" : 200})
		
	def delete(self, filetype, id):
		if filetype == "song":
			post = Songs.query.get_or_404(id)
			db.session.delete(post)
			db.session.commit()
			return jsonify({"message":"deleted"},{'status':204})	
		elif filetype == "podcast":
			post = Podcast.query.get_or_404(id)
			db.session.delete(post)
			db.session.commit()
			return jsonify({"message":"deleted"},{'status':204})
		elif filetype == "audiobook":
			post = Audiobook.query.get_or_404(id)
			db.session.delete(post)
			db.session.commit()
			return jsonify({"message":"deleted"},{'status':204})
		else:
			return jsonify({"message":"file type not found"},{'status':405})
		
		
	def put(self, filetype,id):
		if filetype == "song":
			
			user = Songs.query.get_or_404(id)
			
			try:
				name = request.json['data']['name']
				user.name = name
			except:
				pass
			try:
				duration = request.json['data']['duration']
				user.duration = duration
			except:
				pass
			db.session.commit()
			return jsonify({
				'Message': 'updated' , "status" : 200
			})
		elif filetype == "podcast":
			update_data = Songs.query.get_or_404(id)
			try:
				name = request.json['data']['name']
				update_data.name = name
			except:
				pass
				
			try:
				duration = request.json['data']['duration']
				update_data.duration = duration
			except:
				pass
				
			try:
				host = request.json['data']['host']
				update_data.host= host
			except:
				pass
			db.session.commit()
			return jsonify({
				'Message': 'updated' , "status" : 200
			})	
		elif filetype == "audiobook":
			update_data = Audiobook.query.get_or_404(id)
			try:
				title = request.json['data']['title']
				update_data.title = title
			except:
				pass
			
			try:
				narrator = request.json['data']['narrator']
				update_data.narrator = narrator
			except:
				pass
			try:
				author = request.json['data']['author']
				update_data.author = author
			except:
				pass
			try:
				duration = request.json['data']['duration']
				update_data.duration = duration
			except:
				pass
		
			db.session.commit()
			return jsonify({
				'Message': 'updated' , "status" : 200
			})
		else:
			return ({
				'Message': 'file not found' , "status" : 405
			})


api.add_resource(PostListResource, '/api','/api/<filetype>/<id>','/api/<filetype>',
			methods=['GET', 'POST','PUT', 'DELETE'])



if __name__ == '__main__':
	app.run(debug=True)
	