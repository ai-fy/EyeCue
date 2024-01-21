

from moviepy.editor import * 
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.all import *

import services.story as story


class Video: 
    
    background_music = "./audio/motivational_music_background.mp3"
    volume_background_music = 0.3

    def create_video(self,story):
        #cycle through scenes and create video with moviepy
        # Generate a text clip. You can customize the font, color, etc.
        #txt_clip = TextClip("Amazing JOBs",fontsize=70,color='white')
        print("creating video")
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

        
        try:
            final_video = concatenate_videoclips(
            [scene_clips[0].fadeout(1)]
            + [clip.fadein(1).fadeout(1) for clip in scene_clips[1:-1]]
            + [scene_clips[-1].fadein(1)], method="compose")
            print("composing video with fades failed ... switching back to hard cuts")
        except:
            final_video = concatenate_videoclips(scene_clips)

        audio_to_mix = final_video.audio
        audio_background = AudioFileClip(self.background_music)
        audio_background = audio_background.volumex(Video.volume_background_music)
        audio_background = audio_background.subclip(0, final_video.duration)
        final_audio = CompositeAudioClip([audio_to_mix,audio_background])
        final_video = final_video.set_audio(final_audio)
        file_path = f"./videos/{story.getRoleText()}.mp4"
        final_video.write_videofile(file_path,fps=24)
        story.addVideo(file_path)

       
        return
    

    def __init__(self) -> None:
        pass

    def show():
        return    