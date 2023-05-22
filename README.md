# 

# Instructions to Set Up Virtual Environment and Script

## Navigate to Desired Location

```
cd /home/<user>/
```

**Create Virtual Environment**

```jsx
python3 -m venv venv
```

**Activate the Virtual Environment**

```jsx
source venv/bin/activate
```

**Install Necessary Packages**

```jsx
pip install opencv-python deepface requests
```

**Create a Script**

```jsx
nano run_script.sh
```

**Paste the Following Into the Script**

```jsx
#!/bin/bash
export DISPLAY=:0
cd <location where you created virtal env>
source venv/bin/activate
python3 <location where you placed face_detection.py>
```

**Make the Script Executable**

```jsx
chmod +x run_script.sh
```

**Create a Systemd Service**

```jsx
sudo nano /etc/systemd/system/script.service
```

**Paste the Following Inside**

```jsx
[Unit]
Description=Run script on startup and user login

[Service]
ExecStart=<location of script_name.sh file>

[Install]
WantedBy=default.target
```

**Navigate to Home Directory**

```jsx
cd
```

**Create a Folder for the Weights and Download the Weights**

```jsx
mkdir -p .deepface/weights
wget https://github.com/serengil/deepface_models/releases/download/v1.0/vgg_face_weights.h5 -P .deepface/weights/
```

**Activate the Script Service**

```jsx
sudo systemctl enable script.service
sudo systemctl start script.service
```
