import json
import os
import jsonpickle


#collection of stories, can be stored to filesystem and loaded 

class stories: 

    def getStories(self):
        return self._stories["_stories"]
    
    def getStoryAmount(self):
        return len(self._stories["_stories"])

    def incrementLastId(self):
        self._stories["lastId"] = self._stories["lastId"] + 1
        return self._stories["lastId"]
    
    def addStory(self, story):

        self._stories["_stories"].append(
            {
                "id": self.incrementLastId(),
                "story": story,
            }
        )

    def isSaved(self):
        #check if stories are saved to filesystem
        return os.path.isfile('./data/stories.json')


    def save(self):
        #safe self._stories as json format to filesystem at ./data/stories.json
        with open('./data/stories.json', 'w') as outfile:
            json_obj = jsonpickle.encode(self._stories)
            outfile.write(json_obj)

            

    def load(self):
        #load self._stories from json on filesystem
        with open('./data/stories.json') as json_file:
            json_str = json_file.read()
            self._stories = jsonpickle.decode(json_str)

    def __init__(self):
        self._stories = {
            "lastId": 0,
            "_stories": []
        }
        return
     

#class for a story, with initial inputs, generated assets and final composition for video creation and end result
class story: 

    def getAudioPaths(self): 
        #return list of audio paths
        audio_paths = []
        for audio in self._generated["audios"]:
            audio_paths.append(audio["audio"])
        return audio_paths 
    
    def getImagePaths(self): 
        #return list of image paths
        image_paths = []
        for image in self._generated["images"]:
            image_paths.append(image["image"])
        return image_paths

    def addImage(self, image_path, width, height, caption="", used_prompt=""):
        self._generated["images"].append(
            {
                "image": image_path, 
                "caption": caption, 
                "prompt": used_prompt, 
                "width": width,
                "height": height
            }
            )
        
    # add audio to the story
    def addAudio(self, audio_path, used_prompt=""):
        self._generated["audios"].append(
            {
                "audio": audio_path, 
                "prompt": used_prompt
            }
            )   
    #add story text
    def addStory(self, text):
        self._generated["story"]= text

    #add image prompt
    def addImagePrompt(self, text):
        self._generated["image_prompt"] = text    

    def addScene(self, text,image,audio):
        self._scenes.append(
            {
                "text": text, 
                "image": image, 
                "audio": audio
            }
            )   

    def __init__(self):
        return
    
    def __init__(self,role_txt):
        self._generated = {
            "story": "",
            "image_prompt": "",
            "images": [],
            "audios": [],
            "videos": [],
        }
           # scenes used to generate the story-video, with images, text and audio to be used.
        self._scenes = []

        self._role = role_txt
        return