from google.cloud import vision
from google.cloud import datastore
client_image = vision.ImageAnnotatorClient()

def object_detection(event, context):


    image = vision.types.Image()
    #getting the source image
    image.source.image_uri = 'gs://'+event['bucket']+'/'+event['name']

    response = client_image.label_detection(image=image)
    labels = response.label_annotations
    #saving the labels in a list
    label_list = []
    for label in labels:
        label_list.append(label.description)

    #inserting the labels in datastore kishan_datastore
    client_datastore = datastore.Client()
    task = datastore.Entity(client_datastore.key('kishan_datastore'))
    task.update({
        'labels': label_list,
    })
    client_datastore.put(task)

