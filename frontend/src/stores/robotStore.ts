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
    async fetchRobots() {
      try {
        const response = await fetch('http://localhost:8000/api/robots')
        const data = await response.json()
        this.robots = data.robots.map((robot: any) => ({
          ...robot,
          position: [robot.longitude, robot.latitude]
        }))
      } catch (error) {
        console.error('Error fetching robots:', error)
      }
    },

    updateRobotStatus(robotId: string, status: string) {
      const robot = this.robots.find(r => r.id === robotId)
      if (robot) robot.status = status
    },

    updateRobotPosition(robotId: string, position: [number, number]) {
      const robot = this.robots.find(r => r.id === robotId)
      if (robot) robot.position = position
    }
  }
}) 