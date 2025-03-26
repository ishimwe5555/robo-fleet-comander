import asyncio
import math
from typing import Dict, Tuple
from ..websocket.connection import manager
from ..models.robot import TrailPoint
from ..database import SessionLocal

# ... existing imports ...

class MovementSimulator:
    def __init__(self):
        self.running_simulations = {}

    def calculate_next_position(
        self,
        current: Tuple[float, float],
        target: Tuple[float, float],
        step: float = 0.001
    ) -> Tuple[float, float]:
        dx = target[0] - current[0]
        dy = target[1] - current[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < step:
            return target
        
        return (
            current[0] + (dx / distance) * step,
            current[1] + (dy / distance) * step
        )

    async def move_robot(self, robot_id: str, target_position: Tuple[float, float], current_position: Tuple[float, float]):
        while True:
            if robot_id not in self.running_simulations:
                break

            next_pos = self.calculate_next_position(current_position, target_position)
            
            # Record trail point
            db = SessionLocal()
            try:
                trail_point = TrailPoint(
                    robot_id=robot_id,
                    longitude=next_pos[0],
                    latitude=next_pos[1]
                )
                db.add(trail_point)
                db.commit()
            finally:
                db.close()

            await manager.broadcast_robot_position(
                robot_id,
                {"latitude": next_pos[1], "longitude": next_pos[0]}
            )
            
            if next_pos == target_position:
                self.running_simulations.pop(robot_id, None)
                break

            current_position = next_pos
            await asyncio.sleep(0.1)

    def start_robot_movement(self, robot_id: str, current_position: Tuple[float, float], target_position: Tuple[float, float]):
        if robot_id in self.running_simulations:
            self.running_simulations[robot_id] = False
        
        self.running_simulations[robot_id] = True
        asyncio.create_task(self.move_robot(robot_id, target_position, current_position))

    def stop_robot_movement(self, robot_id: str):
        self.running_simulations.pop(robot_id, None)

movement_simulator = MovementSimulator()

