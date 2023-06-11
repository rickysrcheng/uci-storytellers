import json
from random import sample

class VIST:
    def __init__(self, sis_file = None):
        if sis_file != None:
            sis_dataset = json.load(open(sis_file, 'r'))
            self.LoadAnnotations(sis_dataset)


    def LoadAnnotations(self, sis_dataset = None):
        images = {}
        stories = {}

        if 'images' in sis_dataset:
            for image in sis_dataset['images']:
                images[image['id']] = image

        if 'annotations' in sis_dataset:
            annotations = sis_dataset['annotations']
            for annotation in annotations:
                story_id = annotation['story_id']
                stories[story_id] = stories.get(story_id, []) + [annotation]

        self.images = images
        self.stories = stories

    def SampleStoryImages(self):
        selected = sample(list(self.stories.keys()), 1)
        return [seq["photo_flickr_id"] for seq in self.stories[selected[0]]]

