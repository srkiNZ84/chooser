from google.cloud import firestore
import json

def entrypoint(request):
    if request.method == 'GET':
        getposts(request)
    elif request.method == 'POST':
        addpost(request)
    elif request.method == 'OPTIONS':
        getOptions(request)

def getposts(request):
    print("Getting blog posts")
    if request.method == 'GET':
        db = firestore.Client()
        blog_posts_ref = db.collection(u'posts').get()
        blog_posts = { blog_post.id: blog_post.to_dict() for blog_post in
                blog_posts_ref }
        blog_posts_json = json.dumps(blog_posts)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (blog_posts_json, 200, headers)

def addpost(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    #print("request data is ", request.data)
    request_json = request.get_json()
    #print("Message JSON was ", request_json)
    #if request.args and 'message' in request.args:
    #    return request.args.get('message')
    #elif request_json and 'message' in request_json:
    #    return request_json['message']
    #else:

    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()
    if request_json and 'document' in request_json:
      newdoc = { "content": request_json['document'] }
      db.collection(u'posts').add(newdoc)
    else:
      doc_ref = db.collection(u'posts').document(u'foobar')
      doc_ref.set({
        u'content': u'Lorem Ipsum'
      })
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return ('Successfully saved the post!', 200, headers)

def getOptions(request):
    # Set CORS headers for the preflight request
    # Allows GET requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600'
    }

    return ('Here\'s the headers!', 204, headers)