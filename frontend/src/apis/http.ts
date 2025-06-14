import axios, { AxiosRequestConfig, AxiosResponse, AxiosInstance } from 'axios'
import { ElMessage } from 'element-plus'
import { API_BASE_URL } from '../config'

/**
 * 统一的API请求错误
 */
export class ApiError extends Error {
  status: number
  data?: any

  constructor(message: string, status: number = 500, data?: any) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

/**
 * 统一的HTTP请求服务
 */
class HttpService {
  private axiosInstance: AxiosInstance

  constructor(baseURL: string) {
    this.axiosInstance = axios.create({
      baseURL,
      timeout: 240000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // 请求拦截器
    this.axiosInstance.interceptors.request.use(
      config => {
        // 自动添加Web访问密码请求头
        try {
          const webAccessPassword = localStorage.getItem('webAccessPassword')
          if (webAccessPassword) {
            config.headers = config.headers || {}
            config.headers['request-web-access-password'] = webAccessPassword
          }
        } catch (error) {
          console.warn('获取Web访问密码失败:', error)
        }
        
        return config
      },
      error => Promise.reject(error)
    )

    // 响应拦截器
    this.axiosInstance.interceptors.response.use(
      response => {
        // 检查状态码是否大于200
        if (response.status > 200) {
          const errorData = response.data
          const message = errorData?.detail?.message || errorData?.message || '请求失败'
          const status = response.status
          
          console.error(`API错误 [${status}]:`, message, errorData)
          ElMessage.error(message)
          
          throw new ApiError(message, status, errorData)
        }
        return response.data
      },
      error => {
        let message = '请求失败'
        let status = 500
        let data = null
        
        if (error.response) {
          // 服务器返回了错误响应
          status = error.response.status
          data = error.response.data
          
          // 优先从detail.message获取错误信息
          if (data && typeof data === 'object' && 'detail' in data && (data as any).detail?.message) {
            message = (data as any).detail.message
          } else if (data && typeof data === 'object' && 'message' in data) {
            message = (data as any).message
          } else {
            message = error.message || '请求失败'
          }
        } else {
          // 网络错误或其他错误
          message = error.message || '网络错误'
        }
        
        console.error(`API错误 [${status}]:`, message, data)
        ElMessage.error(message)
        
        return Promise.reject(new ApiError(message, status, data))
      }
    )
  }

  /**
   * 发送HTTP请求
   * @param config 请求配置
   * @returns 响应数据
   */
  async request<T = any>(config: AxiosRequestConfig): Promise<T> {
    try {
      return await this.axiosInstance.request(config)
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      throw new ApiError(error.message || '请求失败')
    }
  }

  /**
   * 上传文件（使用XHR以支持进度回调）
   * @param url 上传URL
   * @param file 文件对象
   * @param onProgress 进度回调
   */
  async uploadFile(url: string, file: Blob, onProgress?: (percent: number) => void): Promise<any> {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable && onProgress) {
          const percent = Math.round((event.loaded / event.total) * 100)
          onProgress(percent)
        }
      }
      
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve({ success: true, status: xhr.status })
        } else {
          reject(new ApiError(`上传失败: ${xhr.status}`, xhr.status))
        }
      }
      
      xhr.onerror = () => {
        reject(new ApiError('网络错误，上传失败'))
      }
      
      xhr.open('PUT', url)
      xhr.send(file)
    })
  }
}

// 导出默认的HTTP服务实例
export default new HttpService(API_BASE_URL)
