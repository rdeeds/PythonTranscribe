This is a small python project. It takes a sound file and returns the transcribed text.

It uses AWS Transcribe through the Boto3 lib. The flow is pretty simple. Bring any wav file into test_audio folder.
point the last line of app.py to that file. Make sure you have your API keys from AWS and you have roles set for both
Transcribe and S3. Run the app and you should have a text file with the output in final_txt_file.

I have provided 3 test audio files. 2 small ones and 1 long one. There is a corrosponding json file and then final text
file.