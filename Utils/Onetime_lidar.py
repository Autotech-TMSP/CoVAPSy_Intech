from Lidar.HokuyoReader import HokuyoReader

IP = '192.168.0.10'
PORT = 10940

def main():
    # Create an instance of HokuyoReader
    lidar = HokuyoReader(IP, PORT)
    
    # Stop any previous measurements
    lidar.stop()
    
    # Start a single read
    lidar.singleRead(0, 1080)
    
    # Print the distance values
    print(lidar.rDistance)
    
    # Stop the lidar
    lidar.stop()

if __name__ == '__main__':
    main()