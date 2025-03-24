import { useRobotStore } from '../stores/robotStore'

export class WebSocketService {
  private ws: WebSocket | null = null
  private readonly url: string

  constructor() {
    this.url = 'ws://localhost:8000/ws'
  }

  connect() {
    this.ws = new WebSocket(this.url)
    const robotStore = useRobotStore()

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'position_update') {
        robotStore.updateRobotPosition(data.robot_id, [
          data.position.longitude,
          data.position.latitude
        ])
      } else if (data.type === 'status_update') {
        robotStore.updateRobotStatus(data.robot_id, data.status)
      }
    }

    this.ws.onclose = () => {
      console.log('WebSocket disconnected')
      setTimeout(() => this.connect(), 1000)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
    }
  }
}

export const wsService = new WebSocketService() 