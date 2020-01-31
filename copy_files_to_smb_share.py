import os

# Two different SMB libraries
import smbclient
from smb.SMBConnection import SMBConnection

# Settings
user = "test_user"
password = "password"
server = "192.168.1.10"


def copy_test_one(source_file: str, target_file: str) -> None:

    # Name of the share
    # Example:
    #   \\FAKEWINDOWS\some_directory\some_subdirectory
    #   In the above path "FAKEWINDOWS" is the name of the smb share
    smb_share = "FAKEWINDOWS"

    # This particular client assumes a client name
    # This may be important if the server requires it
    # NOTE: This is not a username
    client_machine_name = "some-client"

    # This particular client additionally takes a server name
    # As above, this may only be relevant if the server requires it
    server_name = server

    # Register credentials and create a connection
    client = SMBConnection(user, password, client_machine_name, server_name, use_ntlm_v2 = True)
    
    # The connect method returns a boolean
    # True means connected, False means unable to connect
    assert client.connect(server, 139)

    # Read source file
    with open(source_file, 'rb') as file:

        # Target file should be stored in the following remote location
        destination = f"/repository/client-files/{target_file}"

        # Store file 
        client.storeFile(smb_share, destination, file)



def copy_test_two(source_file: str, target_file: str) -> None:

    # Register credentials
    smbclient.register_session(server, username=user, password=password)

    # Absolut file path to the target file
    destination = r"\\{server}\FAKEWINDOWS\repository\client-files\{file}".format(
        server=server,
        file=target_file
    )

    # Read source file
    file_object = open(source_file, "r").read()

    # Write target file
    with smbclient.open_file(destination, mode="w") as remote_file:
        remote_file.write(file_object)


if __name__ == "__main__":
    # Location of test files
    path_to_testfiles = "testfiles"

    # Walk through the directory and subdirectories
    for file_root, file_dir, files in os.walk(path_to_testfiles):

        # Iterate over the files found
        for file_name in files:

            # Construct relative path to file
            testfile = os.path.join(file_root, file_name)

            # We create target file names with prefixes
            # in order to distinguis the two files written per test
            test_one_prefix = f"test_one_{file_name}"
            test_two_prefix = f"test_two_{file_name}"

            # Use copy method one
            copy_test_one(source_file=testfile, target_file=test_one_prefix)

            # Use copy method two
            copy_test_two(source_file=testfile, target_file=test_two_prefix)