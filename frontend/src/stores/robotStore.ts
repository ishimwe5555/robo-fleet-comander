import { defineStore } from 'pinia'

interface RobotState {
  robots: Robot[]
  connected: boolean
}

interface Robot {
  id: string
  name: string
  status: string
  position: [number, number]
}

export const useRobotStore = defineStore('robot', {
  state: (): RobotState => ({
    robots: [],
    connected: false
  }),
  
  actions: {
    updateRobotStatus(robotId: string, status: string) {
      const robot = this.robots.find(r => r.id === robotId)
      if (robot) robot.status = status
    }
  }
}) 