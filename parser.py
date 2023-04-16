import os
import struct
import pandas as pd

# Define the TPS file structure
HEADER_FORMAT = '12sL'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
DATA_FORMAT = '64sL'
DATA_SIZE = struct.calcsize(DATA_FORMAT)

def read_tps_file(filename):
    # Open the TPS file in binary mode
    with open(filename, 'rb') as tps_file:
        # Read the header data
        header_data = tps_file.read(HEADER_SIZE)
        header = struct.unpack(HEADER_FORMAT, header_data)

        # Read the rest of the data
        data = []
        while tps_file.tell() < os.path.getsize(filename):
            data_chunk = tps_file.read(DATA_SIZE)
            if not data_chunk:
                break

            # Check if the data_chunk size is equal to the expected size, if not, skip the chunk
            if len(data_chunk) != DATA_SIZE:
                print(f"Skipping data chunk of size {len(data_chunk)}, expected size {DATA_SIZE}")
                continue
            
            try:
                data.append(struct.unpack(DATA_FORMAT, data_chunk))
            except struct.error as e:
                print(f'Error unpacking data chunk: {e}')
                print(f'Data chunk: {data_chunk}')
                print(f'Expected size: {DATA_SIZE}')
                print(f'Actual size: {len(data_chunk)}')
                raise

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['name', 'value'])
    print (df)
    return df

if __name__ == '__main__':
    read_tps_file(filename = '../PurchaseOrders.tps')    