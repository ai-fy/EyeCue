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
    
    def getRoleText(self):
        return self._role

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

    def getScene(self,scene_id):
        #get scene by id from self._scenes
        for scene in self._scenes:
            if scene["id"] == scene_id:
                return scene    
        
    def getSceneDescription(self,scene_id):
        scene = self.getScene(scene_id)
        return scene["text"]

    def getVisualPrompt(self,scene_id):
        scene = self.getScene(scene_id)
        return scene["image_prompt"]
    
    def getAudioPrompt(self,scene_id):
        scene = self.getScene(scene_id)
        return scene["audio_prompt"]
    
    def getSceneImage(self,scene_id):
        scene = self.getScene(scene_id)
        return scene["image"]
    
    def getSceneAudio(self,scene_id):
        scene = self.getScene(scene_id)
        return scene["audio"]

    def addScene(self, text,image_prompt, image,audio_prompt, audio, id):
        self._scenes.append(
            {
                "text": text, 
                "image_prompt": image_prompt,
                "image": image, 
                "audio_prompt": audio_prompt,
                "audio": audio,
                "id": id
            }
            )   
        
    def addVideo(self, video_path):
        self._generated["video"] = video_path

    def getVideo(self):
        return self._generated["video"]    

    def hasVideo(self):
        return self._generated.get("video","") != ""

    def getScenes(self):
        return self._scenes
    
    
    def toVideo(self):

        text = "CFO at LabLab, the place to be for AI"
        text2= "LabLab.ai"
        video_template = """
{
  "id": "q6kbimx5",
  "type": "component",
  "component": "basic/000",
  "settings": {
    "headline": {
      "text": [
        "{text}}"
      ],
      "color": "white",
      "font-family": "EB Garamond",
      "text-align": "center",
      "font-size": "8vw",
      "padding": "3vw 0"
    },
    "body": {
      "color": "white",
      "text": [
        "{text2}"
      ],
      "text-align": "center",
      "font-family": "EB Garamond",
      "font-size": "5vw"
    },
    "card": {
      "vertical-align": "bottom",
      "margin": "5vw",
      "background-color": "rgba(0,100,150,0.5)",
      "border-radius": "2vw"
    }
  },
  "width": 1080,
  "height": 1800,
  "x": 0,
  "y": 0,
  "duration": 10,
  "comment": "Simple card",
  "position": "custom"
}
        """
        return ""

    def __init__(self):
        return
    
    def __init__(self,role_txt):
        self._generated = {
            "story": "",
            "image_prompt": "",
            "images": [],
            "audios": [],
            "videos": []
        }
           # scenes used to generate the story-video, with images, text and audio to be used.
        self._scenes = []

        self._role = role_txt
        return