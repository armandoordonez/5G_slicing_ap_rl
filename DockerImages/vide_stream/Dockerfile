from ubuntu:trusty 
RUN apt-get -y update 
RUN apt-get -y install vlc
#RUN useradd -ms /bin/bash video_server 
#RUN whoami
USER video_server
#RUN whoami
COPY video.mp4 /home/video_server
CMD su - video_server
CMD unset DISPLAY; vlc-wrapper -R -vvv /home/video_server/video.mp4 --sout '#standard{access=http,mux=asf,dst=0.0.0.0:7079}'


# wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1wLqFqextNvtLRmQaCh5xgx6wHxUTcxil' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1wLqFqextNvtLRmQaCh5xgx6wHxUTcxil" -O video1.mp4 && rm -rf /tmp/cookies.txt
# RUN echo exit 0 > /usr/sbin/policy-rc.d

# 1lAlw_lbzELBhQ1nPeAxNFgs3UHE48FAC

# wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt
# 13Ok0100UDJKQfT5346naXnOa4gpB7Uwo
# wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=13Ok0100UDJKQfT5346naXnOa4gpB7Uwo' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=13Ok0100UDJKQfT5346naXnOa4gpB7Uwo" -O Expedition_Curved.mp4 && rm -rf /tmp/cookies.txt
