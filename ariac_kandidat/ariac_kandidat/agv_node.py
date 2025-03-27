import rclpy
from rclpy.node import Node
from ariac_msgs.srv import MoveAGV
from std_srvs.srv import Trigger

class AGVController(Node):
    def __init__(self):
        super().__init__('agv_controller')     

    def lock_agv_tray(self, agv_id: int):
        """Locks the tray of the specified AGV (1 or 2)."""
        lock_agv_tray_client = self.create_client(Trigger, f'/ariac/agv{agv_id}_lock_tray')

        self.get_logger().info(f'Waiting for /ariac/agv{agv_id}_lock_tray service...')
        lock_agv_tray_client.wait_for_service()

        request = Trigger.Request()

        future = lock_agv_tray_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result().success:
            self.get_logger().info(f" Tray on AGV {agv_id} locked.")
        else:
            self.get_logger().error(f" Failed to lock tray on AGV {agv_id}.")

    def move_agv(self, destination_id: int):
        """Moves the AGV to a predefined destination by ID (e.g., 1 = station_1)."""
        move_agv_client = self.create_client(MoveAGV, f'/ariac/move_agv{destination_id}')

        self.get_logger().info(f'Waiting for /ariac/move_agv{destination_id} service...')
        move_agv_client.wait_for_service()

        request = MoveAGV.Request()
        request.location = destination_id

        future = move_agv_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result().success:
            self.get_logger().info(f" AGV moved to location ID {destination_id}.")
        else:
            self.get_logger().error(" Failed to move AGV.")
