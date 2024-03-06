"""
Name: Abhijit Somnath Shendage
Student ID: 123103499
"""


import requests

cloudlet_url = "http://localhost:5000"


# Function to send HTTP requests to the cloudlet
def send_request(endpoint, data, request_type="POST"):
    url = f"{cloudlet_url}/{endpoint}"
    if request_type == "POST":
        response = requests.post(url, json=data)
    else:
        response = requests.get(url)
    return response.json()


def main():

    #  expecting that cloudlet service is running already,
    # here will create the device object and simulate it;s actions
    #  so will call some dummy get method to check the device life.

    response = send_request("check_if_alive", request_type="GET", data=None)
    # print(response)
    if response and response["message"] == "I am alive!":
        print("\nSuccessfully connected to the cloudlet service")
    else:
        print("Unable to connect to the cloudlet service, exiting")
        exit(-1)

    from device import Device

    # for initial run, clearing all tables
    response = send_request("clear_database", request_type="GET", data=None)
    if response and response["message"] == "Truncate successful!":
        print("Successfully cleared the database tables")
    else:
        print("Failed while truncating the tables")
        exit(-1)

    # create & register devices

    # for simulation I am creating 20 devices of type car and mobile
    #  and registering them in the cloudlet
    devices_parking_spot_sensor = []
    manets = []

    print("\n\n**Devices Registration (REGISTER)**\n")
    for _ in range(15):

        # parking_spot_sensor
        device = Device(device_type="parking_sensor")
        if device.register(
            username="username",
            password="password",
            cloudlet_connection_details=cloudlet_url,
        ):
            devices_parking_spot_sensor.append(device)
        else:
            print("Device-parking spot sensor creation failed")

    print(
        "Parking Spots Created with IDs:",
        [x.device_id for x in devices_parking_spot_sensor],
    )

    # I am creating 3 parkings
    # and registering them in the cloudlet
    devices_parking_manager = []
    for _ in range(3):
        # parking_managers
        device = Device(device_type="parking_manager")
        if device.register(
            username="username",
            password="password",
            cloudlet_connection_details=cloudlet_url,
        ):
            devices_parking_manager.append(device)

        else:
            print("Device-Parking Managers creation failed")

    print(
        "Parking Managers Created with IDs:",
        [x.device_id for x in devices_parking_manager],
    )

    # here, I will establish MANET in such a way that each parking manager will have
    # some parking sensors, and they have already formed a like, say
    # each parking

    # create 3 manets
    print("\n\n**Manet Creation (CREATE)**\n")
    for _ in range(3):  # since there are 3 parking complexes

        # create manet
        create_manet_data = {"manet_type": "parking"}
        manet_id = send_request("create_manet", create_manet_data)["manet_id"]
        print(f"MANET created for parking with ID: {manet_id}")
        manets.append(manet_id)

    # login connect this parking managers to MANET
    print("\n\n**CONNECTING PARKING MANAGERS TO MANETs (JOIN)**\n")
    for i in range(len(devices_parking_manager)):  # since there are 3 parking complexes

        parking_manager = devices_parking_manager[i]
        # login these manets
        message = parking_manager.login(
            cloudlet_connection_details=cloudlet_url,
            username=device.username,
            password=device.password,
        )
        if "success" in message:
            print(f"Parking Manager {parking_manager.device_id} logged in")
            # print(message, "for device", parking_manager.device_id)

        # and join the manet
        message = devices_parking_manager[i].join_network(
            manets[i], cloudlet_connection_details=cloudlet_url
        )
        if "success" in message:
            print(
                f"Parking Manager {parking_manager.device_id} joined MANET {manets[i]}"
            )

    # iterate over devices, login, and connect to MANETs

    print("\n\n**CONNECTING PARKING SPOT SENSORS TO MANETs (JOIN)**\n")
    for device in devices_parking_spot_sensor[0:5]:

        message = device.login(
            cloudlet_connection_details=cloudlet_url,
            username=device.username,
            password=device.password,
        )

        # if message != "Login successful":
        #     print(message, "for device", device.device_id)

        # and this device then joins the manet network
        device.join_network(manets[0], cloudlet_connection_details=cloudlet_url)
        # if message != "Joined MANET successfully":
        #     print(message, "for device", device.device_id)

    print(
        "Parking Spots Sensors with IDs",
        [x.device_id for x in devices_parking_spot_sensor[0:5]],
        "joined the MANET",
        manets[0],
    )

    # iterate over devices, login, and connect to MANETs
    for device in devices_parking_spot_sensor[5:10]:

        message = device.login(
            cloudlet_connection_details=cloudlet_url,
            username=device.username,
            password=device.password,
        )

        # if message != "Login successful":
        #     print(message, "for device", device.device_id)

        # and this device then joins the manet network
        device.join_network(manets[1], cloudlet_connection_details=cloudlet_url)
        # if message != "Joined MANET successfully":
        #     print(message, "for device", device.device_id)

    print(
        "Parking Spots Sensors with IDs",
        [x.device_id for x in devices_parking_spot_sensor[5:10]],
        "joined the MANET",
        manets[1],
    )

    for device in devices_parking_spot_sensor[10:15]:

        message = device.login(
            cloudlet_connection_details=cloudlet_url,
            username=device.username,
            password=device.password,
        )

        # if message != "Login successful":
        #     print(message, "for device", device.device_id)

        # and this device then joins the manet network
        device.join_network(manets[2], cloudlet_connection_details=cloudlet_url)
    print(
            "Parking Spots Sensors with IDs",
            [x.device_id for x in devices_parking_spot_sensor[10:15]],
            "joined the MANET",
            manets[2],
    )
        # if message != "Joined MANET successfully":
        #     print(message, "for device", device.device_id)

    # I will make some devices in the last MANET leave their MANET.

    print("\n\n**PARKING SPOTS SENSORS LEAVING MANET (LEAVE)**\n")
    for device in devices_parking_spot_sensor[7:10]:
        message = device.leave_network(cloudlet_connection_details=cloudlet_url)
        if message == "Left MANET successfully":
            print(f"Device with id {device.device_id} left the network")

    # yoyoyoyo

    #  now will split last network
    #  as per my implementaion, it will be the MANET with highest ID.
    print("\n\n**SPLIT MANETs (SPLIT)**\n")

    manet = manets[-1]
    devices_in_this_manet = []
    response = send_request(
        "get_devices_in_manet", request_type="POST", data={"manet_id": manet}
    )  # ithe response ghya
    devices_in_manet = response["devices_on_manet"]
    # ok, it is list of lists
    # so tyala modify kra
    for i in devices_in_manet:
        devices_in_this_manet.append(i[0])

    # split the network
    response = send_request(
        "split_manet",
        request_type="POST",
        data={"manet_id": manet, "net_type": "parking"},
    )

    def get_object_from_id(device_id):
        for device in devices_parking_spot_sensor:
            if device_id == device.device_id:
                return device
        # backup
        return device

    if response and response["message"] == "Split Successful":
        new_manet_id = response["new_manet_id"]
        manets.append(new_manet_id)

        print(f"Manet {manet} split into {manet} and {new_manet_id}")
        for device_id in devices_in_this_manet[len(devices_in_this_manet) // 2 :]:
            device = get_object_from_id(device_id)

            response = device.leave_network(cloudlet_connection_details=cloudlet_url)

            if "success" in response:
                print(f"Sensor Device {device.device_id} left the MANET {manet}")
                # ithe navin network join kra
                message = device.join_network(
                    new_manet_id, cloudlet_connection_details=cloudlet_url
                )
                if "success" in message:
                    print(
                        f"Sensor {device.device_id} has joined the new network with ID {new_manet_id}"
                    )

    # Merge the network
    print("\n\n**MERGE MANETs (MERGE)**\n")

    # I am merging the last 2 networks
    manet_id_1 = manets[-2]
    manet_id_2 = manets[-1]

    # impacted devices
    response = send_request(
        "get_devices_in_manet", request_type="POST", data={"manet_id": manet_id_2}
    )  # ithe response ghya
    devices_in_manet = response["devices_on_manet"]
    devices_in_this_manet = []
    for i in devices_in_manet:
        devices_in_this_manet.append(i[0])

    response = send_request(
        "merge_manets",
        request_type="POST",
        data={"manet_id_1": manet_id_1, "manet_id_2": manet_id_2},
    )

    if response and "success" in response["message"]:

        print(f"MANETS {manet_id_1} and {manet_id_2} merged")

        # for simulation, choosing random devices
        for device_id in devices_in_this_manet:
            device = get_object_from_id(device_id)
            response = device.leave_network(cloudlet_connection_details=cloudlet_url)

            if "success" in response:
                print(f"Device {device.device_id} left the MANET {manet_id_2}")
                # ithe navin network join kra
                message = device.join_network(
                    manet_id_1, cloudlet_connection_details=cloudlet_url
                )
                if "success" in message:
                    print(
                        f"Sensor {device.device_id} has joined the new network with ID {manet_id_1}"
                    )

    print("\n\n**END**\n")


if __name__ == "__main__":
    main()
