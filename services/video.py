

from moviepy.editor import * 
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.all import *
import services.story as story


class Video: 
    
    def create_video(self,story):
        #cycle through scenes and create video with moviepy
        # Generate a text clip. You can customize the font, color, etc.
        #txt_clip = TextClip("Amazing JOBs",fontsize=70,color='white')

        scene_clips = []
        for scene in story.getScenes():
            #create image clip
            scene_id = scene["id"]
            if story.getSceneImage(scene_id) != "":
                #load audio and get duration of it
                if story.getSceneAudio(scene_id) != "":
                    audioclip = AudioFileClip(story.getSceneAudio(scene_id))
                    duration = audioclip.duration

                image_clip = ImageClip(story.getSceneImage(scene_id),duration=duration) 
                videoclip = image_clip.set_audio(audioclip) 
                scene_clips.append(videoclip)#videoclip.set_start(round(duration/3)).crossfadein(round(duration/2)))

        #final_video = CompositeVideoClip(scene_clips)
        final_video = concatenate_videoclips(scene_clips)
        file_path = f"./videos/{story.getRoleText()}.mp4"
        final_video.write_videofile(file_path,fps=24)
        story.addVideo(file_path)
        

        #image_clip = ImageClip("./images/generated_image_20240118_144545.png",duration=10)
        #image_clip2 = ImageClip("./images/generated_image_20240118_144649.png",duration=10)

        # Say that you want it to appear 10s at the center of the screen
        #txt_clip = txt_clip.set_pos('center').set_duration(10)

        # Overlay the text clip on the first video clip
        # fade1 = image_clip.fx(fadeout, duration=2)
        # fade1 = image_clip.fx(vfx.resize,newsize=0.5)
        # fade2 = image_clip2.fx(fadein, duration=2)
        #video = CompositeVideoClip([fade1, fade2.set_start(3).crossfadein(1)])
        
        
       # video = CompositeVideoClip([image_clip,image_clip2])

        # Write the result to a file (many options available !)
        #video.write_videofile("firstTest.mp4",fps=24)
        return
    

    def __init__(self) -> None:
        pass

    def show():
        return    