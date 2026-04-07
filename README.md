# **CMPT 371 A3 Socket Programming `File Transfer System`**

**Course:** CMPT 371 \- Data Communications & Networking  
**Instructor:** Mirza Zaeem Baig  
**Semester:** Spring 2026  

## **Group Members**

| Name | Student ID | Email |
| :---- | :---- | :---- |
| William Phan | 301468740 | lwp1@sfu.ca |
| Parsa Ghaderi | 301623337 | john.smith@university.edu |

## **1\. Project Overview & Description**

This project is a File Transfer System built using Python's TCP Socket API. It allows a client to connect to a central server via a Command Line Interface (CLI) to transfer files of any format. The system uses a custom 64-byte header to transmit file metadata before sending the actual file data in small chunks. This architecture ensures that even massive files can be transferred safely without overloading system memory.

## **2\. System Limitations & Edge Cases**

As required by the project specifications, we have identified and handled (or defined) the following limitations and potential issues within our application scope:

* **Memory Management & Large File Transfers:** 
  * <span style="color: green;">*Solution:*</span> To prevent system memory crashes, we implemented stream chunking. The application reads and transmits data in 1024-byte chunks rather than loading an entire file into RAM at once. This allows the system to transfer massive, multi-gigabyte files with virtually zero memory overhead (the largest file we tested was 10GB).
  * <span style="color: red;">*Limitation:*</span> The system currently lacks a state-saving or "resume" feature. Because TCP streams are continuous, any network interruption or timeout during a lengthy transfer will cause a complete failure, requiring the client to restart the transfer from the beginning.
* **Handling Multiple Clients Concurrently:**
  * <span style="color: red;">*Limitation:*</span> The server uses a single-threaded blocking architecture. It processes file transfers sequentially. If multiple clients attempt to send files simultaneously, secondary clients are queued by the operating system and must wait until the active transfer is fully complete before their connection is processed.
* **Data Separation (Metadata vs. Binary Payload):**
  * <span style="color: green;">*Solution:*</span> Unlike text-based applications that can easily use JSON, transmitting raw binary files (like `.mp4` or `.jpg`) requires strict separation to prevent data corruption. We solved this by creating a custom application-layer protocol. The system forces the first exactly 64 bytes of the connection to contain the metadata (filename and filesize, padded with null bytes). The server reads exactly 64 bytes, extracts the data, and immediately switches to streaming the remaining incoming bytes purely as raw binary payload.
 
## **3\. Video Demo**

Our 2-minute video demonstration covering connection establishment, data exchange, and process termination can be viewed below:  
[**▶️ Watch Project Demo on YouTube**](temp)

## **4\. Prerequisites (Fresh Environment)**

To run this project, you need:

* **Python 3.10** or higher.  
* The `tqdm` library (used for the CLI progress bars). You must install external dependencies using the included `requirements.txt` file. 
* (Optional) VS Code or Terminal.

## **5\. Step-by-Step Run Guide**

### **Step 1: Install Dependencies**

Open your terminal and navigate to the project folder. Install the required `tqdm` library. 
```bash
pip install -r requirements.txt 
# Console output: "Successfully installed tqdm..."
```

### **Step 2: Start the Server**

Ensure you are still in the project directory. The server binds to 127.0.0.1 on port 65000 and will enter a continuous listening loop. 
```bash
python server.py  
# Console output: ""Server started successfully. Listening on 127.0.0.1:65000..."
# Console output: "Waiting for a client to connect..."
```

### **Step 3: Connect Client & Transfer File**

Open a **new** terminal window (keep the server running). Ensure you have placed the file you want to transfer inside the `client_data` folder (e.g., `test_file.txt`). Run the client script followed by your **exact** filename (including the file extension). The following command is for the included test file.
```bash
python client.py test_file.txt 
# Console output: "Connecting to server at 127.0.0.1:65000..."
# Console output: "Connected successfully!"
# Console output: "Sending test_file.txt: 100%|██████████| 21.0/21.05 [00:00<00:00, 3.10MB/s]"
# Console output: "Transfer complete!"
```

### **Step 4: Verify the Transfer & Close the Server**

1. Watch the synchronized `tqdm` progress bars fill up on both the client and server terminals.  
2. The client terminal will state: `Transfer complete!`
3. Navigate to the newly generated `server_data` folder in your project directory to verify the file arrived completely intact and uncorrupted. 
4. **Continuous Operation:** Because the server runs sequentially, you can immediately run Step 3 again with a different file. 
5. To gracefully terminate the server, click into the server terminal and press `Ctrl+C`.

## **6\. Academic Integrity & References**

* **Code Origin:**  
  * The socket boilerplate was adapted from the [**TA YouTube tutorials**](https://www.youtube.com/playlist?list=PL-8C2cUhmkO1yWLTCiqf4mFXId73phvdx). The base of the file transfer system was adapted from [**this online source.**](https://medium.com/@CHICHEEE/build-a-simple-file-transfer-system-using-python-network-programming-project-c9962cf238c0)
* **GenAI Usage:**  
  * ChatGPT was used to assist in generating the print statements for the console output including the status and errors. ChatGPT was also used sparingly for some of the logic (as cited in the `.py` files) for the header management and the `tqdm` progress bar for visuals.
* **README.md Origin**
  * The formatting for the `README.md` file was very closely based of the [**TA's example README.md.**](https://github.com/mariam-bebawy/CMPT371_A3_Socket_Programming/blob/main/README.md)
