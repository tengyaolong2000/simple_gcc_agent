#Courtesy of https://huggingface.co/spaces/Mightypeacock/tool-YoutubeTranscript/blob/main/tool.py

from smolagents import Tool
from typing import Optional

class YouTubeTranscriptExtractor(Tool):
    description = "Extracts the transcript from a YouTube video."
    name = "youtube_transcript_extractor"
    inputs = {'video_url': {'type': 'string', 'description': 'The URL of the YouTube video.'}}
    output_type = "string"

    def forward(self, video_url: str) -> str:

        try:
          from pytubefix import YouTube
          # Create a YouTube object
          yt = YouTube(video_url)
          lang='en'

          # Get the video transcript
          if lang in yt.captions:
              transcript = yt.captions['en'].generate_srt_captions()

          else:
              transcript = yt.captions.all()[0].generate_srt_captions()
              lang=yt.captions.all()[0].code

          return lang + "transcript : " + transcript
        # return transcript


        except Exception as e:

          return f"An unexpected error occurred: {str(e)}"



class LinksCheckpointStorage(Tool):
    description = "Implements a queue to store the latest 3 links to serve as checkpoints that anchors the agent to steps which the agent is most confident about. The agent may retrieve these links to go to them when the agents realises it is lost."
    name = "links_checkpoint_storage"
    inputs = {
       'link': {'type': 'string', 'description': 'The URL of the YouTube video.'},
       'retrieve': {'type': 'boolean', 'description': 'Whether to retrieve the last link or to push the latest link.', 'nullable': True}
    }
    output_type = "string"
    
    def forward(self, link: str, retrieve: bool = False) -> Optional[str]:
        if not hasattr(self, 'links'):
            self.links = []

        if retrieve:
            if self.links:
                return self.links[-1]
            else:
                return None
        else:
            if link in self.links:
                pass
            else:
                if len(self.links) >= 3:
                    self.links.pop(0)
                self.links.append(link)
        return None
   
YouTubeTranscriptExtractorTool = YouTubeTranscriptExtractor()
LinksCheckpointStorageTool = LinksCheckpointStorage()

if __name__ == "__main__":
    # check if subclass of tool
    print(issubclass(YouTubeTranscriptExtractor, Tool))
    print(issubclass(LinksCheckpointStorage, Tool))
    # check if instance of tool
    print(isinstance(YouTubeTranscriptExtractor(), Tool))
    print(isinstance(LinksCheckpointStorage(), Tool))