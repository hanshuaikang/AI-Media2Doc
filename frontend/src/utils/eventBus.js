import { reactive } from 'vue'

export const eventBus = reactive({
    handlers: {},

    on(event, callback) {
        if (!this.handlers[event]) {
            this.handlers[event] = []
        }
        this.handlers[event].push(callback)
    },

    emit(event, ...args) {
        if (this.handlers[event]) {
            this.handlers[event].forEach(callback => callback(...args))
        }
    },

    off(event, callback) {
        if (this.handlers[event]) {
            if (callback) {
                this.handlers[event] = this.handlers[event].filter(cb => cb !== callback)
            } else {
                delete this.handlers[event]
            }
        }
    }
})
