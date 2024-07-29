import pandas as pd
import subprocess
import logging
import os 

def main():
    """
    Read the control log xlsx file from monitoring office
    and download videos by "unique number".
    """
    # Set the log file save path
    log_name = os.path.join("your_log_path", "main.log")
    logging.basicConfig(filename=log_name, level=logging.INFO, 
                                format='%(asctime)s - %(levelname)s - %(message)s', 
                                datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    
    # Read the control log xlsx file from Songpa District Office
    df = pd.read_excel('your_control_log_path')
    
    # Specify the date format
    df["from_date"] = pd.to_datetime(df["관제일 (yyyymmdd)"].astype(str) + ' ' + df["이벤트 시작시간 (hh:mm:ss)"].astype(str), format="%Y%m%d %H:%M:%S")
    df["to_date"] = pd.to_datetime(df["관제일 (yyyymmdd)"].astype(str) + ' ' + df["이벤트 종료시간 (hh:mm:ss)"].astype(str), format="%Y%m%d %H:%M:%S")
    df["from_date"] = df["from_date"].dt.strftime("%Y%m%d%H%M%S")
    df["to_date"] = df["to_date"].dt.strftime("%Y%m%d%H%M%S")

    # Extract only the necessary information
    rtsp_df = df[['카메라 ID (ddddddd)', '카테고리', 'from_date', 'to_date', '고유 번호 (ddd or dddd)']]
    
    # Download videos for each unique number within the specified time interval
    for index, row in rtsp_df.iterrows():
        logger.info(f"Camera Unique Number: {row['고유 번호 (ddd or dddd)']}")
        dev_serial = row['고유 번호 (ddd or dddd)']
        from_date = row['from_date']
        to_date = row['to_date']
        camera_id = str(row['카메라 ID (ddddddd)'])
        category = row['카테고리']
        
        # Specify the save path
        output_file = f"/Volumes/Elements/crime/{camera_id}_{dev_serial}_{from_date}_{to_date}_{category}.mp4"
        
        x_auth_token = "your_auth_token"
        x_api_serial = "your_api_serial"
        command = f"""
        curl -v -X GET "your_ip/api/video/download/{dev_serial}/0?from_date={from_date}&to_date={to_date}&format=mp4" \
        -H "x-auth-token: {x_auth_token}" \
        -H "x-api-serial: {x_api_serial}" \
        -o "{output_file}" \
        """  
        
        # Set exception handling logic
        try:
            # Execute the curl command
            subprocess.run(command, shell=True)
            # Log the saved file
            logger.info(f"Downloaded {output_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Command execution failed for {output_file}: {e}")
        except FileNotFoundError as e:
            logger.error(f"File path not found: {output_file}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred for {output_file}: {e}")
        
        # Execute the curl command 
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
