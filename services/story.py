import json
import os
import jsonpickle
from services import llm
from services import voice 

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

    def addEmployeeFeedback(self, text):
        self._generated["employee_feedback"] = text

    def getEmployeeFeedback(self):
        return self._generated["employee_feedback"]        

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
    
    def is_generated(self):
        return self._generated["is_generated"]

    def generateSceneAssets(self, eleven_token,status):
        scene_counter = 0
        for scene in self._scenes:
            scene_counter = scene_counter + 1
            status.update(f"generating image for scene {scene_counter} of {len(self._scenes)}")
            image_filepath, prompt, width, height = llm.generate_image(scene["visualprompt"])
            scene["image"] = image_filepath  
          
            if eleven_token != "":
              status.update(f"generating audio for scene {scene_counter} of {len(self._scenes)}")
              audio_filepath = voice.generate_audio(scene["voiceover"],eleven_token)   
            else:
              audio_filepath = ""
            scene["audio"] = audio_filepath
        self._generated["is_generated"] = True
        return

   

    def __init__(self):
        return
    
    def __init__(self,role_txt):
        self._generated = {
            "is_generated": False,
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