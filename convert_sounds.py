# from pydub import AudioSegment

# # Convert each mp3 file to AudioSegment
# audio_files = [AudioSegment.from_mp3('file1.mp3'), AudioSegment.from_mp3('file2.mp3')]

# # Concatenate the audio files
# compiled_music = sum(audio_files)

# # Export the compiled music to a new file
# compiled_music.export('MUSIC.VOX', format='mp3')


# import pygame
# import time

# pygame.init()

# # Initialize mixer
# pygame.mixer.init()

# # Load your compiled music file
# pygame.mixer.music.load('MUSIC.VOX')

# # Play the first section
# pygame.mixer.music.play(start=0, end=10)  # Adjust the start and end points in seconds

# # Wait for a while (replace with your game logic)
# time.sleep(10)

# # Stop the first section
# pygame.mixer.music.stop()

# # Play the second section
# pygame.mixer.music.play(start=10, end=20)  # Adjust the start and end points in seconds

# # Wait for a while (replace with your game logic)
# time.sleep(10)

# # Stop the second section
# pygame.mixer.music.stop()

# pygame.quit()

# import pygame
# import time

# pygame.init()

# # Initialize mixer
# pygame.mixer.init()

# # Load your compiled music file
# pygame.mixer.music.load('MUSIC.VOX')

# # Set an end event to be triggered when the music ends
# music_end_event = pygame.USEREVENT + 1
# pygame.mixer.music.set_endevent(music_end_event)

# # Play the music
# pygame.mixer.music.play()

# running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == music_end_event:
#             # Music has ended, restart the track
#             pygame.mixer.music.rewind()

#     # Your game logic here
#     # ...

#     # Optionally, you can control the loop frequency with pygame.time.Clock()
#     pygame.time.Clock().tick(30)  # 30 frames per second

# pygame.quit()

