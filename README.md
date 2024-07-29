# rtsp-videoclip-save
Script to access the server and download specific time segments of RTSP camera videos.


## Pipeline
Disconnect from the Wi-Fi network and connect the LAN port. After connecting to the LAN environment, set IPv4, IP, Subnet mask, Router, DNS Server, and Domain according to your custom environment. Then, use the 'curl' command below to establish communication and receive responses.

### 1. Server Login and Receive auth-token and api-serial
* You will need the API server and Port, ID, and PW information for this step.

```
curl -v -X GET "your_ip:port/api/login?force-login=false" \
-H "x-account-id:your_id" \
-H 'x-account-pass:your_pw' \
-H "x-account-group:your_group(option)" \
-H "x-license:licNormalClient" \
--max-time 30
```

<img width="650" alt="스크린샷 2024-07-29 오후 8 57 02" src="https://github.com/user-attachments/assets/026cb98f-0401-468f-907c-fda4e4baff7a">

### 2. Return RTSP Address (Optional)
* You can use the token and serial to return the RTSP address. Afterward, you can verify it in real-time using VLC.

```
curl -v -X GET "your_ip:port/api/video/rtsp-url/${serial}/0/0" \
-H "x-auth-token: token" \
-H "x-api-serial: serial" \
--max-time 30
```

### 3. Input auth-token and api-serial into the Script and Execute

* Then, the clip for the specified time interval will be downloaded using the token and serial.