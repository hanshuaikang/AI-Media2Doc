import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './scroll-fix.css'  // 添加这一行导入全局滚动修复样式

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
